from . import views
from django.urls import re_path
from django.urls import path

urlpatterns = [
 re_path(r'^$', views.index, name='index'),
 path('register/', views.sign_up, name='register'),
 path('loginuser/', views.sign_in, name='loginuser'),
 path('userpage/', views.user_page, name='userpage'),
 re_path(r'^query/create/$', views.query_create, name='query_create'),
 re_path(r'^query/(?P<pk>\d+)$', views.QueryDetailView.as_view(), name='query-detail'),
 re_path(r'^querys/$', views.QueryListView.as_view(), name='querys'),
 re_path(r'^querysn/$', views.QueryListView.as_view(), name='querys_n'),
 re_path(r'^querysa/$', views.QueryListView.as_view(), name='querys_a'),
 re_path(r'^querysd/$', views.QueryListView.as_view(), name='querys_d'),
 re_path(r'^query/(?P<pk>\d+)/delete/$', views.QueryDelete.as_view(), name='query_delete'),
 re_path(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDelete.as_view(), name='category_delete'),
 re_path(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
 re_path(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create'),
 re_path(r'^adminpleas/$', views.AdminPleaListView.as_view(), name='adminpleas'),
 re_path(r'^query/(?P<pk>\d+)/complete/$', views.QueryAddDesign.as_view(), name='plea_complete'),
 re_path(r'^query/(?P<pk>\d+)/work/$', views.QueryAddComment.as_view(), name='plea_work'),
 re_path(r'^supermanage/$', views.SuperuserQueryListView.as_view(), name='supermanage'),
 re_path(r'^query/(?P<pk>\d+)/addmin/$', views.QueryAddAdmin, name='addmin'),
]