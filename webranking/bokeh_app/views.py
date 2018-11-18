#**************** view import *************************************************
from django.shortcuts import render, redirect
from bokeh_app.forms import UserForm
from bokeh_app.forms import WebForm
#just to see the models
from bokeh_app.models import WebInfo, ParaInfo
# from django.core import serializers
# view types
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView

# Create your views here.
import logging
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from bokeh.embed import server_document

from . import bk_config

#***************************** connecting with the JavaScript file ********************
import sys
from Naked.toolshed.shell import execute_js, muterun_js

#***************************** rest_framework ****************************************
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from bokeh_app.serializers import UserSerializer, GroupSerializer
from rest_framework.renderers import JSONRenderer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # return JSONRenderer(serializer_class)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TestView(TemplateView):
    template_name = 'bokeh_app/test.html'



def usrweb_view(request):
    params = {}
    # taking the last website from the databased and calling the parameters
    print("in usrweb_view")
    usrWebSite = WebInfo.objects.values('website').order_by('-created_date')[0]['website']
    response = muterun_js('webtest_analysis.js', usrWebSite)
    # data = serializers.serialize("json", response)
    params['web_address'] = usrWebSite


    def prepare(data_in):
        content= data_in
        line = content.split('\n')

        for each in line:
            values=each.split(':')

            # lenght should be two
            if len(values) == 2:
                key, value = values
                params[key] = value
            elif len(values) == 1:
                print("value is 1: ", values)
            else:
                print("in the else ",len(values), " ", values)
        return params

    def renameParms(data):
        mod_dic = {}
        key = {'web_address':'', "load_time":'', "first_byte":'', "start_render":'', "speed_Index":'', "dom_elements":'', "doc_complete_Requests":'', "doc_complete_Byets":'',"fully_time":'', "fully_requests":'', "fully_bytes":''}
        for parm, val in zip(key.keys(),data.values()):
            # print(parm," ", val)
            mod_dic[parm] = val

        return mod_dic

    if response.exitcode == 0:
        print("SUCCEED")
        # print(response.stdout)
        data = str((response.stdout).decode('utf8').replace("'",'"'))
        start = data.find('Load time')
        end = data.find('Waterfall view')
        #passing the SELECTED (SLISED) result to a dictionary
        print(prepare(data[start:end]))
        data_dic = renameParms(prepare(data[start:end]))
        # passing the dictionary to the model
        ParaInfo.objects.create(**data_dic)
    else:
        print("FAILED")
        sys.stderr.write(str(response.stderr))
    # print(msg)
    return render(request, "bokeh_app/process.html")
# Create your views here.
def index(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        website_form = WebForm(data=request.POST)

        if user_form.is_valid() and website_form.is_valid():

            user = user_form.save()
            user.save()
            # adding the created_date
            # UserInfo.create(self)

            website = website_form.save() #(commit=False)
            website.user = user

            website.save()

            registered = True
        else:
            print(user_form.errors, website_form.errors)
    else:
        user_form = UserForm()
        website_form = WebForm()

    #Feed them to the Django template.
    return render(request, 'bokeh_app/index.html',{'user_form':user_form,
                                                    'website_form':website_form,
                                                    "registered":registered})

def barrank_tab(request):
    return render(request, 'bokeh_app/bar.html', {
    "server_script": server_document('http://%s:%s/bk_sliders_bar'%(bk_config.server['address'],
                                                                    bk_config.server['port']))})

def density_tab(request):
    return render(request, 'bokeh_app/density.html', {
    "server_script": server_document('http://%s:%s/bk_sliders_den'%(bk_config.server['address'],
                                                                    bk_config.server['port']))})

def histogram_tab(request):
    return render(request, 'bokeh_app/histogram.html', {
    "server_script": server_document('http://%s:%s/bk_sliders_hist'%(bk_config.server['address'],
                                                                    bk_config.server['port']))})

def table_tab(request):
    return render(request, 'bokeh_app/table.html', {
    "server_script": server_document('http://%s:%s/bk_sliders_tab'%(bk_config.server['address'],
                                                                    bk_config.server['port']))})
