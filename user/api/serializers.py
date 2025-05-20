from rest_framework import serializers
from user.models import CustomUser
from mailing.api.services import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    repeated_password= serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'repeated_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"detail": ["Password fields didn't match."]})
        return attrs
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"detail": ["Email already exists."]})
        return value
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        validated_data['username'] = validated_data['email']
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        send_verification_email(user)
        return user
    
class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = CustomUser.objects.get(pk=uid)
        except (CustomUser.DoesNotExist, ValueError):
            raise serializers.ValidationError({"detail": ["User does not exist."]})

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError({"detail": ["Token is not valid."]})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }