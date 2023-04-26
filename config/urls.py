from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.server_check, name='server-check'),
    path('users', include('user_app.urls')),
]
