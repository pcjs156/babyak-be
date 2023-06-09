from django.urls import path

from . import views

app_name = 'matchings'

urlpatterns = [
    path('', views.MatchingListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>', views.MatchingRetrieveDeleteAPIView.as_view(), name='retrieve-delete'),
    path('<int:matching_id>/join', views.MatchingJoinAPIView.as_view(), name='join'),
    path('<int:matching_id>/leave', views.MatchingLeaveAPIView.as_view(), name='leave'),
    path('me', views.JoinedMatchingListAPIView.as_view(), name='my-list'),
]