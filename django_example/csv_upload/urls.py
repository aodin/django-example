from django.urls import path
from . import views


app_name = "csv"  # Required for namespaced URLs

urlpatterns = [
    path("", views.ItemList.as_view(), name="list"),
    path("upload", views.UploadView.as_view(), name="upload"),
    path("create", views.CreateView.as_view(), name="create"),
    path("speed", views.SpeedView.as_view(), name="speed"),
]
