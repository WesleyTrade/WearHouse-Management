from django.db import models
from inventory.models import Sales, Shop  # ✅ Correct import
from django.utils.timezone import now  

class Report(models.Model):
    """✅ Report Model to Track Sales & Inventory Reports"""
    
    REPORT_TYPES = [
        ("sales", "Sales Report"),
        ("inventory", "Inventory Report"),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
