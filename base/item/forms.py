from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from base.models import Item, CustomUser


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'qty', 'measure', 'price', 'packaging')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-round'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-round', 'style': 'max-height: 70px;'}),
            'qty': forms.NumberInput(attrs={'class': 'w3-input w3-round'}),
            'price': forms.NumberInput(attrs={'class': 'w3-input w3-round'}),
            'measure': forms.Select(attrs={'class': 'w3-input w3-round'})
        }
        labels = {
            'name': 'Item Name',
            'qty': 'Quantity',
            'price': 'Purchase Price'

        }
