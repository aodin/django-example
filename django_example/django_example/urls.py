"""
django_example URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Example.as_view(), name='example'),
    path('app/', include('app.urls')),
]
