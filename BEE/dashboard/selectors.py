"""All logic to get/retrieve data from the db stays here"""
from dashboard.models import IntegratedAccount
from django.contrib.auth.models import User


def get_user_account(user) -> User:
    integrated_account = IntegratedAccount.objects.filter(user=user).first()
    if integrated_account:
        return integrated_account.connected_account
    return None
