from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from .views import sales_report, inventory_report  # ✅ Import correct views

class ReportsAdminSite(AdminSite):
    site_header = "TopTown Clothing - Reports"
    site_title = "Warehouse Reports"
    index_title = "Reports Dashboard"

    def has_permission(self, request):
        """✅ Allow only users with 'view_reports' permission to access"""
        return request.user.is_active and request.user.has_perm("reports.view_reports")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("sales/", self.admin_view(sales_report), name="admin_sales_report"),
            path("inventory/", self.admin_view(inventory_report), name="admin_inventory_report"),
        ]
        return custom_urls + urls

reports_admin = ReportsAdminSite(name="reports_admin")
