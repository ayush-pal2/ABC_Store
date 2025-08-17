from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'store'


urlpatterns = [
    path('', views.store_view, name='store_view'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('products/order/<int:product_id>/', views.place_order, name='place_order'),
    path('orders/customer/', views.customer_orders, name='customer_orders'),
    path('orders/vendor/', views.vendor_orders, name='vendor_orders'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)