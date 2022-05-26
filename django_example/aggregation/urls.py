from django.urls import path

from . import views


urlpatterns = [
    path(
        "purchases",
        views.Purchases.as_view(),
        name="aggregation.purchases",
    ),
    path(
        "monthly",
        views.MonthlyTotals.as_view(),
        name="aggregation.monthly",
    ),
]
