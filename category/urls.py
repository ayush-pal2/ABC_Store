from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('add/', views.add_category, name='add_category'),
    path('filter/', views.filter_products, name='filter_products'),
    path('search/', views.search, name='search'),
    path('list/', views.category_list, name='category_list'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)