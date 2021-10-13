from django.urls import path
from tool import views
app_name = 'tool'
urlpatterns = [
    
path('', views.home, name='home'), 
path('car/<slug:car_slug>', views.car_display, name = 'car_display'),
path('car/<slug:car_slug>/<slug:system_slug>', views.system_display, name = 'system_display'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>', views.assembly_display, name = 'assembly_display'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>', views.part_display, name = 'part_display'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/<slug:pmft_slug>', views.pmft_display, name = 'pmft_display'),
]