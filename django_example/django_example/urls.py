from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Since there is only one app, we'll attach its URLs to the root
    path("", include("example_app.urls", namespace="items")),
    path("admin/", admin.site.urls),
]
