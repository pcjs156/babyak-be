from django.urls import path

from user_app import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('signup/', views.RegistrationAPIView.as_view(), name='signup'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('me', views.RetrieveMeAPIView.as_view(), name='retrieve-me'),
    path('<int:pk>', views.UserRetrieveAPIView.as_view(), name='retrieve'),
]
