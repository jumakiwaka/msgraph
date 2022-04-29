from os import access
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from dashboard.utils import refresh_access_token
from dashboard.services import integrate_account
from auth.services import create_update_user, create_update_user_token
from dashboard.utils import build_msal_app, get_graph_user
from dashboard.selectors import get_user_account
from main.settings import SCOPE, REDIRECT_URI
from common.wrappers.response_wrapper import ResponseWrapper


class LoginAPIVIEW(GenericAPIView):
    permission_classes = [AllowAny]

    @classmethod
    def post(cls, request):
        data = request.data

        if "error" in request.GET:
            status_code = 400
            response = ResponseWrapper(
                status_code=status_code, error="could not get code from msal"
            ).fail
            return JsonResponse(response, status=status_code)

        if data.get("code"):
            result = build_msal_app().acquire_token_by_authorization_code(
                data.get("code"),
                scopes=SCOPE,
                redirect_uri=REDIRECT_URI,
            )

            if "error" in result:
                status_code = 400
                response = ResponseWrapper(
                    status_code=status_code, error=result.get("error_description")
                ).fail
                return JsonResponse(response, status=status_code)
            else:
                access_token = result["access_token"]
                expires_in = result["expires_in"]
                refresh_token = result["refresh_token"]

                # Get user details using microsoft graph api call
                ms_user_data = get_graph_user(access_token)
                user = create_update_user(ms_user_data)
                connect_success = integrate_account(
                    user, access_token, expires_in, refresh_token
                )
                user_token = create_update_user_token(user=user)

                result = {"key": user_token.key, "user_profile": ms_user_data}
                status_code = 200
                response = ResponseWrapper(
                    status_code=status_code, message="Login success", result=result
                ).success

                return JsonResponse(response, status=status_code)

        else:
            response = {"status": "error", "error": "no code provided"}
            status_code = 400
            response = ResponseWrapper(
                status_code=status_code, error="No code provided"
            ).fail
            return JsonResponse(response, status=status_code)



class AuthStatusAPIView(GenericAPIView):

    @classmethod
    def get(cls, request):
        # by this point the drf token is valid, now we need to validate if ms token is still valid as well.
        user = request.user
        connected_account = get_user_account(user=user)
        if connected_account:
            access_token = refresh_access_token(account=connected_account)
            result = bool(access_token)

            response = ResponseWrapper(status_code=200, result=result, message='auth status check success').success

            return JsonResponse(response, status=response.get("status_code"))

        else:
            response = ResponseWrapper(status_code=401, error="user not connected").fail
            return JsonResponse(response, status=response.get("status_code"))

class LogoutAPIView(GenericAPIView):
    @classmethod
    def post(cls, request):

        data = request.data

        return data
