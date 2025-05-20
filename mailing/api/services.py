from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_verification_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"http://localhost:4200/verify-email?uid={uid}&token={token}"

    send_mail(
        subject="E-Mail bestätigen",
        message=f"Klicke auf diesen Link zur Bestätigung:\n{link}",
        from_email="noreply@videoflix.de",
        recipient_list=[user.email],
        fail_silently=False,
    )
