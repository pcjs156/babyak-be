from django.urls import path
from django.contrib.auth import views as auth_views

from user_app.views import LoginAPIView

app_name = 'users'

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name='login'),
]
