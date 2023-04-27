from django.contrib import admin
from django.urls import path, include

from . import views

apiurlpatterns = [
    path('', views.server_check, name='server-check'),
    path('users/', include('user_app.urls')),
    path('matchings/', include('matching_app.urls')),
]

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/', include(apiurlpatterns)),
]
