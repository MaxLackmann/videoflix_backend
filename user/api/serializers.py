from rest_framework import serializers
from user.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    repeated_password= serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'repeated_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError([{"details": "Password fields didn't match."}])
        return attrs
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError([{"details": "Email already exists."}])
        return value
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError([{"details": "Username already exists."}])
        return value
    
    # def validate_password(self, value):
    #     if len(value) < 8:
    #         raise serializers.ValidationError([{"password": "Password must be at least 8 characters."}])
    #     return value
    
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user