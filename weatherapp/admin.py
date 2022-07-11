from django.contrib import admin
from import_export import resources
from .models import City
from import_export.admin import ImportExportModelAdmin

#! For import export
class CityResource(resources.ModelResource):    
    class Meta:
        model = City 

class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource

admin.site.register(City,CityAdmin)
