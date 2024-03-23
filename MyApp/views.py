import jwt
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
# from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person
from .serializers import (GetAllUserSerializer, LoginJWTSerializer,
                          LoginSerializer, PersonSerializer,
                          RegisterSerializer)

# Create your views here.


class GetOneUser(APIView):
    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        token = request.COOKIES.get('jwtToken')
        if not token:
            raise AuthenticationFailed("Token is not available")
        
        try:
            payload = jwt.decode(token, key='secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthentication Token")
            
        
        user = User.objects.get(id=payload['id'])
        serializer = GetAllUserSerializer(instance=user)
        return Response(serializer.data)  

class LoginJWT(APIView):
    
    def post(self, request):
        data = request.data
        serializer = LoginJWTSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({"error": "Invalid Data"}, status=400)
        
        respone = Response()
        respone.set_cookie(key='jwtToken', value=serializer.validated_data['token'])
        respone.data = {
            'data': serializer.validated_data
        }    
            
        return respone


class LogoutJWT(APIView):
    
    def post(self, request):
        response = Response()
        response.delete_cookie('jwtToken')
        response.data = {
            "message": "Successfully logout"
        }
        return response
          
class LoginUser(APIView):
    
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({"error": "Invalid Data"}, status=400)
        
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])    
        return Response({"success": True,
                         "user": serializer.data,
                         "token": token.key
                         }, status=200)

class RegisterUser(APIView):
    
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class GetUser(APIView):
    
    def get(self, request):
        users = User.objects.all()
        serializer = GetAllUserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def index(request):
    data = {
        'title': 'Hello World',
        'content': 'This is a test page.'
    }
    
    return Response(data)

@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def person(request):
    if request.method == 'GET':
        obj = Person.objects.all()
        serializerObj = PersonSerializer(obj, many=True)
        return Response(serializerObj.data)
    elif request.method == 'POST':
        data = request.data
        serializerObj = PersonSerializer(data=data)
        if serializerObj.is_valid():
            serializerObj.save()
            return Response(serializerObj.data)
        else:
            return Response(serializerObj.errors, status=400)
    elif request.method == 'PATCH':
        data = request.data
        serializerObj = PersonSerializer(data=data, partial=True)
        if serializerObj.is_valid():
            serializerObj.save()
            return Response(serializerObj.data)
        else:
            return Response(serializerObj.errors, status=400)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def getOnePerson(request, id):
    if request.method == 'GET':
        obj = Person.objects.get(id=id)
        serializerObj = PersonSerializer(obj)
        return Response(serializerObj.data)
    elif request.method == 'PATCH':
        obj = Person.objects.get(id=id)
        data = request.data
        serializerObj = PersonSerializer(instance=obj, data=data)
        if serializerObj.is_valid():
            serializerObj.save()
            return Response(serializerObj.data)
        else:
            return Response(serializerObj.errors, status=400)
    elif request.method == 'DELETE':
        obj = Person.objects.get(id=id)
        obj.delete()
        return Response(status=204, data="delete person sucessful!")

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=201)
    else:
        return Response(serializer.errors, status=400)  # Bad request

# Remake Person CRUD
class PersonAPI(APIView):
    
    def get(self, request):
        obj = Person.objects.all()
        serializerObj = PersonSerializer(obj, many=True)
        return Response(serializerObj.data)

    