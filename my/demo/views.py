from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import RentalsSer, usedCabinetCount,CabinetLockerRentalsSerializer
from .models import CabinetLockerRentals, Cabinet
import face_recognition
from os import listdir
import numpy as np
from datetime import date, timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay



class getAll(APIView):
    def get (self, request):
        rentals=CabinetLockerRentals.objects.order_by('-id').select_related('customerid')[:10]
        data=[]
        for record in rentals:
            record_data={
                'id':record.id,
                'customer_name':record.customerid.name,
                'rentdate':record.rentdate.strftime('%Y-%m-%d %H:%M:%S'),
                'fee':record.fee ,              
            }
            data.append(record_data)

        return Response(data)
class getNumOfUsedCabinet(APIView):
    def get(self, request):
        count=Cabinet.objects.filter(aval=False).count()
        return Response({'count':count})
class getCabinet(APIView):
    def get(self, request):
        cabinets = Cabinet.objects.order_by('aval','id').select_related('customerid')
        data = []
        for cabinet in cabinets:
            position = f"Row   {cabinet.coord['y']+1} Column   {cabinet.coord['x']+1}"
            cabinet_data = {
                'id': cabinet.id,
                'position': position,
                'customer': None if cabinet.customerid is None else cabinet.customerid.name,
                'occupied':  not cabinet.aval,
                # Add any other fields you want to include in the response
            }
            data.append(cabinet_data)
        return Response(data)

class getOcuppiedCabinet(APIView):
    def get(self, request):
        cabinets = Cabinet.objects.filter(aval=False).select_related('customerid')
        data = []
        for cabinet in cabinets:
            cabinet_data={
                'id':cabinet.id,
                'path':cabinet.customerid.image,
            }
            data.append(cabinet_data)
        return Response(data)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        up_file = request.FILES['file']
        #process target img
        target_img=face_recognition.load_image_file(up_file)
        encodes=face_recognition.face_encodings(target_img)
        if len(encodes)==0:
            return Response(data=[])
        
        target_encode=encodes[0]
        res=[]

        cabinets=Cabinet.objects.select_related('userid').filter(avail=False)
        for cabin in cabinets:
            img_path=cabin.userid.photo
            img=face_recognition.load_image_file("/home/hoangdeptrai/ki2nam3/do_an/backend/public/img/"+img_path)
            cur_encode=face_recognition.face_encodings(img)
            if face_recognition.compare_faces(cur_encode,target_encode)[0]:
                res.append(cabin.id)
        #get candidate matches list
        return Response(res)


class CabinetLockerRevenueView(APIView):
    def get(self, request, format=None):
        today = date.today()
        end_date = today  # get last Sunday
        start_date = end_date - timedelta(days=6)  # get last 7 days
        data = []
        for i in reversed(range(7)):
            weekday = (end_date - timedelta(days=i)).strftime('%A')
            revenue = CabinetLockerRentals.objects.filter(
                rentdate__date=end_date - timedelta(days=i)
            ).aggregate(Sum('fee'))['fee__sum'] or 0.0
            
            data.append({'x': weekday, 'y': float(revenue)})
            
        return Response(data)
