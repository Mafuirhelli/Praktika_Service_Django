from . import views
from django.urls import re_path
from django.urls import path

urlpatterns = [
 re_path(r'^$', views.index, name='index'),
 path('register/', views.sign_up, name='register'),
 path('loginuser/', views.sign_in, name='loginuser'),
 path('userpage/', views.user_page, name='userpage'),
]