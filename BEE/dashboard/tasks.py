from celery import shared_task
from common.logging import get_logger

logger = get_logger(__name__)


@shared_task
def periodic_task():
    from dashboard.models import IntegratedAccount
    from dashboard.utils import get_mails, get_all_read_emails, refresh_access_token
    from datetime import datetime

    try:
        integrated_accounts = IntegratedAccount.objects.all()
        logger.info("Starting to sync accounts")
        for account in integrated_accounts:
            if (
                not account.connected_account.is_sync_running
                and account.connected_account.is_sync_completed
            ):
                logger.info(f"Starting to sync account for {account}")
                access_token = refresh_access_token(account.connected_account)
                from_date = str(
                    datetime.now()
                    .replace(year=datetime.now().year - 2)
                    .strftime("%Y-%m-%dT%H:%M:%SZ")
                )
                job_date_time = datetime.now()
                get_mails(account.connected_account, from_date, access_token)
                get_all_read_emails(account.connected_account, access_token)
                account.connected_account.last_job_run = job_date_time
                account.connected_account.save()
                logger.info(f"Done syncing account for {account}")
            logger.info("Done syncing accounts")
        return True
    except Exception as e:
        logger.exception("An exception occured while synchronizing accounts")
        return False


@shared_task
def sync_task(account_id):
    from dashboard.models import ConnectedAccount
    from dashboard.utils import get_mails
    from datetime import datetime

    try:
        account = ConnectedAccount.objects.filter(id=account_id).first()
        if account:
            from_date = str(
                datetime.now()
                .replace(year=datetime.now().year - 2)
                .strftime("%Y-%m-%dT%H:%M:%SZ")
            )
            get_mails(account, from_date, account.access_token)
            account.is_sync_running = False
            account.is_sync_completed = True
            account.save()
            return True
        else:
            return False
    except Exception as error:
        account.is_sync_running = False
        account.is_sync_completed = True
        account.save()
        logger.exception("An exception occurred while starting to to sync account")
        return False
