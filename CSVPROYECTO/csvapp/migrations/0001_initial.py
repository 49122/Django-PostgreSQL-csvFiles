# Generated by Django 3.2 on 2021-04-23 20:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=95)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('client_id', models.IntegerField()),
                ('client_name', models.CharField(max_length=45)),
                ('dataset_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csvapp.dataset')),
            ],
        ),
    ]
