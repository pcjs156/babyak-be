from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Matching


class MatchingSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    host = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    joined_members = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Matching
        fields = '__all__'
        read_only_fields = ['host', 'joined_members']

    def create(self, validated_data):
        requested_user = self.context.get('request').user

        # 요청자를 호스트로 설정
        matching = Matching(**validated_data)
        matching.host = requested_user
        matching.save()

        # 요청자를 멤버로 추가
        matching.joined_members.add(requested_user)
        matching.save()

        return matching

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        now = timezone.now()
        starts_at = timezone.datetime.strptime(rep.get('starts_at'), '%Y-%m-%dT%H:%M:%S')

        people_limit = rep.get('people_limit')
        joined_members = rep.get('joined_members')

        # 시작 시간이 지났으면 모집 완료
        if starts_at <= now:
            rep['status'] = '모집 완료'
        else:
            # 시작 시간까지 30분 미만 남았으면
            if starts_at - now < timezone.timedelta(minutes=30):
                rep['status'] = '마감 임박'
            # 인원 상한이 있으면
            elif people_limit is not None:
                # 인원 상한을 넘기지 않은 경우 모집중
                if people_limit > len(joined_members):
                    rep['status'] = '모집중'
                # 인원 상한을 넘긴 경우 모집 완료
                else:
                    rep['status'] = '모집 완료'
            # 인원 상한이 없으면
            else:
                rep['status'] = '모집중'

        return rep


class MatchingCreateSerializer(serializers.Serializer):
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
    place = serializers.CharField(max_length=30)
    category = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=100, default='', required=False)
    people_limit = serializers.IntegerField(min_value=2, required=False)

    def validate(self, data):
        starts_at = data.get('starts_at')
        ends_at = data.get('ends_at')
        place = data.get('place')
        category = data.get('category')
        description = data.get('description')
        people_limit = data.get('people_limit')

        # 모임 시작 시간이 모임 종료 시간보다 나중인 경우
        if starts_at >= ends_at:
            raise ValidationError('모임 마감 시간은 모임 시작보다 나중일 수 없습니다.')

        return {
            'starts_at': starts_at,
            'ends_at': ends_at,
            'place': place,
            'category': category,
            'description': description,
            'people_limit': people_limit,
        }
