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
admin.site.register(Subteam)
admin.site.register(TeamLinking)
admin.site.register(PmftCategory)
admin.site.register(IndividualProcess)
admin.site.register(MaterialSubtype)
admin.site.register(IndividualMaterial)
admin.site.register(FastenerSubtype)
admin.site.register(IndividualFastener)
admin.site.register(IndividualTool)
