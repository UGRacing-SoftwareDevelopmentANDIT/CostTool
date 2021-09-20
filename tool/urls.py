from django.urls import path
from tool import views
app_name = 'tool'
urlpatterns = [

#base pages
path('', views.home, name='home')
]