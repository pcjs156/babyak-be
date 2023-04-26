from django.utils import timezone
from django.shortcuts import get_object_or_404

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


class MatchingJoinAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    response_serializer = MatchingSerializer

    def post(self, request: Request, matching_id: int):
        matching = get_object_or_404(Matching, id=matching_id)

        if matching.host == request.user:
            body = {'code': 1, 'message': '본인이 생성한 모임에 참가 신청할 수는 없습니다.'}
            return Response(body, status=status.HTTP_409_CONFLICT)
        elif request.user in matching.joined_members.all():
            body = {'code': 2, 'message': '이미 모임에 소속되어 있습니다.'}
            return Response(body, status=status.HTTP_409_CONFLICT)
        elif timezone.now() > matching.join_deadline or \
                matching.people_limit is not None and matching.people_limit <= matching.joined_members.count():
            body = {'message': '마감된 모임입니다.'}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            matching.joined_members.add(request.user)
            matching.save()

        response = self.response_serializer(matching)

        return Response(response.data, status=status.HTTP_200_OK)
