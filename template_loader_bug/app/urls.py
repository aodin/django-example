from django.urls import path

from . import views


urlpatterns = [
    path('', views.AppExample.as_view(), name='app.example'),
]
