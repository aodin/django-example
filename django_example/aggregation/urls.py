from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.MonthlyTotals.as_view(),
        name="aggregation.monthly",
    ),
]
