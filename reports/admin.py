from django.contrib import admin
from django.urls import path
from django.contrib.admin import AdminSite
from inventory.models import Sales  # ✅ Import Sales correctly
from .views import sales_report, inventory_report

class ReportsAdminSite(AdminSite):
    """✅ Custom Admin Site for Reports"""

    site_header = "TopTown Clothing - Reports"
    site_title = "Warehouse Reports"
    index_title = "Reports Dashboard"

    def has_permission(self, request):
        """✅ Only users with 'view_reports' permission can access"""
        return request.user.is_active and request.user.has_perm("reports.view_reports")

    def get_urls(self):
        """✅ Custom URLs for Reports"""
        urls = super().get_urls()
        custom_urls = [
            path("sales/", self.admin_view(sales_report), name="admin_sales_report"),
            path("inventory/", self.admin_view(inventory_report), name="admin_inventory_report"),
        ]
        return custom_urls + urls

reports_admin = ReportsAdminSite(name="reports_admin")

class SalesAdmin(admin.ModelAdmin):
    """✅ Admin Panel Customization for Sales with Currency Formatting"""

    list_display = (
        "date_recorded", "shop", "till_number", "cashier",
        "formatted_z_reading", "formatted_eftpos_sales",
        "formatted_overing", "formatted_down", "formatted_cash_sales", "recorded_by"
    )

    readonly_fields = ("formatted_cash_sales", "time_recorded")

    # ✅ Format Fields with Currency (PGK)
    def formatted_z_reading(self, obj):
        return f"K{obj.z_reading:,.2f}"
    formatted_z_reading.short_description = "Z Reading"

    def formatted_eftpos_sales(self, obj):
        return f"K{obj.eftpos_sales:,.2f}"
    formatted_eftpos_sales.short_description = "EFTPOS Sales"

    def formatted_overing(self, obj):
        return f"K{obj.overing:,.2f}"
    formatted_overing.short_description = "Overing"

    def formatted_down(self, obj):
        return f"K{obj.down:,.2f}"
    formatted_down.short_description = "Down"

    def formatted_cash_sales(self, obj):
        """✅ Formats Cash Sales as Currency"""
        return f"K{obj.cash_sales:,.2f}"
    formatted_cash_sales.short_description = "Cash Sales"

# ✅ Register Sales Only If Not Already Registered
if not admin.site.is_registered(Sales):
    admin.site.register(Sales, SalesAdmin)
