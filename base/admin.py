from django.contrib import admin

# Register your models here.

from base.user.models import CustomUser, Farm
from base.batch.models import Batch, LiveStock, Mortality
from base.item.models import Item, Measure, Stock
from base.sale.models import Sale, Customer

admin.site.register([CustomUser, Batch, LiveStock, Measure, Stock, 
                     Item, Customer, Sale, Mortality, Farm])
