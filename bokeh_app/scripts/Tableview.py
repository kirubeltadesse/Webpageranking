# %load scripts/histogram.py
import pandas as pd
import numpy as np

from bokeh.io import show, push_notebook
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.transform import dodge

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

from bokeh.layouts import column, row, WidgetBox

def table_tab(webs):

    def make_dataset(params_list):

        avg = []
        parms = []
        values = ["Standard", "input"]
        colors = ["#c9d9d3", "#718dbf"]
        # Iterate through all the parameters
        for i, para_name in enumerate(params_list):


            subset = webs[para_name].mean()
            avg.append(subset)



        data = {'params' : params_list,
            'Standard'   : avg,
        }
        return ColumnDataSource(data=data)


    def make_plot(src):
        columns = [
        TableColumn(field="params", title="Performance Parameter"),
        TableColumn(field="Standard", title="Average Performance") ]
        data_table = DataTable(source=src, columns=columns, width=500, height=380)

        return data_table

    list_of_params = list(webs.columns[1:].unique())
    list_of_params.sort()

    src = make_dataset(list_of_params)

    p = make_plot(src)

     # Put controls in a single element
    controls = WidgetBox(p)

    # Create a row layout
    layout = row(controls)

    # Make a tab with the layout
    tab = Panel(child = layout, title = 'Table View')
    return tab
