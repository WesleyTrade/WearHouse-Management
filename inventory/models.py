from django.db import models   
from django.contrib.auth.models import User
from django.utils.timezone import now  

# ✅ Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# ✅ Shop Model
class Shop(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# ✅ Product Model
class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)  
    category = models.CharField(max_length=50)
    weight_kg = models.IntegerField(default=0)  
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    rate_per_bale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.supplier.name}"

# ✅ User Profile Model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('clerk', 'Pricing Clerk'),
        ('supervisor', 'Supervisor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='clerk')

    def __str__(self):
        return f"{self.user.username} - {self.shop.name if self.shop else 'No Shop Assigned'} ({self.role})"

# ✅ Inventory Model
class Inventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  
    quantities = models.IntegerField(default=0)  
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    bale_number = models.PositiveIntegerField(default=1)  
    date_added = models.DateField(default=now)  
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inventories"  # ✅ Fix pluralization

    def __str__(self):
        return f"{self.product.name if self.product else 'No Product Assigned'} ({self.shop.name}) - {self.quantities} items, Bale {self.bale_number}, Amount: {self.amount} PGK"

# ✅ Sales Model (Auto-Calculating Cash Sales)
class Sales(models.Model):
    shop = models.ForeignKey("Shop", on_delete=models.CASCADE)
    date_recorded = models.DateField(default=now)
    till_number = models.CharField(max_length=20)
    cashier = models.CharField(max_length=255)
    assistant_supervisor = models.CharField(max_length=255, blank=True, null=True)
    z_reading = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eftpos_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    overing = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ Added field
    down = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ Added field
    memo = models.TextField(blank=True, null=True)
    time_recorded = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ["-date_recorded"]

    def save(self, *args, **kwargs):
        """Auto-calculates Cash Sales (Z Reading - EFTPOS Sales) before saving."""
        self.cash_sales = max(self.z_reading - self.eftpos_sales, 0)  # ✅ Prevent negative values
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sales Record - {self.shop.name} ({self.date_recorded})"
