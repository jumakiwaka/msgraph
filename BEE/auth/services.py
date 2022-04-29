"""All logic to mutate data from db stays here"""

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_update_user(user_data: dict) -> User:
    username = user_data.get("userPrincipalName")
    email = username
    fname = user_data.get("givenName")
    lname = user_data.get("surname")

    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.first_name = fname
    user.last_name = lname
    user.save()

    return user


def create_update_user_token(user: User) -> Token:
    user_token, created = Token.objects.get_or_create(user=user)

    return user_token
