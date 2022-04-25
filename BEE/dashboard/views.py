from multiprocessing.dummy import JoinableQueue
from rest_framework.decorators import api_view
import logging
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
from main.settings import SCOPE
from dashboard.models import ConnectedAccount, IntegratedAccount
from dashboard.utils import (
    calculate_no_of_unreads,
    calculate_avg_read_time,
    calculate_response_time,
    calculate_send_ratio,
    count_today_emails,
    get_token_from_cache,
    microsoft_graph_call,
    build_auth_url,
    load_cache,
    build_msal_app,
    save_cache,
    refresh_access_token,
)
from dashboard.tasks import sync_task

logging.getLogger("msal").setLevel(logging.WARN)

@api_view(['get'])
def index(request):
    
    if not request.user.is_authenticated:
        response = {
            'status': "error",
            'error': "401: Not authorized"
        }
        return JsonResponse(response, status=401)
    else:
        account = OutlookGet(request)
        data = {
            "account": account.email,
            "unreads": calculate_no_of_unreads(account),
            "avg_read_time": calculate_avg_read_time(account),
            "response_time": calculate_response_time(account),
            "send_ratio": calculate_send_ratio(account),
            "today_emails": count_today_emails(account),
        }
        return JsonResponse(data=data)


def connect(request):
    session = request.session

    id_token_claims = get_token_from_cache(session, SCOPE)
    if id_token_claims:
        access_token = id_token_claims.get("access_token")

        if access_token:
            graph_response = microsoft_graph_call(access_token)

            if graph_response.get("error"):
                return redirect("/")

            else:
                OutlookConnect(request, graph_response)
                return redirect("/")

        else:
            session["state"] = str(uuid.uuid4())
            auth_url = build_auth_url(scopes=SCOPE, state=session["state"])
            resp = redirect(auth_url)
            return resp
    else:
        session["state"] = str(uuid.uuid4())
        auth_url = build_auth_url(scopes=SCOPE, state=session["state"])
        resp = redirect(auth_url)
        return resp


def disconnect(request):
    session = request.session
    OutlookDisconnect(request)
    session["token_cache"] = None
    session["state"] = None
    session["user"] = None
    return redirect("/")


def logout(request):
    session = request.session
    session.clear()
    return redirect("/")


def get_token(request):
    session = request.session

    # If states don't match login again
    if request.GET.get("state") != session.get("state"):
        return redirect("/")

    # Authentication/Authorization failure
    if "error" in request.GET:
        return redirect("/")

    if request.GET.get("code"):
        cache = load_cache(session)
        result = build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.GET["code"],
            # Misspelled scope would cause an HTTP 400 error here
            scopes=SCOPE,
            redirect_uri="/",
        )

        if "error" in result:
            return redirect("/")
        else:
            access_token = result["access_token"]
            refresh_token = result["refresh_token"]
            session["user"] = result.get("id_token_claims")
            save_cache(session, cache)

            # Get user details using microsoft graph api call
            graph_response = microsoft_graph_call(access_token)
            print(graph_response)
            OutlookConnect(request, graph_response, refresh_token)

    else:
        return redirect("/")

    return redirect("/")


def OutlookConnect(request, data, refresh_token=None):
    account = ConnectedAccount.objects.filter(
        user=request.user, email=request.session["user"]["email"]
    ).first()
    if account:
        integrated_account = IntegratedAccount.objects.filter(
            user=request.user, connected_account=account
        ).first()
        if integrated_account:
            return
        else:
            IntegratedAccount.objects.create(
                user=request.user, connected_account=account
            )
            account.access_token = data["AccessToken"]
            account.access_token_expire_date = datetime.now()
            account.refresh_token = refresh_token

            account.save()

    else:
        account = ConnectedAccount.objects.create(
            user=request.user,
            email=request.session["user"]["email"],
            access_token=data["AccessToken"],
            access_token_expire_date=datetime.now(),
            refresh_token=refresh_token,
        )
        IntegratedAccount.objects.create(user=request.user, connected_account=account)
    # refresh_access_token(account.id)
    start_sync(account)
    return True


def OutlookDisconnect(request):
    account = OutlookGet(request)
    integrated_account = IntegratedAccount.objects.filter(
        user=request.user, connected_account=account
    ).first()
    if integrated_account:
        integrated_account.delete()
    return True


def OutlookGet(request):
    integrated_account = IntegratedAccount.objects.filter(user=request.user).first()
    if integrated_account:
        return integrated_account.connected_account
    return None


def get_emails(request):
    account = OutlookGet(request)
    access_token = refresh_access_token(account)
    print(access_token)
    return redirect("/")


def start_sync(account):
    account.is_sync_running = True
    account.is_sync_completed = False
    account.save()
    task_id = sync_task.delay(account.id)
    print(task_id)
