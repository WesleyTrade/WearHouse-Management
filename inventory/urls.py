
from django.urls import path
from .views import home, generate_report  # ✅ Import home page view

urlpatterns = [
    path("", home, name="home"),  # ✅ Home page URL
    path("reports/sales/", generate_report, name="sales_report"),  # ✅ Sales report route
]

