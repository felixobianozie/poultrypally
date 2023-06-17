from django.forms import ModelForm, TextInput, NumberInput, Select

from base.models import Batch, LiveStock, Mortality


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = ('name', 'target_profit')
        widgets = {
            'name': TextInput(attrs={'class': 'w3-input w3-round'}),
            'target_profit': NumberInput(attrs={'class': 'w3-input w3-round'})
        }
        labels = {
            'name': 'Batch Name',
        }


class LiveStockForm(ModelForm):
    class Meta:
        model = LiveStock
        fields = ('qty', 'price', 'type')
        widgets = {
            'qty': NumberInput(attrs={'class': 'w3-input w3-round'}),
            'price': NumberInput(attrs={'class': 'w3-input w3-round'}),
        }


class MortalityForm(ModelForm):
    class Meta:
        model = Mortality
        fields = ('batch','qty','cost' )
        widgets = {
            'batch': TextInput(attrs={'class': 'w3-input w3-round'}),
            'qty': NumberInput(attrs={'class': 'w3-input w3-round'}),
            'cost': NumberInput(attrs={'class': 'w3-input w3-round'}),
        }