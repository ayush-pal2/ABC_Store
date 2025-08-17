from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/', permanent=False)),  # Redirect root to /home/
    path('home/', include('home.urls')),  # Home app URLs
    path('accounts/', include('accounts.urls')),  # Accounts app URLs
    path('category/', include('category.urls')),  # Category app URLs
    path('store/', include('store.urls')),  # Store app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)