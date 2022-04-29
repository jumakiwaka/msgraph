"""All logic to mutate data from db stays here"""
from dashboard.models import ConnectedAccount, IntegratedAccount
from datetime import datetime, timedelta
from dashboard.tasks import sync_task


def integrate_account(user, access_token, expires_in, refresh_token=None) -> None:
    account, created = ConnectedAccount.objects.get_or_create(
        user=user, email=user.email
    )
    integrated_account, created = IntegratedAccount.objects.get_or_create(
        user=user, connected_account=account
    )

    account.access_token = access_token
    account.access_token_expire_date = datetime.now() + timedelta(seconds=expires_in)
    account.refresh_token = refresh_token
    account.save()

    start_sync(account)


def start_sync(account: ConnectedAccount) -> None:
    account.is_sync_running = True
    account.is_sync_completed = False
    account.save()
    sync_task.delay(account.id)
