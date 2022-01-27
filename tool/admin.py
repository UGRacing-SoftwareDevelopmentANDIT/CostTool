from django.contrib import admin
from tool.models import *
'''
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('categoryName',)}
    
class HackAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
'''

admin.site.register(UserAccount)
admin.site.register(Car)
admin.site.register(Assembly)
admin.site.register(System)
admin.site.register(Part)
admin.site.register(PMFT)
admin.site.register(Subteam)
admin.site.register(TeamLinking)
