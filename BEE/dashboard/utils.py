import datetime
import uuid
from datetime import datetime
import msal
import requests
import pytz
from dateutil.parser import parse
from django.db.models import Avg
from main.settings import (
    REDIRECT_URI,
    CLIENT_ID,
    AUTHORITY,
    CLIENT_SECRET,
    GRAPH_ENDPOINT,
    SCOPE,
)
from dashboard.models import (
    AccountIncomingMailStats,
    AccountOutgoingMailStats,
    ConnectedAccount,
)
from common.logging import get_logger

logger = get_logger(__name__)

TIME_ZONE = pytz.timezone("Africa/Nairobi")


def load_cache(session):
    """loads from msal cache"""
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def save_cache(session, cache):
    """saves to msal cache"""
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def build_msal_app(cache=None, authority=None):
    """builds msal cache"""
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority or AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=cache,
    )


def build_auth_url(authority=None, scopes=None, state=None):
    """builds auth url per tenantid"""
    return build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [], state=state or str(uuid.uuid4()), redirect_uri=REDIRECT_URI
    )


def get_token_from_cache(session, scope):
    """get accesstoken from cache"""
    # This web app maintains one cache per session
    cache = load_cache(session)
    cca = build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    # So all account(s) belong to the current signed-in user
    if accounts:
        result = cca.acquire_token_silent(scope, account=accounts[0])
        save_cache(session, cache)
        return result


def microsoft_graph_call(access_token):
    """graph api to microsoft"""
    # Use token to call downstream service
    # graph_data = requests.get(
    #     url='https://graph.microsoft.com/v1.0//me/messages' + '?$search="isRead:true"&$top="1000"$count=true',
    #     headers={'Authorization': 'Bearer ' + access_token},
    #     ).json()

    graph_data = requests.get(
        url=GRAPH_ENDPOINT,
        headers={"Authorization": "Bearer " + access_token},
    ).json()

    if "error" not in graph_data:
        return {
            "Login": "success",
            "UserId": graph_data.get("id"),
            "UserName": graph_data.get("displayName"),
            "AccessToken": access_token,
        }

    else:
        return {"error": graph_data}


def get_mails_api(access_token, url):
    """graph api to microsoft"""
    # Use token to call downstream service
    graph_data = requests.get(
        url=url,
        headers={"Authorization": "Bearer " + access_token},
    ).json()
    logger.info("Returning mails response")
    return graph_data


def get_mails(account, to_date, access_token):
    from_date = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    if account:
        url = (
            "https://graph.microsoft.com/v1.0/me/mailFolders/sentitems/messages?"
            "$filter=((sentDateTime le "
            + to_date
            + ") and (sentDateTime ge "
            + from_date
            + "))&$select=id,conversationId,sentDateTime&$top=999&$orderby=sentDateTime"
        )

        while url is not None:
            sent_emails = get_mails_api(access_token, url)
            if "error" in sent_emails:
                return False
            for email in sent_emails["value"]:
                mail = AccountOutgoingMailStats.objects.filter(
                    account=account, message_id=email["id"]
                ).first()
                if not mail:
                    outgoing_mail = AccountOutgoingMailStats.objects.create(
                        account=account,
                        message_id=email["id"],
                        conversation_id=email["conversationId"],
                        sent_date_time=email["sentDateTime"],
                    )
                    matching_incoming_mail = AccountIncomingMailStats.objects.filter(
                        account=account, conversation_id=email["conversationId"]
                    ).first()
                    if matching_incoming_mail:
                        time_diff = (
                            matching_incoming_mail.sent_date_time
                            - outgoing_mail.sent_date_time
                        )
                        res_time = int(time_diff.total_seconds())
                        outgoing_mail.response_time = res_time
                        outgoing_mail.save()
            url = (
                sent_emails["@odata.nextLink"]
                if "@odata.nextLink" in sent_emails
                else None
            )

        url = (
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?"
            "$filter=((receivedDateTime le "
            + to_date
            + ") and (receivedDateTime ge "
            + from_date
            + "))&$expand=SingleValueExtendedProperties($filter=(Id%20eq%20'Integer%200x1081'))"
            "&$top=999&$orderby=receivedDateTime"
        )

        while url is not None:
            inbox_emails = get_mails_api(access_token, url)
            if "error" in inbox_emails:
                return False
            for email in inbox_emails["value"]:
                mail = AccountIncomingMailStats.objects.filter(
                    account=account, message_id=email["id"]
                ).first()
                if not mail:
                    mail = AccountIncomingMailStats.objects.create(
                        account=account,
                        message_id=email["id"],
                        conversation_id=email["conversationId"],
                        sent_date_time=email["receivedDateTime"],
                        is_read=email["isRead"],
                        is_read_date_time=datetime.now(tz=TIME_ZONE)
                        if email["isRead"]
                        else None,
                        read_time_taken=0 if email["isRead"] else None,
                    )
                else:
                    if not mail.is_read and email["isRead"]:
                        mail.is_read_date_time = datetime.now(tz=TIME_ZONE)

                        time_format = "%Y-%d-%m %H:%M:%S"
                        receive_date_time = datetime.strptime(
                            mail.sent_date_time.strftime("%Y-%d-%m %H:%M:%S"),
                            time_format,
                        )
                        read_date_time = datetime.strptime(
                            mail.is_read_date_time.strftime("%Y-%d-%m %H:%M:%S"),
                            time_format,
                        )
                        mail.read_time_taken = int(
                            (read_date_time - receive_date_time).seconds / 60
                        )
                        mail.save()
                    if not email["isRead"]:
                        mail.is_read_date_time = None
                    mail.is_read = email["isRead"]
                    mail.save()

                if "singleValueExtendedProperties@odata.context" in email:
                    # #message_id = re.search("messages(\'(.*)')/singleValueExtendedProperties", email['singleValueExtendedProperties@odata.context'])
                    # start = email['singleValueExtendedProperties@odata.context'].find("messages(\'")
                    # end = email['singleValueExtendedProperties@odata.context'].find("')/singleValueExtendedProperties")
                    # if start!= -1 and end!= -1:
                    #     message_id = email['singleValueExtendedProperties@odata.context'][start+9:end]
                    associated_sent_mails = AccountOutgoingMailStats.objects.filter(
                        account=account,
                        conversation_id=mail.conversation_id,
                        sent_date_time__gt=parse(email["sentDateTime"]),
                    )
                    for associated_sent_mail in associated_sent_mails:
                        associated_sent_mail.inbox_email = mail
                        time_format = "%Y-%d-%m %H:%M:%S"
                        sent_date_time = datetime.strptime(
                            parse(email["sentDateTime"]).strftime("%Y-%d-%m %H:%M:%S"),
                            time_format,
                        )
                        response_date_time = datetime.strptime(
                            associated_sent_mail.sent_date_time.strftime(
                                "%Y-%d-%m %H:%M:%S"
                            ),
                            time_format,
                        )
                        associated_sent_mail.response_time = int(
                            (response_date_time - sent_date_time).total_seconds() / 60
                        )
                        associated_sent_mail.save()
                    if mail.is_read_date_time is None and email["isRead"]:
                        mail.is_read = True
                        mail.is_read_date_time = datetime.now(tz=TIME_ZONE)
                        mail.save()
            url = (
                inbox_emails["@odata.nextLink"]
                if "@odata.nextLink" in inbox_emails
                else None
            )


