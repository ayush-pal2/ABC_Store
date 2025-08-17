from django.shortcuts import render
from category.models import Category
from store.models import Products

def home_view(request):
    """Render the home page with featured categories and products."""
    categories = Category.objects.all()
    featured_products = Products.objects.all()[:5]  # Fetch first 5 products
    return render(request, 'home/home.html', {
        'categories': categories,
        'featured_products': featured_products
    })
