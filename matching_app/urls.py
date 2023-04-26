from django.urls import path

from . import views

app_name = 'matchings'

urlpatterns = [
    path('', views.MatchingCreateAPIView.as_view(), name='create'),
    path('<int:matching_id>/join', views.MatchingJoinAPIView.as_view(), name='join'),
    path('<int:matching_id>/leave', views.MatchingLeaveAPIView.as_view(), name='leave'),
]
