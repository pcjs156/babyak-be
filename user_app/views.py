from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import LoginSerializer


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
