from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from reports.admin import reports_admin  # ✅ Import reports_admin

def homepage(request):
    return render(request, "homepage.html")  # Make sure to create this template!

urlpatterns = [
    path("", homepage, name="homepage"),  # This handles the root URL (/)
    path("admin/", admin.site.urls),
    path("reports/", include("reports.urls")),  # Ensure your reports app is included
    path("reports-admin/", reports_admin.urls),  # ✅ Add custom reports admin panel
]

