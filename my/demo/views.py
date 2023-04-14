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

class getAll(APIView):
    def get (self, request):
        list=CabinetLockerRentals.objects.all().select_related('customerid')
        mydata=CabinetLockerRentalsSerializer(list, many=True)
        return Response(data=mydata.data,status=status.HTTP_200_OK)
class getNumOfUsedCabinet(APIView):
    def get(self, request):
        count=Cabinet.objects.filter(aval=False).count()
        return Response({'count':count})


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
        target_encode=face_recognition.face_encodings(target_img)[0]

        #get candidate matches list
        matches=face_recognition.compare_faces(knowface_encodes,target_encode)
        #get closet img to the target
        face_distances = face_recognition.face_distance(knowface_encodes,target_encode)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            return Response({'face':knowface_name[best_match_index]})
        return Response(up_file.name, status.HTTP_201_CREATED)


