# forms.py
from django import forms

from category.models import Category
from store.models import Products
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']  # Only include fields that the user needs to input

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        # Set the initial product value directly if it's provided
        if product:
            self.product = product
        else:
            self.product = None

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'image', 'stock', 'category']  # Include the category field

        # Optional: Customize the widgets for a better user experience
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
