from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from accounts.models import Vendor, Customer
from category.models import Category
from django.utils.text import slugify


def validate_price(value):
    if value < 0:
        raise ValidationError('Price cannot be negative.')


class Products(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # Allow blank to auto-generate slug
    description = models.TextField(null=True, blank=True, max_length=10000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    image = models.ImageField(null=True, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
        unique_together = ('slug', 'category')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            while Products.objects.filter(slug=unique_slug, category=self.category).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('store:product_details', args=[self.category.slug, self.slug])

    @property
    def ImageURL(self):
        if self.image:
            return self.image.url
        return '/static/default-image.png'  # Path to default image

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.customer.get_full_name()}"
