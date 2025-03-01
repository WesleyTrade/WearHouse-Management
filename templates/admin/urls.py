from django.urls import path
from .views import sales_report, inventory_report

urlpatterns = [
    path("sales/", sales_report, name="sales_report"),
    path("inventory/", inventory_report, name="inventory_report"),
]
