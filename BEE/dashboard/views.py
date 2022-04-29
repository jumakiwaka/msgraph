from rest_framework.decorators import api_view
import logging
from django.http import JsonResponse
from dashboard.utils import (
    calculate_no_of_unreads,
    calculate_avg_read_time,
    calculate_response_time,
    calculate_send_ratio,
    count_today_emails,
    count_all_mails,
)
from dashboard.selectors import get_user_account
from common.wrappers.response_wrapper import ResponseWrapper

logging.getLogger("msal").setLevel(logging.WARN)


@api_view(["get"])
def summary(request):

    if not request.user.is_authenticated:
        response = {"status": "error", "error": "401: Not authorized"}
        return JsonResponse(response, status=401)
    else:
        account = get_user_account(user=request.user)
        if account:
            data = {
                "account": account.email,
                "unreads": calculate_no_of_unreads(account),
                "avg_read_time": calculate_avg_read_time(account),
                "response_time": calculate_response_time(account),
                "send_ratio": calculate_send_ratio(account),
                "today_emails": count_today_emails(account),
                "all_mails": count_all_mails(account),
            }
            response = ResponseWrapper(
                status_code=200,
                message="dashboard summary retrieval success",
                result=data,
            ).success
            return JsonResponse(response, status=response.get("status_code"))
        else:
            response = ResponseWrapper(
                status_code=404, error="user account not found"
            ).fail
            return JsonResponse(response, status=response.get("status_code"))
