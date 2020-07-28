from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
                'name',
                'price',
                'minimum_order',
                'img',
                'description',
                'sub_category',
                'status',
            )