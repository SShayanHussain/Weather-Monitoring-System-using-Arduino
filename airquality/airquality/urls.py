# airquality/urls.py
from django.contrib import admin
from django.urls import path, include
from monitor import views  # Import views from your app
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('monitor.urls')),  # Include your app's routes
    path('', views.dashboard, name='dashboard'),
    path('firmware/', include('firmware.urls')), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))