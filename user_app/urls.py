from django.urls import path

from user_app.views import LoginAPIView, RegistrationAPIView

app_name = 'users'

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('signup', RegistrationAPIView.as_view(), name='signup'),
]
