from django.urls import path
from django.contrib.auth import views as auth_views

from user_app.views import LoginAPIView, RegistrationAPIView, LogoutAPIView

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
