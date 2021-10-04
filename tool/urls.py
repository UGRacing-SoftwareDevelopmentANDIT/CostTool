from django.urls import path
from tool import views
app_name = 'tool'
urlpatterns = [

#base pages
path('', views.home, name='home'), 
path('car/<slug:car_slug>', views.car_display, name = 'car_display')
]