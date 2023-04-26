from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Matching


class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'


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
