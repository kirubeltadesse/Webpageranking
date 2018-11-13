#**************** view import *************************************************
from django.shortcuts import render
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

#**************************** libraries for bokeh **********************************
import pandas as pd
import numpy as np

import os.path
from os.path import dirname, join

from bokeh.core.properties import value
from bokeh.transform import dodge

from scipy.stats import gaussian_kde

from bokeh.plotting import figure, show
from bokeh.models import (CategoricalColorMapper, HoverTool,
      ColumnDataSource, Panel,
      FuncTickFormatter, SingleIntervalTicker,LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
      Tabs, CheckboxButtonGroup,
      TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

#*************************** bokeh server imports ***********************************
from bokeh.resources import CDN
from bokeh.embed import components, file_html, server_session, server_document
from bokeh.server.server import Server

#
from bokeh.io import curdoc, show
from bokeh.client import push_session

#***************************** connecting with the JavaScript file ********************
import sys
from Naked.toolshed.shell import execute_js, muterun_js





BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, 'data')
print(BASE_DIR)
# Read data into dataframes
webs = pd.read_csv(os.path.join(RESOURCE_DIR, 'nor_time.csv'),
                                index_col=0).dropna()

#? need to from the model of the website
usrweb = webs.iloc[2]

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
def view_404(request):
    return rediect('/')

def bokapp_page(request):
    print("inside the function")
    script = server_document('http:://localhost:5006/bkapp')
    return render_to_response('bokeh_app/plot.html', {'script' : script } ) #, 'div' : div


def barrank_tab(request):



    def make_dataset(params_list):

        #by_params = pd.DataFrame(columns=[ ,'Max', 'Avarage', 'Min','color'])
        by_params = pd.DataFrame(columns=[ 'left','right', 'proportion', 'p_proportion','p_interval', 'name', 'w_name','color'])
            #

        # range_extent = range_end - range_start
        avg = []
        parms = []
        values = ["Standard", "input"]
        colors = ["#c9d9d3", "#718dbf"]
        # Iterate through all the parameters
        for i, para_name in enumerate(params_list):

            #print para_name
            # Subset to the parameter
            subset = webs[para_name].mean()
            avg.append(subset)

            params = usrweb[para_name]
            parms.append(params)

        data = {'params' : params_list,
            'Standard'   : avg,
            'input'   : parms,
        }
            # note: subset have to be a list of values

            # [webs.columns[i%6]]
            # Create a histogram with specified bins and range
            # arr_hist, edges = np.histogram(subset,
            #                              # bins = int(range_extent / bin_width),
            #                               range = [range_start, range_end])

            # Divide the counts by the total to get a proportion and create df
        #     arr_df= pd.DataFrame({'proportion': arr_hist ,
        #                           'left': edges[:-1], 'right': edges[1:]}) #/ np.sum(arr_hist)
        #
        #     # Format the proportion
        #     arr_df['p_proportion'] = ['%0.00005f' % proportion for proportion in arr_df['proportion']]
        #
        #     # Format the interval
        #     arr_df['p_interval'] = ['%d to %d scale' % (left, right) for left,
        #                            right in zip(arr_df['left'], arr_df['right'])]
        #
        #     # Assign the parameter for labels
        #     arr_df['name'] = para_name
        #     #arr_df['w_name'] = webs['Site name']
        #
        #
        #     # Color each parametr differently
        #     arr_df['color'] = Category20_16[i]
        #
        #     # Add to the overall dataframe
        #     by_params = by_params.append(arr_df)
        #
        # # Overall dataframe
        # by_params = by_params.sort_values(['name','left'])

        return ColumnDataSource(data=data)


    def style(p):
        # Title
        p.title.align = 'center'
        p.title.text_font_size ='20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 1
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"

        return p


    def make_plot(src):
        # Blank plot with correct labels
        # p = figure(plot_width = 700, plot_height = 700,
                  # title = "Histogram of Parameters for the Websites",
                  # x_axis_label = 'parameters', y_axis_label = "values")
        p = figure(x_range=initial_params, plot_height=450, toolbar_location=None,
                title="Average Performance of Website parameters")

        # Quad glyphs to create a histogram
        # p.quad(source=src, bottom =0,left = 'left', right = 'right', color ='color', top= 'proportion',fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
               # hover_fill_alpha = 1.0, line_color = 'color') #top='proportion',
        p.vbar(x=dodge('params',-0.15,range=p.x_range),
                        top = 'Standard', width=0.25, source=src, color = "#c9d9d3", legend=value("Standard"))
        p.vbar(x=dodge('params',0.15,range=p.x_range),
                        top = 'input', width=0.25, source=src, color = "#718dbf", legend=value("input cite"))
        # # Hover tool with vline mode
        # hover = HoverTool(tooltips=[('Parameter','@name'),
        #                            ('Website','@w_name'),
        #                             ('Proportion','@p_proportion')
        #                            ],
        #                  mode='vline')

        # p.add_tools(hover)
        # Stypling
        p = style(p)

        return p

    # Update function takes three default parameters
    def update(attr, old, new):

        # Get the list of parameter for the graph
        parameter_to_plot = [para_selection.labels[i] for i in para_selection.active]

        # Make a new dataset based on the selected parameter and the
        # make_dataset function defined earlier
        new_src = make_dataset(parameter_to_plot) #,
                      #       range_start = range_select.value[0],
                      # range_end = range_select.value[1],
                      # bin_width = binwidth_select.value)

        # Update the source used the quad glpyhs
        src.data.update(new_src.data)

    list_of_params = list(webs.columns[1:].unique())
    list_of_params.sort()

    para_selection = CheckboxGroup(labels=list_of_params, active = [0,1])
    para_selection.on_change('active',update)

    binwidth_select = Slider(start =0, end = 5,
                            step = 0.025, value = 0.05,
                            title = 'Change in parameter')
    binwidth_select.on_change('value', update)

    range_select = RangeSlider(start=0, end=1, value =(0,1),
                             step=0.00025, title = 'Change in range')
    range_select.on_change('value', update)

    initial_params = [para_selection.labels[i] for i in para_selection.active]


    src = make_dataset(initial_params)


    p = make_plot(src)
    #show(p)
    # Put controls in a single element
    controls = WidgetBox(para_selection, binwidth_select, range_select)

    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    # tab = Panel(child = layout, title = 'Bar ranking')
    # return tab
    script, div = components(layout, CDN)

    return render_to_response('bokeh_app/bar.html', {'script' : script , 'div' : div})

