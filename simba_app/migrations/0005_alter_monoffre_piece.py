# Generated by Django 4.0.4 on 2022-06-22 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simba_app', '0004_alter_monoffre_piece'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monoffre',
            name='piece',
            field=models.CharField(max_length=10, null=True, verbose_name='Nombre de pièce'),
        ),
    ]
