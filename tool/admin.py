from django.contrib import admin
from tool.models import PMFT, Car, UserAccount, System, Part, Assembly
'''
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('categoryName',)}
    
class HackAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
'''

admin.site.register(UserAccount)
admin.site.register(Car)
admin.site.register(System)
admin.site.register(PMFT)
admin.site.register(Assembly)
admin.site.register(Part)