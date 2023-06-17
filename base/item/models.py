from django.db import models
import uuid


class Measure(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.name)


class Stock(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    tier1 = models.ForeignKey(Measure, related_name="tier1", on_delete=models.SET_NULL, blank=True, null=True)
    tier1_qty = models.IntegerField(default=0)
    tier1_price = models.IntegerField(default=0)
    tier2 = models.ForeignKey(Measure, related_name="tier2", on_delete=models.SET_NULL, blank=True, null=True)
    tier2_qty = models.IntegerField(default=0)
    tier2_price = models.IntegerField(default=0)
    tier2_limit = models.IntegerField(default=0)
    tier3 = models.ForeignKey(Measure, related_name="tier3", on_delete=models.SET_NULL, blank=True, null=True)
    tier3_qty = models.IntegerField(default=0)
    tier3_price = models.IntegerField(default=0)
    tier3_limit = models.IntegerField(default=0)


class Item(models.Model):
    PACKAGING = [('single', 'single-level'),
                 ('multiple', 'multi-level')
                 ]

    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qty = models.IntegerField()
    measure = models.ForeignKey(Measure, null=True, on_delete=models.SET_NULL, related_name="measure_items")
    price = models.IntegerField()
    packaging = models.CharField(choices=PACKAGING, max_length=20, default='single')
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, null=True, blank=True, related_name='item')
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, null=True, blank=True, related_name='batch_items')
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='user_items')
    created_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return str(self.name)
