
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats.kde import gaussian_kde
import pandas as pd
from bokeh.io import output_file, show, output_notebook
from bokeh.models import ColumnDataSource, FixedTicker, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.sampledata.perceptions import probly
# import colorcet as cc
from bokeh.models import (CategoricalColorMapper, HoverTool,ColumnDataSource, Panel,FuncTickFormatter, SingleIntervalTicker,LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

output_notebook()


# In[3]:


def bar_tab(webs, usrweb):
    
    def make_dataset(param_list):
        avg = []
        parms = []
       
        for i, param in enumerate(param_list):
            subset = webs[param]
            avg.append(subset.mean())
            params = usrweb[param]
            parms.append(params)
            
           
            data = {'params' : param_list,
            'Standard'   : avg,
            'input'   : parms
                   }
           
            
            return ColumnDataSource(data=data)
        
        def make_plot(src):
            p = figure(x_range='params', plot_height=450, toolbar_location=None,title="Average Performance of Website parameters")
            p.vbar(x=dodge('params',-0.15,range=p.x_range),
                        top = 'Standard', width=0.25, source=src, color = '#718dbf', legend=value("Standard"))
            p.vbar(x=dodge('params',0.15,range=p.x_range),
                        top = 'input', width=0.25, source=src, color = '#c9d9d3', legend=value("input cite"))
            p = style(p)
            show(p)
            return p
        
    
        def style(p):
            # Title
            p.title.align = 'center'
            p.title.text_font_size = '20pt'
            p.title.text_font = 'serif'
            # Axis titles
            p.xaxis.axis_label_text_font_size = '14pt'
            p.xaxis.axis_label_text_font_style = 'bold'
            p.yaxis.axis_label_text_font_size = '14pt'
            p.yaxis.axis_label_text_font_style = 'bold'
            # Tick labels
            p.xaxis.major_label_text_font_size = '12pt'
            p.yaxis.major_label_text_font_size = '12pt'
            return p
        
    available_parameters= list(set(webs.columns[1:]))
    available_parameters.sort()
    
    # Make the Bar plot data source
    src = make_dataset(available_parameters)
    p = make_plot(src)
    
    #controls = WidgetBox(param_selection, range_select,bandwidth_select, bandwidth_choose)
    layout = row(p)
    tab = Panel(child=layout, title = 'Bar Plot')
    return tab #tabs = Tabs(tabs=[tab])





















# In[6]:




