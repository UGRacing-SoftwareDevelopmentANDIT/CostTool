from django.contrib import admin
from tool.models import UserAccount

'''
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('categoryName',)}
    
class HackAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
'''

admin.site.register(UserAccount)