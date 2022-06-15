from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import MonOffre

from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters

class AdSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = MonOffre
        geo_field = 'geom'
        fields = ('id','statut','types','piece','superficie','tarif','image','image2','image3','video', 'document', 'agence', 'description','commentaire', 'date','commune','quartier','contact', 'email','fournisseur' )
        
        
class RegionFilter(GeoFilterSet):
    slug = filters.CharFilter('slug', lookup_expr='istartswith')
    contains_geom = GeometryFilter('geom', lookup_expr='contains')
    

    class Meta:
        model = MonOffre
        fields = ('statut','types','piece','superficie','tarif', 'commentaire', 'contact', 'email')