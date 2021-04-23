from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=95)
    date = models.DateField()

class Row(models.Model):
    dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    point = models.PointField()
    client_id = models.IntegerField()
    client_name = models.CharField(max_length=45)
