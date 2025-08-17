from django.contrib import admin
from .models import Customer, Address, Vendor


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_type', 'street_address', 'city')
    search_fields = ('customer__user__username', 'street_address', 'city')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'contact_number', 'address')
    search_fields = ('user__username', 'business_name')
