from django.urls import path

from . import views

app_name = 'matchings'

urlpatterns = [
    path('', views.MatchingCreateAPIView.as_view(), name='create'),
]
