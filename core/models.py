from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Equipment', 'Equipment'),
        ('Consumable', 'Consumable'),
        ('Medical', 'Medical'),
        ('Safety', 'Safety'),
        ('Tools', 'Tools'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Low Stock', 'Low Stock'),
        ('Out of Stock', 'Out of Stock'),
        ('Maintenance', 'Maintenance'),
    ]

    name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="DRRM-XXX-000")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Equipment')
    barcode = models.CharField(max_length=100, unique=True, default='', help_text="QR or Barcode value")
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def qr_payload(self):
        """Format: Code|Name|Category|ID"""
        return f"{self.item_code}|{self.name}|{self.category}|{self.id}"

    def save(self, *args, **kwargs):
        # Generate item_code if missing (e.g., DRRM-EQU-001)
        if not self.item_code:
            prefix = "DRRM"
            cat_short = self.category[:3].upper()
            count = Item.objects.filter(category=self.category).count() + 1
            self.item_code = f"{prefix}-{cat_short}-{count:03d}"
        
        if not self.barcode:
            self.barcode = self.item_code

        if self.quantity <= 0:
            self.status = 'Out of Stock'
        elif self.quantity <= self.low_stock_threshold:
            self.status = 'Low Stock'
        else:
            self.status = 'Available'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.item_code})"

class StockTransaction(models.Model):
    TRANSACTION_TYPE = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPE)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.type} - {self.item.name} ({self.quantity})"

class Borrowing(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Returned', 'Returned'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrowings')
    borrower_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.borrower_name} borrowed {self.item.name}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

# Keeping Task and TaskItem for legacy/extra functionality if needed, or I can remove them.
# The user asked for specific models, so I'll prioritize those.
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('In Use', 'In Use'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.CharField(max_length=100, default='Admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.item.name} for {self.task.title}"
