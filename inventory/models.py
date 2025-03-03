from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Product(models.Model):
    supplier = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)  
    category = models.CharField(max_length=50)
    weight_kg = models.IntegerField(default=0)  
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    rate_per_bale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.supplier.name}"

# ✅ Shop Model
class Shop(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# ✅ Sales Model (Only Defined Here)
class Sales(models.Model):
    """✅ Sales Model with Auto-Calculated Cash Sales"""
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="sales")  # ✅ Fix reverse accessor clash
    date_recorded = models.DateField(default=now)
    till_number = models.CharField(max_length=20, blank=True, null=True)
    cashier = models.CharField(max_length=255, blank=True, null=True)
    assistant_supervisor = models.CharField(max_length=255, blank=True, null=True)

    # ✅ Use DecimalField for currency support
    z_reading = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eftpos_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    overing = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    down = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    memo = models.TextField(blank=True, null=True)
    time_recorded = models.DateTimeField(default=now)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def cash_sales(self):
        """✅ Auto-Calculates Cash Sales"""
        return self.z_reading - self.eftpos_sales + self.overing - self.down

    def __str__(self):
        return f"Sales - {self.shop.name} ({self.date_recorded}) - PGK {self.cash_sales:.2f}"

class Inventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  
    quantities = models.IntegerField(default=0)  
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # ✅ Fixed missing parenthesis
    bale_number = models.PositiveIntegerField(default=1)  
    date_added = models.DateField(default=now)  
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"{self.product.name if self.product else 'No Product Assigned'} ({self.shop.name}) - {self.quantities} items, Bale {self.bale_number}, Amount: {self.amount} PGK"

class Supplier(models.Model):
    """✅ Supplier Model"""
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


