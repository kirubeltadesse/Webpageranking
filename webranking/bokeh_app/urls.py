# from django.shortcuts import render
# Create your views here.
from django.urls import path, re_path
from bokeh_app import views

from rest_framework.routers import DefaultRouter
# Create your views here.

router = DefaultRouter()
# app_name = 'bokeh_app'
urlpatterns = [
    #path('', views.index, name='index'),

    # re_path('', views.showWebRequestView.as_view(), name="userinfo_list"),
    # re_path(r'^request_list', views.showWebRequestDetail.as_view(), name="userinfo_detail"),
    # path('process', views.process, name='process'),
    path('process', views.usrweb_view, name='usrweb_view'),
    path('barranking',views.barrank_tab, name= "barrank"),
    path('histogram',views.histogram_tab, name= "histogram"),
    path('density',views.density_tab, name= "density"),
    path('table',views.table_tab, name= "table"),
    path('sidebyside', views.sidebyside, name="sidebyside"),
]
