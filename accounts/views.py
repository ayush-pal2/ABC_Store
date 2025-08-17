from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
import logging

from .forms import CustomerSignUpForm, VendorSignUpForm
from .models import Customer, Vendor
from store.models import Order, Products

# Set up logging
logger = logging.getLogger(__name__)


def login(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)

                # Redirect based on user role
                if user.is_superuser:
                    return redirect('admin:index')  # Redirect to Django admin
                elif user.groups.filter(name='Vendor').exists():
                    return redirect('accounts:vendor_dashboard')
                elif user.groups.filter(name='Customer').exists():
                    return redirect('accounts:customer_dashboard')

                # Fallback redirect if no specific role is found
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
                logger.warning(f"Failed login attempt for user: {username}")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def register_customer(request):
    """Handle customer registration."""
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Customer.objects.get_or_create(user=user)
                customer_group, _ = Group.objects.get_or_create(name='Customer')
                customer_group.user_set.add(user)
                return redirect('accounts:login')
            except IntegrityError:
                form.add_error(None, 'A customer with this username already exists.')
                logger.error(f"IntegrityError during customer registration: {form.cleaned_data.get('username')}")
    else:
        form = CustomerSignUpForm()
    return render(request, 'registration/register_customer.html', {'form': form})


def register_vendor(request):
    """Handle vendor registration."""
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Vendor.objects.get_or_create(user=user)
                vendor_group, _ = Group.objects.get_or_create(name='Vendor')
                vendor_group.user_set.add(user)
                return redirect('accounts:login')
            except IntegrityError:
                form.add_error(None, 'A vendor with this username already exists.')
                logger.error(f"IntegrityError during vendor registration: {form.cleaned_data.get('username')}")
    else:
        form = VendorSignUpForm()
    return render(request, 'registration/register_vendor.html', {'form': form})


def logout(request):
    """Handle user logout."""
    django_logout(request)
    return redirect('home')


@login_required
def customer_dashboard(request):
    """View for the customer dashboard."""
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer)
    products = Products.objects.all()  # Fetch all products or filter as needed
    return render(request, 'accounts/customer_dashboard.html', {'orders': orders, 'products': products})

@login_required
def vendor_dashboard(request):
    """View for the vendor dashboard."""
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Products.objects.filter(vendor=vendor)
    orders = Order.objects.filter(product__vendor=vendor)
    return render(request, 'accounts/vendor_dashboard.html', {'products': products, 'orders': orders})
