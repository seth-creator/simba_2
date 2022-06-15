from django import forms
from leaflet.admin import LeafletGeoAdmin

from leaflet.forms.widgets import LeafletWidget

from simba_app.models import MonOffre, Commentaires

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth.models import User
from django import forms
from import_export import resources

class MonMapWidget(LeafletWidget):
    geometry_field_class = 'geom'

class MonOffreForm(forms.ModelForm):

    class Meta:
        model = MonOffre
        fields = ('statut','types','piece','superficie','tarif', 'commune','image', 'image2','image3','video', 'document', 'commentaire', 'agence','description','contact' ,'email','date','geom' )
        """widgets = {'geom': LeafletWidget(attrs={
            'settings_overrides': {
            'DEFAULT_CENTER': (5.39460 , -3.97684),
            'map_height': 100,
            'map_width': 30,
        
            }

        })}"""
        default_map_attrs = {  
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 15,
            "center": [5.39460 , -3.97684],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True, 
            "readonly": True,
            "placeholder": "Choisissez un lieu sur la carte ci-dessous", 
            "language": "auto",
            "message_404": "undefined address",
             
            
             }





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# formulaire pour contacter 
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class SearchForm(forms.Form):
    search_text =  forms.CharField(
        required = False,
        label='Search statut or types!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )
    
    
class BookResource(resources.ModelResource):
    class Meta:
        model = MonOffre
        fields = ('statut', 'types', 'tarif',)
        
        
class NoteForm(forms.ModelForm):
    class Meta :
        model = Commentaires
        fields= ['text','user','offre']
        
class NotationForm(forms.Form):
    note_note = forms.CharField(widget=forms.Textarea)


        