import django_filters
from .models import MonOffre, Service,  UserProfile

class MonFiltre(django_filters.FilterSet):
    class Meta :
        model = MonOffre
        fields = ('statut', 'types', 'tarif','commune', 'quartier','fournisseur')

class ServiceFilter(django_filters.FilterSet):
    class Meta :
        model = Service
        fields = ('nom', 'secteur', 'caract1','caract2')
        
        
class FournisseurFilter(django_filters.FilterSet):        
    class Meta :
        model = UserProfile
        fields = ('city',)