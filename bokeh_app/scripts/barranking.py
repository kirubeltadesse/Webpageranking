# %load scripts/histogram.py
import pandas as pd
import numpy as np

from bokeh.io import show, push_notebook
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.transform import dodge

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs


from bokeh.layouts import column, row, WidgetBox

def barrank_tab(webs, usrweb):

    def make_dataset(params_list):

        avg = []
        parms = []
        values = ["Standard", "input"]
        colors = ["#c9d9d3", "#718dbf"]
        # Iterate through all the parameters
        for i, para_name in enumerate(params_list):


            subset = webs[para_name].mean()
            avg.append(subset)

            params = usrweb[para_name]
            parms.append(params)

        data = {'params' : params_list,
            'Standard'   : avg,
            'input'   : parms,
        }
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

    def update(attr, old, new):
        # Get the list of carriers for the graph
        para_to_plot = [para_selection.labels[i] for i in
                            para_selection.active]

        # Make a new dataset based on the selected carriers and the
        # make_dataset function defined earlier
        new_src = make_dataset(para_to_plot)

        # Update the source used the quad glpyhs
        src.data.update(new_src.data)


    def make_plot(src):

        p = figure(x_range=list_of_params, plot_height=450, toolbar_location="right",
                title="Comparison of the Performance of Websites",
                x_axis_label = 'Parameters', y_axis_label = 'Percentage')

        p.vbar(x=dodge('params',-0.15,range=p.x_range),
                        top = 'Standard', width=0.65, source=src, color = "#41b6c4", alpha=0.8,muted_color="#41b6c4", muted_alpha=0.2, legend=value("Standard"))
        p.vbar(x=dodge('params',0.15,range=p.x_range),
                        top = 'input', width=0.6, source=src, color = "#084594", alpha=0.8,muted_color="#084594", muted_alpha=0.2,legend=value("input site"))
        p.legend.click_policy="mute"

        hover = HoverTool(tooltips=[('Percentage','@src'),
                            #('Distribution', '@src'),
                                #('Density', '@ys'),
                                    ],
                                    line_policy = 'next')

        p.add_tools(hover)

        p = style(p)

        return p

    list_of_params = list(webs.columns[1:].unique())
    list_of_params.sort()

    src = make_dataset(list_of_params)
    para_selection = CheckboxGroup(labels=list_of_params, active = [0, 1])
    para_selection.on_change('active', update)

#     binwidth_select = Slider(start = 0, end = 1,
#                          step = 0.00025, value = 0.0005,
#                          title = 'Delay Width (min)')
#     binwidth_select.on_change('value', update)

#     range_select = RangeSlider(start = 0, end = 1, value = (0,1),
#                                step = 0.00025, title = 'Delay Range (min)')
#     range_select.on_change('value', update)



    initial_params = [para_selection.labels[i] for i in para_selection.active]

    src = make_dataset(initial_params)
    p = make_plot(src)

     # Put controls in a single element
    controls = WidgetBox(para_selection)

    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child = layout, title = 'Bar ranking')
    return tab
