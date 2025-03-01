from django.db.models import Sum, F
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Shop, Supplier, Product, Inventory, Sales

# ✅ **Homepage View to Fix 404 Error**
def home_view(request):
    return HttpResponse("<h1>Welcome to WearHouse Inventory System</h1>")

# 📌 **Helper function to filter by timeframe**
def get_timeframe_filter(timeframe):
    today = now().date()

    if timeframe == "daily":
        return {"date_recorded": today}  # ✅ Fixed: Used `date_recorded` instead of `date_added`
    elif timeframe == "weekly":
        start_week = today - timedelta(days=today.weekday())
        return {"date_recorded__gte": start_week}
    elif timeframe == "monthly":
        return {"date_recorded__month": today.month, "date_recorded__year": today.year}
    elif timeframe == "yearly":
        return {"date_recorded__year": today.year}
    else:
        return {}

def add_sales(request):
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.recorded_by = request.user  # ✅ Automatically records the user
            sale.date_recorded = now().date()  # ✅ Automatically set today's date
            sale.cash_sales = sale.z_reading + sale.eftpos_sales + sale.overing - sale.down  # ✅ Corrected calculation
            sale.save()
            return redirect("sales_list")  # Redirect to a sales listing page

    else:
        form = SalesForm()

    return render(request, "sales/add_sales.html", {"form": form})

# 📌 **API View: Get Inventory List**
class InventoryListView(View):
    def get(self, request):
        inventories = Inventory.objects.all().values(
            "id", "shop__name", "product__name", "bale_number", "quantities", "amount", "date_added"
        )
        return JsonResponse({"inventories": list(inventories)}, safe=False)

# 📌 **API View: Get Inventory Detail**
class InventoryDetailView(View):
    def get(self, request, inventory_id):
        inventory = get_object_or_404(Inventory, id=inventory_id)
        data = {
            "shop": inventory.shop.name,
            "product": inventory.product.name,
            "bale_number": inventory.bale_number,
            "quantities": inventory.quantities,
            "amount": inventory.amount,
            "date_added": inventory.date_added,
        }
        return JsonResponse(data)

# 📌 **API View: Add Inventory**
class InventoryCreateView(View):
    def post(self, request):
        shop_id = request.POST.get("shop")
        product_id = request.POST.get("product")
        bale_number = request.POST.get("bale_number")
        quantities = request.POST.get("quantities")
        amount = request.POST.get("amount")

        shop = get_object_or_404(Shop, id=shop_id)
        product = get_object_or_404(Product, id=product_id)

        inventory = Inventory.objects.create(
            shop=shop,
            product=product,
            bale_number=bale_number,
            quantities=quantities,
            amount=amount,
            date_added=now().date(),
        )
        return JsonResponse({"message": "Inventory added successfully", "inventory_id": inventory.id})

# 📌 **Generate Reports**
def generate_report(request, report_type):
    timeframe = request.GET.get("timeframe", "monthly")
    filters = get_timeframe_filter(timeframe)

    if report_type == "cost":
        total_cost = Inventory.objects.filter(**filters).aggregate(
            total_cost=Sum(F('product__unit_price') * F('quantities'))
        )
        report_value = total_cost['total_cost'] or 0
        report_name = "Inventory at Cost"

    elif report_type == "selling_price":
        total_selling_price = Inventory.objects.filter(**filters).aggregate(
            total_selling_price=Sum(F('product__rate_per_bale') * F('quantities'))
        )
        report_value = total_selling_price['total_selling_price'] or 0
        report_name = "Inventory at Selling Price"

    elif report_type == "sales":
        total_sales = Sales.objects.filter(**filters).aggregate(
            revenue=Sum(F('cash_sales') + F('eftpos_sales'))  # ✅ Fixed: Included cash_sales
        )
        report_value = total_sales['revenue'] or 0
        report_name = "Total Daily Sales Report"

    else:
        report_value = 0
        report_name = "Unknown Report"

    return render(request, "admin/reports.html", {
        "report_name": report_name,
        "report_value": report_value,
        "timeframe": timeframe
    })
