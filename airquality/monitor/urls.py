from django.urls import path
from . import views
from django.urls import path, include

# urls.py
urlpatterns = [

    path('data/', views.receive_data, name='receive_data'),
    path('', views.dashboard, name='dashboard'),
    path('get_all_data/', views.get_all_data, name='get_all_data'),
    path('about/', views.about, name='about'),
    path('livedata/', views.live, name='live'),
    path('get_latest_data/', views.get_latest_data, name='get_latest_data'),
    path('firmware/', include('firmware.urls'))

]
