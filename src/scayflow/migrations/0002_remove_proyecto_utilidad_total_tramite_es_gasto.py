# Generated by Django 5.2.3 on 2025-07-15 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scayflow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='utilidad_total',
        ),
        migrations.AddField(
            model_name='tramite',
            name='es_gasto',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
