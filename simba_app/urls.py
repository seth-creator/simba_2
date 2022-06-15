from django.urls import path
from django.contrib import admin
from django.urls import re_path as url
#from . import views

urlpatterns = [
    
]

from django.urls import path
from  simba_app import views
from compte.views import accespage, inscripage, lagoutuser
from compte2.views import accespage2, inscripage2, lagoutuser2

from django.conf.urls import  include
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from . models import MonOffre, LimQuart, Pharmacie, Culte, Hotel, Boulangerie, Banque, Cafe, Cinema, Commerce, Commissariat, Ecole, Station, Hopital, FastFood, UserProfile
from . models import AdministrativeBoundary


from rest_framework.routers import DefaultRouter
from .views import AdViewSet, Buffer

router = DefaultRouter()
router.register(r'markers', AdViewSet, basename='marker')
urlpatterns = router.urls

urlpatterns = [
    path('profile/<int:pk>', views.edit_user, name='account_update'),
    url(r'^profile/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    #url(r'^profile/<int:pk>$', views.edit_user, name='account_update'),
    #path('fournisseur/',admin.site.urls, name = 'fournisseur'),
    #path('accueil/',views.index),
    path('formulaire/',views.formu, name = 'formulaire'),
    path('',views.map, name = 'filter'),
    #path('filter',views.AdViewSet.bbox_filter_field, name = 'filter'),
    path('inscription/',inscripage, name = 'inscrit'),
    path('inscription-agent/',inscripage2, name = 'inscrit2'),
    #path('',accespage, name = 'acces'),
    path('login-agent',accespage2, name = 'acces2'),
    path('quitter/',lagoutuser, name = 'quitter'),
    path('produit/',views.gisfilter, name = 'produit'),
    url(r'^pagedetail(?P<id>\d+)/$', views.product_detail_view, name='detail'),
    path('service/',views.serviceview, name = 'service'),
    path('fournisseur/',views.profilefournisseur, name = 'fournisseur'),
    url(r'^user(?P<id>\d+)/$', views.user_detail_view, name='userdetail'),
    url(r'^perso(?P<id>\d+)/$', views.perso_detail_view, name='persodetail'),
    path('recherche/',views.BarFilter.as_view(), name = 'recherche'),
    #url(r'^accueil/$', TemplateView.as_view(template_name = 'simba/index2.html'), name = 'home'),
    url(r'^data/$', GeoJSONLayerView.as_view(model = LimQuart, properties = ('nom')), name = 'data'),
    url(r'^datab/$', GeoJSONLayerView.as_view(model = Buffer, properties = ()), name = 'datab'),
    url(r'^commune/$', GeoJSONLayerView.as_view(model = AdministrativeBoundary, properties = ('nom','identifiant')), name = 'commune'),
    url(
        r'^filtergeom/$',
        views.AdViewSet.as_view ({'get': 'list'}),
        name='filtergeom',
    ),
 
    url(r'^contact/$', views.contact, name='contact'),
    
    url(r'^pharmacie/$', GeoJSONLayerView.as_view(model = Pharmacie, properties = ('nom')), name = 'pharmacie'),
    url(r'^hopital/$', GeoJSONLayerView.as_view(model = Hopital, properties = ('nom')), name = 'hopital'),
    url(r'^hotel/$', GeoJSONLayerView.as_view(model = Hotel, properties = ('nom')), name = 'hotel'),
    url(r'^boulangerie/$', GeoJSONLayerView.as_view(model = Boulangerie, properties = ('nom')), name = 'boulangerie'),
    url(r'^banque/$', GeoJSONLayerView.as_view(model = Banque, properties = ('nom')), name = 'banque'),
    url(r'^cafe/$', GeoJSONLayerView.as_view(model = Cafe, properties = ('nom')), name = 'cafe'),
    url(r'^cinema/$', GeoJSONLayerView.as_view(model = Cinema, properties = ('nom')), name = 'cinema'),
    url(r'^commerce/$', GeoJSONLayerView.as_view(model = Commerce, properties = ('nom')), name = 'commerce'),
    url(r'^culte/$', GeoJSONLayerView.as_view(model = Culte, properties = ('nom')), name = 'culte'),
    url(r'^commissariat/$', GeoJSONLayerView.as_view(model = Commissariat, properties = ('nom')), name = 'commissariat'),
    url(r'^ecole/$', GeoJSONLayerView.as_view(model = Ecole, properties = ('nom')), name = 'ecole'),
    url(r'^station/$', GeoJSONLayerView.as_view(model = Station, properties = ('nom')), name = 'station'),
    url(r'^fastfood/$', GeoJSONLayerView.as_view(model = FastFood, properties = ('nom')), name = 'fastfood'),
    url(r'^fournimap/$', GeoJSONLayerView.as_view(model = UserProfile, properties = ('organization','phone', 'website', 'bio', 'city', 'country')), name = 'fournimap'),
    path('notes/',views.home,name='notes'),
    path('tableau/',views.ticket_class_view,name='tableau'),
    
]


