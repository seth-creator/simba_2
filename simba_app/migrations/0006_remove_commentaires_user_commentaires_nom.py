# Generated by Django 4.0.4 on 2022-06-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simba_app', '0005_alter_monoffre_piece'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentaires',
            name='user',
        ),
        migrations.AddField(
            model_name='commentaires',
            name='nom',
            field=models.CharField(blank=True, max_length=200, verbose_name=''),
        ),
    ]
