from django.urls import path
from .views import generate_report

urlpatterns = [
    path('reports/sales/', generate_report, name="sales_report"),  # ✅ Add correct API route
]


