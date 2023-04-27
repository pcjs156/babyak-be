from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Matching


class MatchingSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

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
        join_deadline = timezone.datetime.strptime(rep.get('join_deadline'), '%Y-%m-%dT%H:%M:%S')

        people_limit = rep.get('people_limit')
        joined_members = rep.get('joined_members')

        # 모집 기한을 넘기지 않은 경우
        if now < join_deadline:
            # 인원 상한이 없는 경우
            if people_limit is None:
                rep['status'] = '모집중'
            # 인원 상한이 있는 경우
            else:
                # 인원 상한에 아직 도달하지 않은 경우
                if people_limit < len(joined_members):
                    rep['status'] = '모집중'
                else:
                    rep['status'] = '모집 완료'
        else:
            rep['status'] = '모집 완료'

        return rep


class MatchingCreateSerializer(serializers.Serializer):
    starts_at = serializers.DateTimeField()
    join_deadline = serializers.DateTimeField()
    place = serializers.CharField(max_length=30)
    category = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=100, default='', required=False)
    people_limit = serializers.IntegerField(min_value=2, required=False)

    def validate(self, data):
        starts_at = data.get('starts_at')
        join_deadline = data.get('join_deadline')
        place = data.get('place')
        category = data.get('category')
        description = data.get('description')
        people_limit = data.get('people_limit')

        # 모임 마감 시간이 모임 시작 시간보다 나중인 경우
        if starts_at < join_deadline:
            raise ValidationError('모임 마감 시간은 모임 시작보다 나중일 수 없습니다.')

        return {
            'starts_at': starts_at,
            'join_deadline': join_deadline,
            'place': place,
            'category': category,
            'description': description,
            'people_limit': people_limit,
        }
