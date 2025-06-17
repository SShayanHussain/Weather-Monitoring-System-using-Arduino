from django.urls import path
from . import views 

urlpatterns = [
    path('upload/', views.upload_firmware, name='upload_firmware'),
    path('check/', views.check_firmware, name='latest_firmware'),
    path('upload_', views.upload, name='upload'),
    


]
