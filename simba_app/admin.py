from django.contrib import admin

# Register your models here.

from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth.models import AbstractUser

from .models import MonOffre, UserProfile, Service, Pharmacie, Hotel, Hopital, Ecole, Station, Banque, Commentaires, Notation
from mapbox_location_field.spatial.admin import SpatialMapAdmin
from import_export.admin import ImportExportModelAdmin
from .forms import BookResource

class OffreAdmin(ImportExportModelAdmin, SpatialMapAdmin) :
    display = ('statut','types','tarif')
    search_fields = ('types',)
    list_filter = ('statut', 'commune', 'tarif',)
    date_hierarchy = 'date'
    resource_class = BookResource

class UserAdmin(SpatialMapAdmin):
    display = ( 'user', 'phone','city')
    
    
class PointAdmin(SpatialMapAdmin):
    display = ( 'nom')
    
    
#class BookAdmin(ImportExportModelAdmin):
    #resource_class = BookResource

#Register your models here.
admin.site.register(MonOffre, OffreAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Service, SpatialMapAdmin)
admin.site.register(Pharmacie, PointAdmin)
admin.site.register(Hotel, PointAdmin)
admin.site.register(Ecole, PointAdmin)
admin.site.register(Banque, PointAdmin)
admin.site.register(Station, PointAdmin)
admin.site.register(Commentaires)
admin.site.register(Notation)
