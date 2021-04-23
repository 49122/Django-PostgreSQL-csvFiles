from django.urls import path

from . import views

urlpatterns = [
    path('', views.addcsv, name='addcsv'),
]