import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs


from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

#from bokeh.application.handlers import FunctionHandler
#from bokeh.application import Application

#output_notebook()

def histogram_tab(webs):

    def make_dataset(params_list, range_start = 0.0, range_end = 1, bin_width = 0.005):
        
        #check to make sure the start is less than the end
        assert range_start < range_end, "Start must be less than end!"

        #by_params = pd.DataFrame(columns=[ ,'Max', 'Avarage', 'Min','color'])
        by_params = pd.DataFrame(columns=[ 'left','right', 'proportion', 'p_proportion','p_interval', 'name', 'w_name','color']) 
            # 

        range_extent = range_end - range_start
        values = ['Min', "Avarage", 'Max']
        # Iterate through all the parameters 
        for i, para_name in enumerate(params_list):

            #print para_name
            # Subset to the parameter
            subset = webs[para_name]

            # note: subset have to be a list of values

            # [webs.columns[i%6]]

            # Create a histogram with specified bins and range
            arr_hist, edges = np.histogram(subset,  
                                          bins = int(range_extent / bin_width),
                                          range = [range_start, range_end])

            # Divide the counts by the total to get a proportion and create df
            arr_df= pd.DataFrame({'proportion': arr_hist ,
                                  'left': edges[:-1], 'right': edges[1:]}) #/ np.sum(arr_hist)

            # Format the proportion
            arr_df['p_proportion'] = ['%0.00005f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['p_interval'] = ['%d to %d scale' % (left, right) for left, 
                                   right in zip(arr_df['left'], arr_df['right'])]

            # Assign the parameter for labels
            arr_df['name'] = para_name
            #arr_df['w_name'] = webs['Site name']

            # Color each parametr differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            by_params = by_params.append(arr_df)

        # Overall dataframe
        by_params = by_params.sort_values(['name','left'])
    
        return ColumnDataSource(by_params)


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

        return p


    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700,
                  title = "Histogram of Parameters for the Websites",
                  x_axis_label = 'parameters', y_axis_label = "values")

        # Quad glyphs to create a histogram
        p.quad(source=src, bottom =0,left = 'left', right = 'right', color ='color', top= 'proportion',fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'color') #top='proportion',

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Parameter','@name'),
                                   ('Website','@w_name'),
                                    ('Proportion','p_proportion')
                                   ],
                         mode='vline')

        p.add_tools(hover)
        # Stypling
        p = style(p)
        return p
     
    # Update function takes three default parameters
    def update(attr, old, new):

        # Get the list of parameter for the graph
        parameter_to_plot = [para_selection.labels[i] for i in para_selection.active]

        # Make a new dataset based on the selected parameter and the 
        # make_dataset function defined earlier
        new_src = make_dataset(parameter_to_plot,
								range_start = range_select.value[0],
                      range_end = range_select.value[1],
                      bin_width = binwidth_select.value)

        # Convert dataframe to column data source
        new_src = ColumnDataSource(new_src)

        # Update the source used the quad glpyhs
        src.data.update(new_src.data)

    list_of_params = list(webs.columns[1:].unique())
    list_of_params.sort()
    
    para_selection = CheckboxGroup(labels=list_of_params, active = [0,1])
    para_selection.on_change('active',update)
    
    binwidth_select = Slider(start =0, end = 1,
                            step = 0.00025, value = 0.0005,
                            title = 'Change in parameter')
    binwidth_select.on_change('value', update)
    
    range_select = RangeSlider(start=0, end=1, value =(0,1),
                             step=0.00025, title = 'Change in range')
    range_select.on_change('value', update)
    
    initial_params = [para_selection.labels[i] for i in para_selection.active]
    
    src = make_dataset(initial_params,
                      range_start = range_select.value[0],
                      range_end = range_select.value[1],
                      bin_width = binwidth_select.value)
    
    
    p = make_plot(src)
    #show(p)
    # Put controls in a single element
    controls = WidgetBox(para_selection, binwidth_select, range_select)
    
    # Create a row layout
    layout = row(controls, p)
    
    # Make a tab with the layout
    tab = Panel(child = layout, title = 'Histogram')
    return tab
    #tabs = Tabs(tabs=[tab])
    
    #doc.add_root(tabs)
    
# Set up an application
#handler = FunctionHandler(modify_doc)
#app = Application(handler)


#modify_doc(webs)
#show(app, 'localhost:9000')



