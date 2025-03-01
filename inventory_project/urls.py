
from django.contrib import admin
from django.urls import path, include
from reports.admin import reports_admin  # ✅ Import reports_admin

urlpatterns = [
    path("admin/", admin.site.urls),  # ✅ Default Django Admin
    path("reports/", include("reports.urls")),  # ✅ Reports module
    path("reports-admin/", reports_admin.urls),  # ✅ Unique admin site for reports
]

