from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise AuthenticationFailed
        else:
            login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except IntegrityError:
            body = {
                'message': '해당 username은 이미 사용중입니다.'
            }
            return Response(body, status=status.HTTP_409_CONFLICT)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    def post(self, request: Request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class RetrieveMeAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(data=serializer.data)
