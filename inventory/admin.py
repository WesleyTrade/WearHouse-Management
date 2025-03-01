from django.contrib import admin
from inventory.models import Sales
from inventory.forms import SalesForm
from django import forms
from inventory.models import Sales, Shop, Product, Inventory

# ✅ Custom Form for Sales to enforce numeric input
class SalesForm(forms.ModelForm):
    """Ensure numeric fields only accept numbers"""

    class Meta:
        model = Sales
        fields = "__all__"

    def clean_numeric_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value is None:
            return 0.00  # ✅ Default value for empty fields
        try:
            return float(value)
        except ValueError:
            raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} must be a numeric value.")

    def clean_z_reading(self):
        return self.clean_numeric_field("z_reading")

    def clean_eftpos_sales(self):
        return self.clean_numeric_field("eftpos_sales")

    def clean_overing(self):
        return self.clean_numeric_field("overing")

    def clean_down(self):
        return self.clean_numeric_field("down")


# ✅ Admin Panel for Sales Records
@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    """✅ Admin Panel for Sales Records"""
    form = SalesForm
    list_display = (
        "shop", "date_recorded", "till_number", "cashier",
        "assistant_supervisor", "z_reading", "eftpos_sales",
        "overing", "down", "memo", "time_recorded", "cash_sales", "recorded_by"
    )
    list_filter = ("shop", "date_recorded")
    search_fields = ("shop__name", "cashier", "assistant_supervisor", "recorded_by__username")
    date_hierarchy = "date_recorded"
    readonly_fields = ("time_recorded", "cash_sales", "recorded_by")

    def save_model(self, request, obj, form, change):
        """✅ Automatically set recorded_by & calculate cash sales before saving"""
        obj.cash_sales = obj.z_reading - obj.eftpos_sales + obj.overing - obj.down
        if not obj.pk:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)

# ✅ Shop Admin Panel (FIXED list_display)
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name",)  # ✅ Removed 'location' field
    search_fields = ("name",)


# ✅ Product Admin Panel
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "supplier")
    search_fields = ("name", "category", "supplier__name")


# ✅ Inventory Admin Panel
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "shop", "quantities", "amount", "date_added", "created_by")
    list_filter = ("shop", "date_added")
    search_fields = ("product__name", "shop__name")
