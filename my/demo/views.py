from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import CabinetLockerRentals, Cabinet, Customer
import face_recognition
from os import listdir
import numpy as np
import json
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
                'rentdate':record.rentdate.strftime("%H:%M %A %d %B, %Y"),
                'fee':record.fee ,              
            }
            data.append(record_data)

        return Response(data)
class getNumOfUsedCabinet(APIView):
    def get(self, request):
        count=Cabinet.objects.filter(avail=False).count()
        return Response({'count':count})
class getCabinet(APIView):
    def get(self, request):
        cabinets = Cabinet.objects.order_by('avail','id').select_related('userid')
        data = []
        for cabinet in cabinets:
            coord=cabinet.coord
            coord=json.loads(coord)
            position = f"Row   {coord['y']+1} Column   {coord['x']+1}"
            cabinet_data = {
                'id': cabinet.id,
                'position': position,
                'customer': None if cabinet.userid is None else cabinet.userid.name,
                'occupied':  not cabinet.avail,
                'date': None if not cabinet.start else cabinet.start.strftime("%H:%M %A %d %B, %Y")

                # Add any other fields you want to include in the response
            }
            data.append(cabinet_data)
        return Response(data)
class GetAllRentals(APIView):
    def get(self, request):
        rentals = CabinetLockerRentals.objects.select_related('customerid', 'cabinetid')
        data=[]
        for rental in rentals:
            cabinet=rental.cabinetid
            coord=cabinet.coord
            coord=json.loads(coord)
            position = f"Row   {coord['y']+1} Column   {coord['x']+1}"
            total_seconds=rental.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            tuple={
                'id':rental.id,
                'rentdate': rental.rentdate.strftime("%H:%M %A %d %B, %Y"),
                'pos':position,
                'name':rental.customerid.name,
                'duration': f"{hours} hours and {minutes} minutes",
                'paymentmethod': rental.paymentmethod,
                'fee':rental.fee,
            }
            data.append(tuple)
        return Response(data)
class GetAllCustomers(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        response = []
        for customer in customers:
            rentals = CabinetLockerRentals.objects.filter(customerid=customer)
            total_spent = sum(rental.fee for rental in rentals)
            customer_info = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                # 'phone': customer.phone,
                'total_spent': total_spent,
            }
            response.append(customer_info)
        return Response(response)
class getOcuppiedCabinet(APIView):
    def get(self, request):
        cabinets = Cabinet.objects.filter(avail=False).select_related('userid')
        data = []
        for cabinet in cabinets:
            cabinet_data={
                'id':cabinet.id,
                'path':cabinet.userid.image,
            }
            data.append(cabinet_data)
        return Response(data)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        up_file = request.FILES['file']
 # File should be closed only after all chuns are added

        img_files=listdir("./base_image")
        knowface_encodes=[]
        knowface_name=[]


        for img_file in img_files:
            #get img name
            knowface_name.append(img_file.split(".")[0])

            #get encode
            img=face_recognition.load_image_file('./base_image/'+img_file)
            encode=face_recognition.face_encodings(img)[0]
            knowface_encodes.append(encode)

        #get img from request

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



class RentalRevenueView(APIView):
    def get(self, request):
        # Get the current date
        today = date.today()

        # Calculate the start of the last 30 days and last 7 days
        start_of_last_30_days = today - timedelta(days=29)
        start_of_last_7_days = today - timedelta(days=6)

        # Get the total revenue for all rentals
        total_revenue = CabinetLockerRentals.objects.aggregate(total_revenue=Sum('fee'))['total_revenue'] or 0

        # Get the revenue for rentals in the last 30 days
        last_30_days_revenue = CabinetLockerRentals.objects \
            .filter(rentdate__date__range=[start_of_last_30_days, today]) \
            .aggregate(last_30_days_revenue=Sum('fee'))['last_30_days_revenue'] or 0

        # Get the revenue for rentals in the last 7 days
        last_7_days_revenue = CabinetLockerRentals.objects \
            .filter(rentdate__date__range=[start_of_last_7_days, today]) \
            .aggregate(last_7_days_revenue=Sum('fee'))['last_7_days_revenue'] or 0

        # Return a JSON response with the revenue data
        data = {
            'total': total_revenue,
            'monthly': last_30_days_revenue,
            'weekly': last_7_days_revenue,
        }
        return Response(data)