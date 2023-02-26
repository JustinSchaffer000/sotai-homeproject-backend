from django.contrib.auth import login

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from . import serializers
import csv

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']

        return JsonResponse({'username': username})
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

def csv_to_json(csvFilePath, year):
    jsonArray = []
      
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            if row['year'] == str(year):
                jsonArray.append(row)
  
    return jsonArray

def year_data(request, year) :
    if request.method == 'GET':
        csvFilePath = settings.BASE_DIR / 'cpu_hours.csv'
        
        return JsonResponse({
            'message': 'success',
            'data': csv_to_json(csvFilePath, year)})


