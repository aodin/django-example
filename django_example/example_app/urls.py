from django.urls import path
from . import views


app_name = "items"  # Required for namedspaced URLs

urlpatterns = [
    path("", views.ItemList.as_view(), name="list"),
    path("create", views.CreateItem.as_view(), name="create"),
]
