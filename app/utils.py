from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail


ADMIN_EMAIL = 'admin@localhost'

def set_jwt_cookies(response, user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )

def send_email(subject, body, address):
    send_mail(subject, body, ADMIN_EMAIL, [address])