def get_all_read_emails(account, access_token):
    if account:
        url = (
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?"
            "$filter=isRead eq true&$top=999"
        )
        while url is not None:
            unread_emails = get_mails_api(access_token, url)
            if "error" in unread_emails:
                return False
            for email in unread_emails["value"]:
                mail = AccountIncomingMailStats.objects.filter(
                    account=account, message_id=email["id"], is_read=False
                ).first()
                if mail:
                    mail.is_read = True
                    mail.is_read_date_time = datetime.now(tz=TIME_ZONE)
                    mail.save()
            url = (
                unread_emails["@odata.nextLink"]
                if "@odata.nextLink" in unread_emails
                else None
            )
    return True


def calculate_no_of_unreads(account):
    if account:
        return AccountIncomingMailStats.objects.filter(
            connected_account=account, is_read=False
        ).count()
    else:
        return None


def calculate_avg_read_time(account):
    if account:
        avg = AccountIncomingMailStats.objects.filter(
            connected_account=account, read_time_taken__isnull=False
        ).aggregate(Avg("read_time_taken"))["read_time_taken__avg"]
        if avg is not None:
            hours = int(avg / 60)
            minutes = avg % 60
            return "%dh %.fm" % (hours, minutes)
    return None


def calculate_response_time(account):
    if account:
        avg = AccountOutgoingMailStats.objects.filter(
            connected_account=account, response_time__isnull=False
        ).aggregate(Avg("response_time"))["response_time__avg"]
        if avg is not None:
            minutes = int(avg / 60)
            hours = minutes % 60
            return "%dh %.fm" % (hours, minutes)
    return None


def calculate_send_ratio(account):
    if account:
        receive_count = AccountIncomingMailStats.objects.filter(connected_account=account).count()
        response_count = AccountOutgoingMailStats.objects.filter(
            connected_account=account
        ).count()
        if receive_count > 0:
            avg = response_count / receive_count
            return float("{:.2f}".format(avg))
        return 0
    return None


def count_today_emails(account):
    if account:
        return AccountIncomingMailStats.objects.filter(
            sent_date_time__month=datetime.now().month,
            sent_date_time__year=datetime.now().year,
            sent_date_time__day=datetime.now().day,
            connected_account=account,
        ).count()
    return None


def refresh_access_token(account):
    time_format = "%Y-%d-%m %H:%M:%S"
    initial_time = datetime.strptime(
        account.access_token_expire_date.strftime("%Y-%d-%m %H:%M:%S"), time_format
    )
    current_time = datetime.strptime(
        datetime.now().strftime("%Y-%d-%m %H:%M:%S"), time_format
    )
    expire_time = int((current_time - initial_time).total_seconds() / 60)
    if expire_time > 59:
        result = build_msal_app(cache=None).acquire_token_by_refresh_token(
            refresh_token=account.refresh_token,
            # Misspelled scope would cause an HTTP 400 error here
            scopes=SCOPE,
        )
        account.access_token = result["access_token"]
        account.refresh_token = result["refresh_token"]
        account.access_token_expire_date = datetime.now()
        account.save()
    return account.access_token
