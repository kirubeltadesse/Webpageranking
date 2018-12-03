from django.contrib import messages
from django.shortcuts import render, redirect
from bokeh_app.forms import WebForm
#just to see the models
from bokeh_app.models import WebInfo, ParaInfo
from bokeh_app.process_input import helper
# from django.core import serializers
# view types
from django.utils import timezone
# from django.views.generic import ListView, DetailView, TemplateView

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

#********************************* bokeh server imports ************************
from bokeh.embed import server_document
from . import bk_config

#***************************** connecting with the JavaScript file *************
import sys
from Naked.toolshed.shell import execute_js, muterun_js

#***************************** rest_framework **********************************
from django.contrib.auth.models import User, Group



def usrweb_view(request):
    print("in usrweb_view")
    # HttpResponseRedirect("bokeh_app/plot.html")
    params = {}
    # taking the last website from the databased and calling the parameters
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
        # dic_para = ParaInfo.objects.values().filter(web_address= WebInfo.objects.values('website').order_by('-created_date')[0]['website'])[0]
        helper(2).write_model_toCSV(data_dic)
        # write_model_toCSV(data_dic)

    else:
        print("FAILED")
        sys.stderr.write(str(response.stderr))
    # print(msg)
    return render(request, "bokeh_app/process.html")

# Create your views here.
def index(request):
    registered = False
    if request.method == "POST":
        website_form = WebForm(data=request.POST)
        if website_form.is_valid():
            websiteInput = website_form.save() #(commit=False)
            websiteInput.save()

            registered = True
            # messages.success(request,'Form submission successful')
        else:
            print(website_form.errors)
        # messages.add_message(request, messages.INFO, "please wait patiently as we collect the parameters for the website!")
    else:
        # user_form = UserForm()
        website_form = WebForm()

    #Feed them to the Django template.
    return render(request, 'bokeh_app/index.html',{'website_form':website_form,
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


def sidebyside(request):
    return render(request, 'bokeh_app/sidebyside.html',{
    "server_script": server_document('http://%s:%s/bk_sliders_tab'%(bk_config.server['address'],
                                                                    bk_config.server['port'])),
    "den_script": server_document('http://%s:%s/bk_sliders_den'%(bk_config.server['address'],
                                                                    bk_config.server['port'])),
    "his_script": server_document('http://%s:%s/bk_sliders_hist'%(bk_config.server['address'],
                                                                   bk_config.server['port'])),
    "rank_script": server_document('http://%s:%s/bk_sliders_bar'%(bk_config.server['address'],
                                                                    bk_config.server['port'])),
                                                                })
