from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from .tasks import send_confirmation_email


User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )


class RegistrationCustomerView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but trouble with email',
                                 'data': serializer.data}, status=201)

        return Response(serializer.data, status=201)


class ActivationEmailView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activate', status=200)
