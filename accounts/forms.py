from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Customer, Vendor


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VendorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    business_name = forms.CharField(max_length=100, required=True)
    contact_number = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=200, required=True)
    website = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Vendor.objects.create(
                user=user,
                business_name=self.cleaned_data.get('business_name'),
                contact_number=self.cleaned_data.get('contact_number'),
                address=self.cleaned_data.get('address'),
                website=self.cleaned_data.get('website'),
                description=self.cleaned_data.get('description')
            )
        return user
