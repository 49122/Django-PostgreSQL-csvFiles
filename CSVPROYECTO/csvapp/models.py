from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils import timezone
# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=95)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Row(models.Model):
    dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    point = models.PointField()
    client_id = models.IntegerField()
    client_name = models.CharField(max_length=45)
