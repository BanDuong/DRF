from django.contrib import admin
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('v1/index', views.index),
    # path('v1/person', views.person),
    path('v1/user/<id>', views.GetOneUser.as_view(), name="getOneUser"),
    # path('v1/login', views.login, name="login"),
    path('v1/person', views.PersonAPI.as_view(), name="person"),
    path('v1/registeruser', views.RegisterUser.as_view(), name="registerUser"),
    path('v1/getuser', views.GetUser.as_view(), name="getUser"),
    path('v1/login', views.LoginUser.as_view(), name="login"),
]

