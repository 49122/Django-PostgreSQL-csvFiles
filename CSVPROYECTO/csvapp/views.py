# Django imports
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.core.files import File
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
# Utilitis
import os
import csv
import pandas as pd
import collections
import re
from .models import Dataset,Row
import numpy as np


# Create your views here.

class Csv(View):

    def get(self, request):
        registros = Dataset.objects.all()
        p = Paginator(registros, 5)
        page_num = request.GET.get('page',1)
        valor = int(page_num)+1
        valor = str(valor)
        message = 'http://127.0.0.1:8000/api/v1/datasets/?page='+valor
        
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        lista = [x for x in page]

        context = {
            'mensaje': message,
            'TotalPages':p.num_pages
            }

        for i in range(len(lista)):
            context[i] = {
                'Name': lista[i].name,
                'Upload_date': lista[i].date,
            }

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        time_of_request = timezone.now()


        logger_info = {}
        logger_info['ip'] = ip
        logger_info['time'] = str(time_of_request)
        logger_info['user'] = request.META['HTTP_USER_AGENT']

        with open('./debug.log','a') as f:
            myfile = File(f)
            myfile.write('{}\n'.format(str(logger_info)))
        

        return JsonResponse(context)






    def post(self, request, *args, **kwarg):
        
        csv_file = request.FILES['csv']

        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('File is not csv')

        # Validate file size
        if csv_file.multiple_chunks():

            return HttpResponse('File is to heavy')

        # Pandas DataFrame 
        df = pd.read_csv(csv_file,index_col=False)

        # Headers validation
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        headers = ['dataset_id', 'latitude', 'longitude', 'client_id', 'client_name']
        if not compare(df.columns.tolist(),headers):
            return HttpResponse("Headers of file are invalid, need to be like so: 'dataset_id', 'latitude', 'longitude', 'client_id', 'client_name'")
        

        dataset_name = request.POST['name']

        # Dataset existence validation
        try:
            Dataset.objects.get(name=dataset_name)
            return HttpResponse('Dataset already in existance in our database')
        except Exception:
            pass

        

        # Validating Data within the dataset 
        if not df['dataset_id'].dtypes == 'int64':
            return HttpResponse('dataset_id column needs to be integer type')


        if df['latitude'].dtypes == 'int64':
            pass
        elif df['latitude'].dtypes == 'float64':
            pass
        else:
            return HttpResponse('latitud column needs to be either integer or float')


        if df['longitude'].dtypes == 'int64':
            pass
        elif df['longitude'].dtypes == 'float64':
            pass
        else:
            return HttpResponse('longitude column needs to be either integer or float')

        
        if not df['client_id'].dtypes == 'int64':
            return HttpResponse('dataset_id column needs to be integer type')


        upload_date = timezone.now()
        dataset = Dataset(name=dataset_name,date=upload_date)
        dataset.save()

        df['point'] = df[['latitude','longitude']].values.tolist()

        
        for i in range(len(df)):
            try:
                d = Dataset.objects.get(id=df.iloc[i, 0])
            except:
                return HttpResponse('There is no dataset with the id that the row number:{} is giving'.format(i+1))
            
            point_object = Point(df.iloc[i, 5])

            row = Row(dataset_id=d, point=point_object, client_id=df.iloc[i, 3], client_name=df.iloc[i, 4])
            row.save()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        time_of_request = timezone.now()

        logger_info = {}
        logger_info['ip'] = ip
        logger_info['time'] = str(time_of_request)
        logger_info['user'] = request.META['HTTP_USER_AGENT']

        with open('./debug.log', 'a') as f:
            myfile = File(f)
            myfile.write('{}\n'.format(str(logger_info)))

        return HttpResponse('To bien')

class RowView(View):

    def get(self,request):

        try:
            id_dataset = request.GET.get('dataset_id')
        except:
            return HttpResponse('You did not send an id as a params')

        data = Dataset.objects.get(id=id_dataset)
        registros = Row.objects.filter(dataset_id=data)

        lista = [x for x in registros]

        bundle = []
        paquete = {}

        for i in range(len(lista)):
            point = [x for x in lista[i].point]
            bundle.append({
                'client_name': lista[i].client_name,
                'client_id': lista[i].client_id,
                'dataset_id': lista[i].dataset_id.id,
                'point': point
            })

        paquete['Data'] = bundle

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        time_of_request = timezone.now()

        logger_info = {}
        logger_info['ip'] = ip
        logger_info['time'] = str(time_of_request)
        logger_info['user'] = request.META['HTTP_USER_AGENT']

        with open('./debug.log', 'a') as f:
            myfile = File(f)
            myfile.write('{}\n'.format(str(logger_info)))
        return JsonResponse(paquete)



class TableView(View):

    def get(dels,request):
        context = []
        
        with open('./debug.log', 'r') as f:
            myfile = File(f)
            lineas = myfile.readlines()
            for linea in lineas:
                to_dict = eval(linea)
                context.append(to_dict)
        
        
        return render(request,'csvapp/index.html',{'lineas':context})
