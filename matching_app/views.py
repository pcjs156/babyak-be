from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from matching_app.serializers import MatchingCreateSerializer, MatchingSerializer

from .models import Matching


class MatchingCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = MatchingCreateSerializer
    response_serializer = MatchingSerializer

    def post(self, request: Request):
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['host'] = request.user

        matching = Matching.objects.create(**data)
        matching.joined_members.add(request.user)
        matching.save()
        response = self.response_serializer(matching)

        return Response(response.data, status=status.HTTP_201_CREATED)
