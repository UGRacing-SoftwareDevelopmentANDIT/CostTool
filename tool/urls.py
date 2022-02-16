from django.urls import path
from tool import views


app_name = 'tool'
urlpatterns = [
path('', views.home, name='home'), 
path('car/addCar', views.add_car, name = 'add_car'),
path('car/<slug:car_slug>', views.car_display, name = 'car_display'),
path('car/<slug:car_slug>/addSystem', views.add_system, name = 'add_system'),
path('car/<slug:car_slug>/<slug:system_slug>', views.system_display, name = 'system_display'),

path('car/<slug:car_slug>/<slug:system_slug>/editSubteam', views.edit_subteam, name = 'edit_subteam'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:subteam_slug>/delete', views.delete_subteam, name = 'delete_subteam'),

path('car/<slug:car_slug>/<slug:system_slug>/add-assembly', views.add_assembly, name="add_assembly"),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/editAssignEng', views.edit_assign_eng, name = 'edit_assign_eng'),

path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/addPart', views.add_part, name = 'add_part'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/addPMFT', views.add_pmft, name = 'add_pmft'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
]
