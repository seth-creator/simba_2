# Generated by Django 4.0.4 on 2022-05-27 16:04

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mapbox_location_field.spatial.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeBoundary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_code', models.CharField(max_length=10)),
                ('données', models.CharField(max_length=50)),
                ('data_set', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=254)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('type', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Banque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Boulangerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Commerce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Commissariat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Culte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Ecole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='FastFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='LimQuart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_commune', models.IntegerField(null=True, verbose_name='')),
                ('nom', models.CharField(choices=[('Riviera 4', 'Riviera 4'), ('Riviera 3', 'Riviera 3'), ('Palmeraie', 'Palmeraie'), ('7e Tranche', '7e Tranche'), ('9e Tranche', '9e Tranche')], max_length=200, null=True, verbose_name='Quartier')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='MonOffre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(choices=[('A vendre', 'A vendre'), ('A louer', 'A louer')], max_length=200, null=True, verbose_name='Offre')),
                ('types', models.CharField(choices=[('Bureau', 'Bureau'), ('Villa', 'Villa'), ('Appartement', 'Appartement'), ('Residence meublée', 'Residence meublée'), ('Terrain', 'Terrain')], max_length=200, null=True, verbose_name='Type de bien')),
                ('piece', models.FloatField(null=True, verbose_name='Nombre de pièce')),
                ('superficie', models.FloatField(null=True)),
                ('tarif', models.FloatField(null=True, verbose_name='Mon tarif')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Vue générale')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Vue de la chambre')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Vue de la douche')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('document', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('commentaire', models.TextField(max_length=200, null=True)),
                ('commune', models.CharField(choices=[('Abobo', 'Abobo'), ('Adjamé', 'Adiamé'), ('Anyama', 'Anyama'), ('Attecoubé', 'Attecoubé'), ('Cocody', 'Cocody'), ('Koumassi', 'Koumassi'), ('Port-bouet', 'Port-bouet'), ('Treichville', 'Treichville'), ('Songon', 'Songon'), ('Yopougon', 'Youpougon'), ('Plateau', 'Plateau'), ('Marcory', 'Marcory')], max_length=200, null=True, verbose_name='Commune')),
                ('quartier', models.CharField(choices=[('Riviera 4', 'Riviera 4'), ('Riviera 3', 'Riviera 3'), ('Palmeraie', 'Palmeraie'), ('7e Tranche', '7e Tranche'), ('8e Tranche', '8e Tranche'), ('9e Tranche', '9e Tranche'), ('Angré', 'Angré'), ('Les Versants', 'Les Versants'), ('Les Perles', 'Les Perles'), ('Danga Nord', 'Danga Nord'), ('Ambassade', 'Ambassade'), ('Danga Sud', 'Danga Sud'), ('Riviera Golf', 'Riviera Golf'), ('Bessikoi - Djorogobité', 'Bessikoi - Djorogobité'), ('Angré Extension', 'Angré Extension')], max_length=200, null=True, verbose_name='Quartier')),
                ('contact', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('agence', models.CharField(max_length=200, null=True, verbose_name='Nom du fournisseur')),
                ('description', models.TextField(max_length=200, null=True)),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='Localiser votre bien')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=50)),
                ('survived', models.BooleanField()),
                ('age', models.FloatField()),
                ('ticket_class', models.PositiveSmallIntegerField()),
                ('embarked', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, default='', max_length=100)),
                ('secteur', models.CharField(blank=True, default='', max_length=100)),
                ('caract1', models.CharField(blank=True, default='', max_length=100)),
                ('caract2', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, max_length=255, null=True, upload_to=('main.UserProfile.photo', 'profiles'), verbose_name='Profile Picture')),
                ('website', models.URLField(blank=True, default='')),
                ('bio', models.TextField(blank=True, verbose_name='Description')),
                ('phone', models.CharField(blank=True, default='', max_length=20)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100)),
                ('organization', models.CharField(blank=True, default='', max_length=100)),
                ('geom', mapbox_location_field.spatial.models.SpatialLocationField(map_attrs={}, null=True, srid=4326, verbose_name='localiser le fournisseur')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.IntegerField(blank=True)),
                ('monoffre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simba_app.monoffre')),
            ],
        ),
        migrations.AddField(
            model_name='monoffre',
            name='fournisseur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simba_app.userprofile'),
        ),
        migrations.CreateModel(
            name='Commentaires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='')),
                ('offre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='simba_app.monoffre')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
    ]
