from django.db import models
import uuid

class LiveStock(models.Model):
    LIVE_STOCK_TYPE = [('broiler', 'broiler'),
                       ('layer', 'layer')
                       ]

    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32,
                          editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=LIVE_STOCK_TYPE,
                            blank=False, default='broiler')
    qty = models.IntegerField(verbose_name='Quantity')
    price = models.IntegerField()

    def __str__(self) -> str:
        return str(self.type) + ':' + str(self.qty)


class Batch(models.Model):
    id = models.CharField(max_length=32, default= uuid.uuid4, primary_key=True,
                          editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.IntegerField()
    cost = models.IntegerField()
    target_profit = models.IntegerField()
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
                                   related_name="batches", null=True, blank=True)
    livestock = models.OneToOneField(LiveStock, related_name="batch",
                                     on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    def sale_details(self) -> dict:
        """Computes the worth, count, selling_price, profit of all sales associated with
        the given batch instance"""
        from base.models import Sale

        sales_q = Sale.objects.filter(batch=self)
        worth = 0

        for sale in sales_q:
              worth += sale.amount
            
        selling_price = (self.cost + self.target_profit - worth) / self.size
        profit = worth - self.cost

        return {'worth': worth, 'count': sales_q.count(), 'selling_price': selling_price,
                'profit': profit}

    def mortality_details(self) -> dict:
        """Computes the count, worth of all mortalities associated with
        the given batch instance"""
        
        mortality_q = Mortality.objects.filter(batch=self)
        count = mortality_q.count()
        worth = 0

        for mortality in mortality_q:
            worth += mortality.cost
        
        return {'count': count, 'worth': worth}
    
    def update_cost(self):
        """Updates the cost attribute of the batch instance"""
        from base.models import Item

        cost = 0
        items_q = Item.objects.filter(batch=self)
        tmp = self.livestock.price

        for item in items_q:
            cost += item.price
        self.cost = cost + tmp

        self.save()
        return cost


class Mortality(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=32, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    qty = models.IntegerField()
    cost = models.IntegerField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='mortalities')

    def __str__(self) -> str:
        return str(self.qty) + ' ' + str(self.livestock.batch.name)