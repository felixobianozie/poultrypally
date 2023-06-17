from django.forms import ModelForm

from base.models import Sale


class SalesForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('batch', 'description', 'qty', 'amount', 'status', 'deposit', 'balance' )

