from django.apps import apps  # ✅ Import get_model dynamically
from django.shortcuts import render
from django.db.models import Sum, F
from inventory.models import Sales, Shop, Product
import datetime  

def sales_report(request):
    """✅ Generates progressive sales report for weekly & monthly"""

    Product = apps.get_model('inventory', 'Product')  # ✅ Lazy import of Product model

    # 🔹 Get user-selected timeframe (default: monthly)
    timeframe = request.GET.get("timeframe", "monthly")  
    selected_shop = request.GET.get("shop")

    sales_query = Sales.objects.all()

    # 🔹 Filter by shop if selected
    if selected_shop and selected_shop.isdigit():
        sales_query = sales_query.filter(shop_id=int(selected_shop))

    # 🔹 Get today's date
    today = datetime.date.today()

    # 🔹 Define start date for progressive report
    if timeframe == "weekly":
        start_date = today - datetime.timedelta(days=7)  # Last 7 days
    elif timeframe == "monthly":
        start_date = today.replace(day=1)  # Start of the current month
    else:
        start_date = None

    # 🔹 Apply date filter
    if start_date:
        sales_query = sales_query.filter(date_recorded__gte=start_date)

    # ✅ Aggregate sales data progressively
    sales_data = sales_query.values('date_recorded').annotate(
        total_sales=Sum(F('z_reading') - F('eftpos_sales') + F('overing') - F('down'))
    ).order_by('date_recorded')

    # ✅ Compute total sales sum in Python instead of using `sum` in the template
    total_sales = sum(sale['total_sales'] for sale in sales_data if sale['total_sales'])

    # ✅ Convert date format & handle None values
    labels = []
    values = []
    for sale in sales_data:
        labels.append(sale['date_recorded'].strftime("%b %d") if sale['date_recorded'] else "Unknown")
        values.append(sale['total_sales'])

    # ✅ Zip labels and values to avoid template errors
    sales_data_zipped = list(zip(labels, values))

    context = {
        'report_name': f"Sales Report - {timeframe.capitalize()}",
        'sales_data': sales_data_zipped,  # Pass zipped data to the template
        'total_sales': total_sales,  # ✅ Fix for sum filter
        'timeframe': timeframe,
        'today_date': today.strftime("%A, %B %d, %Y"),
    }

    return render(request, "reports/sales_report.html", context)


# 🔹 Inventory Report View
def inventory_report(request):
    """✅ Generates inventory report"""

    selected_shop = request.GET.get("shop")
    selected_category = request.GET.get("category")

    inventory_query = Product.objects.all()

    # 🔹 Filter by shop and category
    if selected_shop and selected_shop.isdigit():
        inventory_query = inventory_query.filter(shop_id=int(selected_shop))
    if selected_category:
        inventory_query = inventory_query.filter(category=selected_category)

    # ✅ Aggregate inventory data
    inventory_data = inventory_query.annotate(
        total_quantity=Sum('quantities'),
        total_value=Sum(F('quantities') * F('unit_price'))
    ).values('name', 'shop__name', 'total_quantity', 'total_value').order_by('name')

    shops = Shop.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'report_name': "Inventory Report",
        'inventory_data': inventory_data,
        'shops': shops,
        'categories': categories,
        'selected_shop': int(selected_shop) if selected_shop and selected_shop.isdigit() else None,
        'selected_category': selected_category,
    }

    return render(request, "reports/inventory_report.html", context)