def density_tab(request):

    return render_to_response('bokeh_app/density.html', {'script' : script , 'div' : div})

def histogram_tab(request):

    return render_to_response('bokeh_app/histogram.html', {'script' : script , 'div' : div})
def table_tab(request):

    return render_to_response('bokeh_app/table.html', {'script' : script , 'div' : div})


def test_view(request):
    # bokeh_server_url = "%sbokehproxy/sliders" % (request.build_absolute_uri(location='/'))
    # print( "This is what is being printed out", bokeh_server_url)
    x= [1,3,5,7,9,11,13]
    y= [1,2,3,4,5,6,7]
    title = 'y = f(x)'
    # print("getting in the test view")
    plot = figure(title= title ,
        x_axis_label= 'X-Axis',
        y_axis_label= 'Y-Axis',
        plot_width =400,
        plot_height =400)

    # some data to be plot
    plot.line(x, y, legend= 'f(x)', line_width = 2)

    server = Server(
     # list of Bokeh applications
     bokeh_app,
     # Tornado IOLoop
     io_loop = loop,
     # port, num_procs, etc.
     **server_kwargs
    )
    server.start()

    #creat a session
    session  = push_session(curdoc())


    context = {'script': autoload_server(f, session_id=session.id)}
    # additonal argument to the autoload_server can be passed
    #                          app_path="/selection_histogram",
    # context = {'script': autoload_server(model=None)#, url="http://localhost:5006/")

    return render_to_response('plot.html', context=context)

    #Store components
    # script, div = components(plot)
    # html = file_html(plot, CDN, "MY PLOT")
    # print(html)

    # context = {'script': autoload_server}
    # return render(request, html)
    # return HttpResponse("yest it works")

    # return render_to_response('bokeh_app/plot.html', {'script' : script , 'div' : div})
    # return render_to_response(show(plot))
