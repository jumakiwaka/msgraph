from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_test_user_token() -> str:
    user_details = {
        "username": "testuser@msgraph.com",
        "email": "testuser@msgraph.com"
    }
    user, created = User.objects.get_or_create(**user_details)
    token, created = Token.objects.get_or_create(user=user)
    return token.key

  
