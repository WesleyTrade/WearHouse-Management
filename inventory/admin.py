from django.contrib import admin
from inventory.models import Sales, Inventory, Product, Shop 
from .models import Product, Inventory  # ✅ Import models
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

class SalesResource(ModelResource):
    class Meta:
        model = Sales

# ✅ Register Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "supplier", "unit_price", "rate_per_bale")
    search_fields = ("name", "category", "supplier__name")
    list_filter = ("category", "supplier")

# ✅ Register Inventory
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("shop", "product", "quantities", "amount", "bale_number", "date_added")
    search_fields = ("shop__name", "product__name")
    list_filter = ("shop", "date_added")

@admin.register(Sales)
class SalesAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SalesResource
    """✅ Custom Admin View for Sales with Currency Formatting"""

    list_display = (
        "date_recorded", "shop", "till_number", "cashier",
        "formatted_z_reading", "formatted_eftpos_sales",
        "formatted_overing", "formatted_down", "formatted_cash_sales", "recorded_by"
    )

    search_fields = ("shop__name", "date_recorded")
    list_filter = ("shop", "date_recorded")
    readonly_fields = ("formatted_cash_sales", "time_recorded")

    # ✅ Format currency fields in Admin Panel
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
        return f"K{obj.cash_sales:,.2f}"
    formatted_cash_sales.short_description = "Cash Sales"


admin.site.register(Shop)
