from random import choice

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.generics import RetrieveDestroyAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matching_app.serializers import MatchingSerializer
from .models import Matching


class MatchingListMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)

        # 필터링 처리
        status = request.query_params.get('status', '모집 완료')
        status = set(map(str.strip, status.split(',')))
        resp.data = list(filter(lambda x: x['status'] in status, resp.data))

        # 정렬 처리
        order_by = request.query_params.get('order-by', 'starts_at')
        order_direction = request.query_params.get('order-direction', 'asc')

        resp.data = sorted(resp.data, key=lambda x: x[order_by], reverse=order_direction.lower() == 'desc')

        return resp


class JoinedMatchingListMixin(MatchingListMixin):
    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)

        user = request.user
        resp.data = list(filter(lambda x: user.name in x['joined_members'], resp.data))

        return resp


class MatchingCreateMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        else:
            return super().create(request, *args, **kwargs)


class MatchingListCreateAPIView(MatchingListMixin, MatchingCreateMixin, GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class JoinedMatchingListAPIView(JoinedMatchingListMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer

    def get(self, request: Request, *args, **kwargs):
        resp = self.list(request, *args, **kwargs)
        return resp


class MatchingRetrieveDeleteAPIView(RetrieveDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer

    def get_serializer_context(self):
        ret = super().get_serializer_context()
        return ret

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        elif not Matching.objects.filter(id=kwargs['pk'], host=request.user).exists():
            raise PermissionDenied
        else:
            return super().destroy(request, *args, **kwargs)


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
        elif timezone.now() > matching.starts_at or \
                matching.people_limit is not None and matching.people_limit <= matching.joined_members.count():
            body = {'message': '마감된 모임입니다.'}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            matching.joined_members.add(request.user)
            matching.save()

        response = self.response_serializer(matching)

        return Response(response.data, status=status.HTTP_200_OK)


class MatchingLeaveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, matching_id: int):
        matching = get_object_or_404(Matching, id=matching_id)

        if request.user not in matching.joined_members.all():
            body = {'message': '해당 모임에 참여한 기록이 없습니다.'}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        elif timezone.now() > matching.starts_at:
            body = {'message': '이미 시작되었거나 끝난 모임에서 나올 수 없습니다.'}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        # 호스트인 경우
        if request.user == matching.host:
            # 호스트인데 나만 있는 경우 모임 삭제
            if matching.joined_members.count() == 1:
                matching.delete()
            # 호스트인데 나 말고 다른 사람이 있는 경우
            else:
                # 일단 호스트는 빠지고
                matching.joined_members.all(id=request.user.id).delete()
                # 나머지 중에서 새 호스트를 랜덤하게 찾음
                new_host = choice(matching.joined_members.all())
                matching.host = new_host
                matching.save()

        # 호스트가 아닌 경우
        else:
            # 일단 나는 빠지고
            matching.joined_members.filter(id=request.user.id).delete()
            # 남은 멤버가 없으면 모임 삭제
            if not matching.joined_members.exists():
                matching.delete()
            # 남은 멤버가 없으면 변경 내역 반영
            else:
                matching.save()

        return Response(status=status.HTTP_200_OK)
