# from django.shortcuts import render

# Create your views here.
from django.urls import path, re_path
from bokeh_app import views
# Create your views here.

urlpatterns = [
    #path('', views.index, name='index'),

    # re_path('', views.showWebRequestView.as_view(), name="userinfo_list"),
    # re_path(r'^request_list', views.showWebRequestDetail.as_view(), name="userinfo_detail"),
    path('process', views.usrweb_view, name='usrweb_view'),
    path('',views.TestView.as_view(), name= "test"),
    # the name of the new
    # path('test', views.test_view, name='test_view'),
    # path('front', views.front_view, name='front_view'),
]
