from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    keyword = models.CharField(max_length=255)  # Adjusted to CharField
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Use BooleanField for status instead of string
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('category:products_bycategory', args=[self.slug])

    @property
    def ImageURL(self):
        if self.image:
            return self.image.url
        return '/static/default-category-image.png'  # Path to default image

    def __str__(self):
        return self.name
