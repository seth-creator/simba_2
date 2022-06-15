from django.shortcuts import render
from django.urls.conf import include
from django.contrib.gis.db import models
from django.db import models

# Create your views here.
def index(request) :
    return render(request, 'index.html')

from django.shortcuts import render, HttpResponse,redirect
from django.contrib.gis.geos import Polygon, GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance`
from django.views.generic import TemplateView
from simba_app.models import MonOffre, Service, Notes, Commentaires, Notation
from simba_app.forms import MonOffreForm, UserForm, ContactForm, SearchForm, NotationForm
from . filters import MonFiltre, ServiceFilter, FournisseurFilter
from django.contrib.auth.forms import UserCreationForm
#from compte.forms import CreerUser
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter
from .gis_forms import AdSerializer, RegionFilter
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, NoteForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django import forms
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from search_views.search import SearchListView
from search_views.filters import BaseFilter

from django.db.models import Count, Q
from django.utils.datastructures import MultiValueDictKeyError
from .models import Passenger
from django.db.models import Sum



# Creation de vue.

@login_required(login_url = 'acces')
class MaVue(TemplateView) :
    template_name = 'simba/formulaire.html'
    def get(self, request) :
        form = MonOffreForm()
        #bbox = (-6.9145,53.5958,-5.6085,53.1023)#min_lat,max_lat,min_lng,max_lng 
        #geoom = Polygon.from_bbox(bbox)
        pnt = GEOSGeometry('POINT(-3.97684 5.39460)', srid=4326)
        qs = MonOffre.objects.filter(geom__distance_lte=(pnt, D(km=15)))
        offres = MonOffre.objects.all()
        myfilter = MonFiltre(request.GET, queryset =offres )
        offres = myfilter.qs
        context = {'offres':offres, 'pnt': pnt, 'qs': qs, 'form' : form, 'myfilter' : myfilter}
        return render(request, self.template_name, context)
class Buffer(models.Model) :
    pnt = GEOSGeometry('POINT(-3.97684 5.39460)', srid=4326)
    qs = MonOffre.objects.filter(geom__distance_lte=(pnt, D(km=15)))

#formulaire
@login_required(login_url = 'acces')
def formu(request) :
        if request.method == 'POST':
            form = MonOffreForm(request.POST, request.FILES)
        #form = MonOffreForm(request.POST)
            if form.is_valid():
                form.save()
            #text = form.cleaned_data['post']
           
                return redirect('filter')
        else :
             form = MonOffreForm()
            
        args = {'form': form}   
        return render(request,'simba/form.html', args)


# convertir en geojson
class AdViewSet (ReadOnlyModelViewSet):
    
        
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter,)
    queryset = MonOffre.objects.filter(geom__isnull=False)
    serializer_class = AdSerializer
      
    context = {'queryset' : queryset,'filter_backends' : filter_backends, 'bbox_filter_field' : bbox_filter_field, 'serializer_class' : serializer_class}
    
    
class LocationList(ReadOnlyModelViewSet):

    queryset = MonOffre.objects.all()
    serializer_class = AdSerializer
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True # Optional
    
#@login_required(login_url = 'acces')
note = ''
def gisfilter(request) :
    #point = input('Entrer les coords')
    pnt = GEOSGeometry('POINT(-3.97684 5.39460)', srid=4326)
    qs = MonOffre.objects.filter(geom__distance_lte=(pnt, D(km=5)))
    offres = MonOffre.objects.all()
    offress = MonOffre.objects.all()
    myfilter = MonFiltre(request.GET, queryset = offres )
    gis_filters = RegionFilter(request.GET, queryset = offress )
    offres = myfilter.qs
    offress = gis_filters.qs
    note = Notation.objects.values('monoffre').annotate(Note = Sum('note')/Count('monoffre'))
    context = {'myfilter' : myfilter, 'gis_filters' : gis_filters, 'pnt' : pnt, 'qs' : qs, 'offres': offres,'note':note}
    serializer_class = AdSerializer
    return render(request, 'simba/gis_filter.html', context)



def product_detail_view(request, id=None):
    product = MonOffre.objects.get( id=id)
    #fourni = UserProfile.objects.all()
    related = MonOffre.objects.filter(types = product.types).exclude(id=id)[:4]
    curent_user = request.user
    #comment = Commentaires.objects.get(offre_id = id)
    notes = Commentaires.objects.filter(offre_id = id)
    #nota = Notation.objects.get(monoffre_id = id)
    #nota = get_object_or_404(Notation, id=id)
    if request.method == 'POST' :
        try :
            forms = Notation.objects.create(note = request.POST['note_note'],monoffre = MonOffre.objects.get(id =id))
        except MultiValueDictKeyError :
            forms = 0
            
    form = ""
    if request.method == 'POST':
        try :
            form = Commentaires.objects.create(text = request.POST['commento'], user = request.user, offre = MonOffre.objects.get(id =id))
        except MultiValueDictKeyError :
            form =0
            #if form.is_valid():
            #form.save()
            
    noto = Notation.objects.filter(monoffre_id = id).values('monoffre').annotate(Note = Sum('note')/Count('monoffre'))
    noty = noto.values('Note')
        
        
    context= {'product': product, 'relatedvalue' : related,'Curent_user' : curent_user,'Notes' : notes, 'Noto' : noto, 'Noty': noty}
    return render(request, 'simba/product-detail-view.html', context)

def user_detail_view(request, id=None):

    userdt = get_object_or_404(UserProfile, id=id)
    
    context= {'userdt': userdt,
              }
    
    return render(request, 'simba/user-detail-view.html', context)

def perso_detail_view(request, id=None):

    perso = get_object_or_404(UserProfile, id=id)
    
    context= {'perso': perso,
              }
    
    return render(request, 'simba/perso-detail-view.html', context)

#@login_required(login_url = 'acces')   
def map(request) :
    #point = input('Entrer les coords')
    pnt = GEOSGeometry('POINT(-3.97684 5.39460)', srid=4326)
    qs = MonOffre.objects.filter(geom__distance_lte=(pnt, D(km=15)))
    offres = MonOffre.objects.all()
    offress = MonOffre.objects.all()
    myfilter = MonFiltre(request.GET, queryset = offres )
    gis_filters = RegionFilter(request.GET, queryset = offress )
    offres = myfilter.qs
    offress = gis_filters.qs
    context = {'myfilter' : myfilter, 'gis_filters' : gis_filters, 'pnt' : pnt, 'qs' : qs, 'offres': offres}
    serializer_class = AdSerializer
    return render(request, 'simba/map_2.html', context)



"""
class LocationList(ListCreateAPIView):

    queryset = models.Location.objects.all()
    serializer_class = RegionFilter
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True # Optional

      """  


#@login_required() # only logged in users should access this
#@login_required
"""def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/profile/')

        return render(request, 'profile/account_update.html', {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied"""

def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('photo','website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/produit/')

        return render(request, "profile/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


def contact(request) :
    form = ContactForm(request.POST, request.FILES)
    
    if form.is_valid():
        
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']

        recipients = ['sackosekou1113@gmail.com']
        if cc_myself:
            recipients.append(sender)

        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect('http://192.168.1.185/')
    context = {'form' : form }
    return render(request,'simba/contact.html', context)


def serviceview(request) :
    #point = input('Entrer les coords')
    
    service = Service.objects.all()
    filter = ServiceFilter(request.GET, queryset = service )
    services = filter.qs
    context = {'services' : services, 'filter' : filter,  'service' : service}
    #serializer_class = AdSerializer
    return render(request, 'simba/service.html', context)

def profilefournisseur(request) :
    #point = input('Entrer les coords')
    
    pservice = UserProfile.objects.all()
    pfilter = FournisseurFilter(request.GET, queryset = pservice )
    pservices = pfilter.qs
    context = {'pservices' : pservices, 'pfilter' : pfilter,  'pservice' : pservice}
    #serializer_class = AdSerializer
    return render(request, 'simba/fournisseur2.html', context)




class SousClassFilter(BaseFilter):
    search_fields = {
        'search_text' : ['Statut', 'types'],
        #'search_age_exact' : { 'operator' : '__exact', 'fields' : ['age'] },
        #'search_age_min' : { 'operator' : '__gte', 'fields' : ['age'] },
        #'search_age_max' : { 'operator' : '__lte', 'fields' : ['age'] },  
    }

class BarFilter(SearchListView):
    model = MonOffre
    #
    # paginate_by = 30
    template_name = "simba/recherche.html"
    form_class = SearchForm
    filter_class = SousClassFilter


def home(request):
   if request.method == 'GET':    
       notes = Notes.objects.filter(user=request.user)
       #items = Items.objects.all()
       return render(request,
           "simba/notes.html",
           {'Notes':notes})
   elif request.method == 'POST': 
       try:
           Notes.objects.create(name=request.POST['note_name'],
                               user=request.user)
       except:
           return HttpResponse("Note already exists!")
       else:
           notes = Notes.objects.filter(user=request.user)
           #items = Items.objects.all()
           return render(request,
               "simba/notes.html",
               {'Notes':notes})
        
        


def ticket_class_view(request):
    dataset = MonOffre.objects \
        .values('types') \
        .annotate(survived_count=Count('types', filter=Q(types = 'Villa')),
                  bureau_count=Count('types', filter=Q(types = 'Bureau')),
                  terrain_count=Count('types', filter=Q(types = 'Terrain')),
                  not_survived_count=Count('types', filter=Q(types = 'Appartement' ))) \
        .order_by('types')
    return render(request, 'simba/ticket_class.html', {'dataset': dataset})
