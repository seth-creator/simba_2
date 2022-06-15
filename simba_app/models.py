from django.db import models

# Create your models here.

from django.contrib.gis.db import models
from django.core.files.storage import FileSystemStorage
from mapbox_location_field.spatial.models import SpatialLocationField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator

#fs = FileSystemStorage(location='/media/photos')

class MonOffre(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    STATUT = (('A vendre', 'A vendre'),
                ('A louer', 'A louer'))
    statut = models.CharField('Offre',max_length = 200, null = True, choices = STATUT,)
    def __str__(self) :
        return self.statut
    TYPE = (('Bureau', 'Bureau'),
              ('Villa', 'Villa'),
                ('Appartement', 'Appartement'),
                ('Residence meublée', 'Residence meublée'),
                ('Terrain', 'Terrain'))
    types = models.CharField('Type de bien', max_length = 200, null = True, choices = TYPE )
    def __str__(self) :
        return self.types
    piece = models.IntegerField('Nombre de pièce', null=True)
    superficie = models.FloatField(null=True)
    tarif = models.IntegerField('Mon tarif',null = True)
    image = models.ImageField('Vue générale',null = True, blank = True, upload_to ='uploads/')
    image2 = models.ImageField('Vue de la chambre',null = True, blank = True, upload_to ='uploads/')
    image3 = models.ImageField('Vue de la douche',null = True, blank = True, upload_to ='uploads/')
    #PDF = models.FileField('document',null = True, blank = True, upload_to ='uploads/')

    video = models.FileField(upload_to='videos_uploaded',null=True, blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    document = models.FileField(null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    commentaire = models.TextField(max_length=200, null=True)
    comm = (('Abobo', 'Abobo'),
                ('Adjamé', 'Adiamé'),
                ('Anyama', 'Anyama'),
                ('Attecoubé', 'Attecoubé'),
                ('Cocody', 'Cocody'),
                ('Koumassi', 'Koumassi'),
                ('Port-bouet', 'Port-bouet'),
                ('Treichville', 'Treichville'),
                ('Songon', 'Songon'),
                ('Yopougon', 'Youpougon'),
                ('Plateau', 'Plateau'),
                ('Marcory', 'Marcory')
                )
    commune = models.CharField('Commune', null = True, max_length = 200, choices = comm)
    qua = (('Riviera 4', 'Riviera 4'),
                ('Riviera 3', 'Riviera 3'),
                ('Palmeraie', 'Palmeraie'),
                ('7e Tranche', '7e Tranche'),
                ('8e Tranche', '8e Tranche'),
                ('9e Tranche', '9e Tranche'),
                ('Angré', 'Angré'),
                ('Les Versants', 'Les Versants'),
                ('Les Perles', 'Les Perles'),
                ('Danga Nord', 'Danga Nord'),
                ('Ambassade', 'Ambassade'),
                ('Danga Sud', 'Danga Sud'),
                ('Riviera Golf', 'Riviera Golf'),
                ('Bessikoi - Djorogobité', 'Bessikoi - Djorogobité'),
                ('Angré Extension', 'Angré Extension'),
                )
    quartier = models.CharField('Quartier', null = True, max_length = 200, choices = qua)
    contact = models.IntegerField(null =True)
    email = models.EmailField(null=True, max_length = 200)
    agence = models.CharField("Nom du fournisseur", max_length = 200, null = True)
    description = models.TextField(max_length=200, null=True)
    date = models.DateField('Date', null=True,)
    fournisseur = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null =True)
    #notation = models.ForeignKey('Notation', on_delete = models.CASCADE)
    #notes = models.ForeignKey('Notation', on_delete = models.CASCADE, null = True)
    #lon = models.FloatField()
    #lat = models.FloatField()
    geom = SpatialLocationField('Localiser votre bien',blank = False, null = True)

    #objects = models.GeoManager()
    
    #rast = models.RasterField(null=True)
    #subregion = models.IntegerField('Sub-Region Code')
    

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    #mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
class AdministrativeBoundary(models.Model):
    data_code = models.CharField(max_length=10)
    données = models.CharField(max_length=50)
    data_set = models.CharField(max_length=50)
    nom = models.CharField(max_length=254)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    type = models.IntegerField()
    geom = models.PolygonField(srid=4326)
    
class Route (models.Model):
    name = models.CharField(max_length=50, null = True)
    geom = models.MultiLineStringField(srid=4326, null = True)


"""class UserModuleProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    expired = models.DateTimeField()
    admin = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=50)
    organisation_name = models.ForeignKey('Organizations', on_delete=models.PROTECT)
    country = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user"""

#models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='user')
    photo = models.ImageField(verbose_name=_("Profile Picture"),
            upload_to=("main.UserProfile.photo", "profiles"),
            max_length=255, null=True, blank=True)
    #image = models.ImageField('photo',null = True, blank = False, upload_to ='uploads/')
    website = models.URLField(default='', blank=True)
    bio = models.TextField('Description', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)
    geom = SpatialLocationField('localiser le fournisseur', null = True)
     
    
    def __str__(self):
        return self.organization
    
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Service(models.Model):
    nom = models.CharField(max_length=100, default='', blank=True)
    secteur = models.CharField(max_length=100, default='', blank=True)
    caract1 = models.CharField(max_length=100, default='', blank=True)
    caract2 = models.CharField(max_length=100, default='', blank=True)
    #geo_location = models.PointField()
    #location = SpatialLocationField(null = True)
    
class LimQuart(models.Model):
    id_commune = models.IntegerField('', null = True)
    quar = (('Riviera 4', 'Riviera 4'),
                ('Riviera 3', 'Riviera 3'),
                ('Palmeraie', 'Palmeraie'),
                ('7e Tranche', '7e Tranche'),
                ('9e Tranche', '9e Tranche'),
                )
    nom = models.CharField('Quartier', null = True, max_length = 200, choices = quar)
    
    geom = models.PolygonField(srid=4326, null = True)
    
    
    
    
"""('Akouedo Extension Nord', 'Akouedo Extension Nord'),
                ('Les Versants', 'Les Versants'),
                ('Les Perles', 'Les Perles'),
                ('Ephrata', 'Ephrata'),
                ('Commandant Sanon', 'Commandant Sanon'),
                ('Le Vallon', 'Le Vallon'),
                ('Aghien', 'Aghien'),
                ('Riviera Bonoumin', 'Riviera Bonoumin'),
                ('Nouveau Camp', 'Nouveau Camp'),
                ('Colombie', 'Colombie'),
                ('Attoban', 'Attoban'),
                ('SICOGI', 'SICOGI'),
                ('TF 233', 'TF 233'),
                ('SYNATRESOR', 'SYNATRESOR'),
                ('Faya', 'Faya'),
                ('ATCI', 'ATCI'),
                ('Adjame Village', 'Adjame Village'),
                ('1ere Tranche', '1ere Tranche'),
                ('Palmeraie Triangle', 'Palmeraie Triangle'),
                ('Agban', 'Agban'),
                ('Mbadon-Akouedo', 'Mbadon-Akouedo'),
                ('2e Tranche', '2e Tranche'),
                ('Ancien camp', 'Ancien camp'),
                ('Riviera Allabra', 'Riviera Allabra'),
                ('Riviera Golf', 'Riviera Golf'),
                ('Ambassade', 'Ambassade'),
                ('Danga Nord', 'Danga Nord'),
                ('Mpouto Village', 'Mpouto Village'),
                ('Angre Extension', 'Angre Extension'),
                ('Bessikoi - Djorogobite', 'Bessikoi - Djorogobite'),
                ('8e Tranche', '8e Tranche'),
                ('Dokui', 'Dokui'),
                ('Cite des Arts', 'Cite des Arts'),"""
                
                
class Hotel(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Hopital(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class FastFood(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Ecole(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Station(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Pharmacie(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Culte(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Commissariat(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Commerce(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Cinema(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Cafe(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Boulangerie(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
class Banque(models.Model):
    nom = models.CharField(null = True, max_length = 100)
    geom = SpatialLocationField('',blank = False, null = True)
    def __str__(self):
        return self.nom
    
    
class Notes(models.Model):
   name = models.CharField(max_length=30)
   user = models.ForeignKey(User, default=1,
                       on_delete= models.CASCADE)  #here
   def __str__(self):
       return str(self.id)+": "+self.name
   class Meta:                                     # here
       unique_together = ('user','name')           # here
       
       
class Passenger(models.Model):
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    survived = models.BooleanField()
    age = models.FloatField()
    ticket_class = models.PositiveSmallIntegerField()
    embarked = models.CharField(max_length =50)
    
class Commentaires(models.Model) :
    text = models.TextField('',max_length = 200)
    user = models.ForeignKey(User, null = True,on_delete = models.CASCADE)
    offre = models.ForeignKey(MonOffre,null = True, on_delete = models.CASCADE, blank = True)
    
    
class Notation(models.Model):
    note = models.IntegerField(blank = True)
    monoffre = models.ForeignKey('MonOffre', null = True, on_delete = models.CASCADE)
    #def __str__(self):
        #return self
    
    
