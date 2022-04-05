from django.urls import path
from tool import views


app_name = 'tool'
urlpatterns = [
path('', views.home, name='home'), 
path('car/addCar', views.add_car, name = 'add_car'),
path('car/<slug:car_slug>/edit', views.add_car, name = 'add_car'),
path('car/<slug:car_slug>', views.car_display, name = 'car_display'),
path('car/<slug:car_slug>/delete', views.car_delete, name = 'car_delete'),

path('car/<slug:car_slug>/addSystem', views.add_system, name = 'add_system'),
path('car/<slug:car_slug>/<slug:system_slug>/edit', views.add_system, name = 'add_system'),
path('car/<slug:car_slug>/<slug:system_slug>', views.system_display, name = 'system_display'),
path('car/<slug:car_slug>/<slug:system_slug>/delete', views.system_delete, name = 'system_delete'),
path('car/<slug:car_slug>/<slug:system_slug>/editSubteam', views.edit_subteam, name = 'edit_subteam'),
path('car/<slug:car_slug>/<slug:system_slug>/subteam/<slug:subteam_slug>/delete', views.delete_subteam, name = 'delete_subteam'),

path('car/<slug:car_slug>/<slug:system_slug>/add-assembly', views.add_assembly, name="add_assembly"),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/edit', views.add_assembly, name="add_assembly"),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/delete', views.assembly_delete, name="assembly_delete"),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/editAssignEng', views.edit_assign_eng, name = 'edit_assign_eng'),

path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/addPart', views.add_part, name = 'add_part'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/edit', views.add_part, name = 'add_part'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/delete', views.part_delete, name = 'part_delete'),

path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/addPMFT', views.add_pmft, name = 'add_pmft'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/<slug:pmft_slug>/edit', views.add_pmft, name = 'add_pmft'),
path('car/<slug:car_slug>/<slug:system_slug>/<slug:assembly_slug>/<slug:part_slug>/<slug:pmft_slug>/delete', views.pmft_delete, name = 'pmft_delete'),

path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('change_password/', views.change_password, name='change_password'),
path('logout/', views.user_logout, name='logout'),
]
