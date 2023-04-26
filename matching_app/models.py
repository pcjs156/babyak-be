from django.db import models


class Matching(models.Model):
    starts_at = models.DateTimeField(verbose_name='모임 시작 일시')
    join_deadline = models.DateTimeField(verbose_name='인원 모집 마각 일시')
    place = models.CharField(max_length=30, verbose_name='모임 장소')
    category = models.CharField(max_length=30, verbose_name='모임 유형')
    description = models.TextField(blank=True, default='', verbose_name='추가 정보')
    people_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='최대 인원')
    joined_members = models.ManyToManyField('user_app.User', related_name='joined_matchings', verbose_name='참여 유저')
