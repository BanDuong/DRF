import datetime

import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import Color, Person

# from DRF.settings import SECRET_KEY



class LoginJWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        print(hasattr(token, 'decode'))
        attrs['token'] = token
        return attrs
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        attrs['user'] = user
        return attrs
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        attrs['user'] = user
        return attrs
        
    

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'
        


class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    color_infor = serializers.SerializerMethodField() 
    
    class Meta:
        model = Person
        # exclude = ('name', 'email')  # Exclude these fields in the
        # fields = ('id', 'name', 'age')
        fields = '__all__'
        # depth = 10 # 0<depth<=10 ----> show how many fields are in Color model
    
    def get_color_infor(self, attr):
        color = Color.objects.get(id = attr.color.id)
        return {
            'color_name': color.color_name,
            'color_id': color.id
        }     
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def validate_name(self, attrs):
        specical_characters = "!@+=-._-?/~<>()#$%^&*,;'"
        if any(c in specical_characters for c in attrs):
            raise serializers.ValidationError('Name cannot contain special characters')
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField()        
    
    def validate(self, attrs):
        # if attrs['password'] and User.objects.filter(username=attrs['password']).exists():
        #     raise serializers.ValidationError('Password already exists')
        
        if attrs['email'] and User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email is already registered')
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   
        # user.is_staff = True
        return user
    
class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



                     
        