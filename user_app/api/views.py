from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# from user_app import models


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Succesful!"
            data['username'] = account.username
            data['email'] = account.email
            # poniższa część jest używana razem z rest_framework.authentication.TokenAuthentication
            token = Token.objects.get(user=account).key  # można użyć tutaj  metody get_or_create()
            data['token'] = token

            # poniższa część przy użyciu metody JWT (creating token manyally)
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
        else:
            data = serializer.errors
        return Response(data, status.HTTP_201_CREATED)


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()  # usuwamy token
        return Response(status=status.HTTP_200_OK)
