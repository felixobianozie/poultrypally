from django.db import models
import uuid


class Customer(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)


class Sale(models.Model):
    STATUS_TYPES = [
        ('paid_only', 'paid_only'),
        ('collected_only', 'collected_only'),
        ('paid_collected', 'paid_collected')
    ]

    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    qty = models.IntegerField()
    amount = models.IntegerField()
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, related_name="sales")
    status = models.CharField(choices=STATUS_TYPES, default="paid_collected", max_length=20)
    deposit = models.IntegerField()
    balance = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.description)