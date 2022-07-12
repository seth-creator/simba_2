#from django.conf.urls import 
from django.urls import re_path as url, path, re_path
from simba_crud import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^crud/$', views.crud, name = 'add'),
    url(r'^accueil_fourni/$', views.index, name='index'), #Commenter
    path('ajout/',views.formu, name = 'add'),
    url(r'^edition/(?P<id>\d+)/$', views.formu, name='edit'),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^suppression/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^index/$', views.PurchaseList.as_view(), name='indextest'), #Commenter PurchaseList
    re_path('^index2/(?P<username>.+)/$', views.PurchaseListo.as_view()),
    path('tableau/',views.ticket_class_view,name='tableau'),
    #url(r'^export/', views.CategoryExportView.as_view(), name='export'),
    #export
    url(r'export/$', login_required(views.CountryExport.as_view()), name='country_export'),

    #import
   # url(r'import/$', login_required(views.CountryImport.as_view()), name='country_import'),
    #url(r'process_import/$',     login_required(views.CountryProcessImport.as_view()), name='process_import'),
    #url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
]