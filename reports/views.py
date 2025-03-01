from django.shortcuts import render
from django.db.models import Sum, F
from inventory.models import Sales, Shop, Product, Inventory  # ✅ Ensure correct imports
from django.conf import settings
from django.db.models.functions import TruncDate

# ✅ **Sales Report View**
def sales_report(request):
    timeframe = request.GET.get("timeframe", "monthly")
    selected_shop = request.GET.get("shop")
    selected_category = request.GET.get("category")

    sales_query = Sales.objects.all()
    if selected_shop:
        sales_query = sales_query.filter(shop_id=selected_shop)
    if selected_category:
        sales_query = sales_query.filter(product__category=selected_category)

    # ✅ Aggregate sales by date
    sales_data = sales_query.annotate(
        date=TruncDate('date_recorded')
    ).values('date').annotate(
        total_sales=Sum(F('cash_sales') + F('eftpos_sales'))
    ).order_by('date')

    labels = [sale['date'].strftime("%b %d") for sale in sales_data]
    values = [sale['total_sales'] for sale in sales_data]

    context = {
        'report_name': f"Sales Report - {timeframe.capitalize()}",
        'labels': labels,
        'values': values,
        'shops': Shop.objects.all(),
        'categories': Product.objects.values_list('category', flat=True).distinct(),
        'selected_shop': selected_shop,
        'selected_category': selected_category,
    }
    return render(request, "reports/sales_report.html", context)


# ✅ **Inventory Report View**
def inventory_report(request):
    selected_shop = request.GET.get("shop")
    selected_category = request.GET.get("category")

    inventory_query = Inventory.objects.all()
    if selected_shop:
        inventory_query = inventory_query.filter(shop_id=selected_shop)
    if selected_category:
        inventory_query = inventory_query.filter(product__category=selected_category)

    # ✅ Aggregate inventory totals
    inventory_data = inventory_query.values('product__name', 'shop__name').annotate(
        total_quantity=Sum('quantities'),
        total_value=Sum(F('quantities') * F('amount'))  # ✅ Calculate total inventory value
    ).order_by('product__name')

    total_units = inventory_query.aggregate(total=Sum('quantities'))['total'] or 0
    total_value = inventory_query.aggregate(total=Sum(F('quantities') * F('amount')))['total'] or 0

    context = {
        'report_name': "Inventory Report",
        'inventory_data': inventory_data,
        'shops': Shop.objects.all(),
        'categories': Product.objects.values_list('category', flat=True).distinct(),
        'selected_shop': selected_shop,
        'selected_category': selected_category,
        'total_units': total_units,
        'total_value': total_value,
    }
    return render(request, "reports/inventory_report.html", context)
