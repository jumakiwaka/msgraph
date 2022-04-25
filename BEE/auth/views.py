from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from dashboard.models import ConnectedAccount, IntegratedAccount



class LoginAPIVIEW(GenericAPIView):
    permission_classes = [AllowAny]

    @classmethod
    def post(cls, request):
        data = request.data

        access_token = data.get("accessToken")
        expires_on = data.get("expiresOn")
        account = data.get("account")
        username = account.get("userName")
        name = account.get("name")
        fname, lname = name.split(" ")

        user, created = User.objects.get_or_create(
            username=username,
        )

        user.first_name = fname
        user.last_name = lname
        user.email = username
        user.save()

        connected_account, created = ConnectedAccount.objects.get_or_create(
            user=user
        )
        connected_account.email = username
        connected_account.access_token = access_token
        connected_account.access_token_exp_date = expires_on
        connected_account.save()

        integrated_account, created = IntegratedAccount.objects.get_or_create(user=user, connected_account=connected_account)

        user_token, created = Token.objects.get_or_create(user=user)

        response = {
            "token": user_token.key
        }


        return JsonResponse(response)




class LogoutAPIView(GenericAPIView):

    @classmethod
    def post(cls, request):

        data = request.data


        return data


