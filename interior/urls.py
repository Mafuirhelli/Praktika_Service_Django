from . import views
from django.urls import re_path
from django.urls import path

urlpatterns = [
 re_path(r'^$', views.index, name='index'),
 path('register/', views.sign_up, name='register'),
 path('loginuser/', views.sign_in, name='loginuser'),
 path('userpage/', views.user_page, name='userpage'),
 re_path(r'^query/create/$', views.QueryCreate.as_view(), name='query_create'),
 re_path(r'^query/create/$', views.query_create, name='query_create'),
 re_path(r'^query/(?P<pk>\d+)$', views.QueryDetailView.as_view(), name='query-detail'),
 re_path(r'^querys/$', views.QueryListView.as_view(), name='querys'),
 re_path(r'^querysn/$', views.QueryListView.as_view(), name='querys_n'),
 re_path(r'^querysa/$', views.QueryListView.as_view(), name='querys_a'),
 re_path(r'^querysd/$', views.QueryListView.as_view(), name='querys_d'),

 re_path(r'^query/(?P<pk>\d+)/delete/$', views.QueryDelete.as_view(), name='query_delete'),
]