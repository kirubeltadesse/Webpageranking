from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import pandas as pd
import numpy as np

from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

# for bar plot
from bokeh.transform import dodge
from bokeh.core.properties import value

# for density plot
from scipy.stats import gaussian_kde
from . import process_input


Instant = process_input.helper(2)
#, index_col=0).dropna()

#getting the csv file
file = pd.read_csv(Instant.get_data(file='alexasite.csv')).dropna()

# picking up the six Column
time = Instant.catagory(file,'time')

# normalizing the 6 Columns
webs_nor = Instant.normal(time, name='running_normalization')


webs= pd.DataFrame(data=webs_nor)

# print(webs.index.values)
usrInputDf = Instant.get_data()
# print(webs)
# changing the input to pandas serias
usrweb = usrInputDf.iloc[0]


# print(type(usrweb),"this is the type")

def histogram_tab(doc):

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

			arr_df['w_name'] = webs.index.values[i]

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
		p.quad(source=src, bottom =0,left = 'left', right = 'right', color ='color', top= 'proportion',fill_alpha = 0.7, hover_fill_color = 'navy', legend = 'name',
			   hover_fill_alpha = 1.0, line_color = 'color') #top='proportion',

		# Hover tool with vline mode
		hover = HoverTool(tooltips=[('Parameter','@name'),
								   ('Website','@w_name'),
									('Proportion','@p_proportion')
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
		#new_src = ColumnDataSource(new_src)

		# Update the source used the quad glpyhs
		src.data.update(new_src.data)

	list_of_params = list(webs.columns.get_level_values(0).drop_duplicates())[1:]
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
	doc.title = "Histogram"
	doc.add_root(layout)

def barrank_tab(doc):

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

		return ColumnDataSource(data=dict(data))


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
				x_axis_label = 'parameters', y_axis_label = 'Percentage')

		p.vbar(x=dodge('params',-0.15,range=p.x_range),
						top = 'Standard', width=0.65, source=src, color = "#41b6c4", muted_color="#41b6c4",
						muted_alpha=0.2, fill_alpha = 0.7, hover_fill_color = 'navy',  hover_fill_alpha = 1.0, legend=value("Standard"))
		p.vbar(x=dodge('params',0.15,range=p.x_range),
						top = 'input', width=0.5, source=src, color = "#084594", muted_color="#084594",
						muted_alpha=0.2,fill_alpha = 0.7, hover_fill_color = 'navy',  hover_fill_alpha = 1.0, legend=value("input site"))
		hover = HoverTool(tooltips=[('Parameter','@name'),
								   # ('Website','@w_name'),
									# ('Proportion','@p_proportion')
								   ],
						 mode='vline')
		p.legend.click_policy="mute"

		hover = HoverTool(tooltips=[('Percentage','@y_axis_label'),
							#('Distribution', '@src'),
								#('Density', '@ys'),
									],
									line_policy = 'next')

		p.add_tools(hover)

		p = style(p)

		return p

	list_of_params = list(webs.columns.get_level_values(0).drop_duplicates()) #.unique())
	# list_of_params.sort()

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

	layout = row(controls, p)
	doc.add_root(layout)
	doc.title = "Bar ranking"

def density_tab(doc):

	def make_dataset(param_list, range_start, range_end, bandwidth):

		xs = []
		ys = []
		colors = []
		labels = []

		for i, param in enumerate(param_list):
			print(webs[param])

			subset = webs[param].between(range_start,range_end)

			# subset= webs[(webs[param] >= range_start) and (webs[para] <= range_end)]

			# subset = webs[param].between(range_start,range_end)

			#subset = subset[subset[param].between(range_start,range_end)]

			kde = gaussian_kde(webs[param], bw_method=bandwidth)

			# Evenly space x values
			x = np.linspace(range_start, range_end, 100)

			y = kde.pdf(x)

			# Append the values to plot
			xs.append(list(x))
			ys.append(list(y))

			# Append the colors and label
			colors.append(para_colors[i])
			labels.append(param)

		new_src = ColumnDataSource(data={'x':xs, 'y':ys,
										'color':colors, 'label':labels})
		return new_src

	def make_plot(src):
		p = figure(plot_width = 700, plot_height = 700,
					title = 'Density Plot Parameters',
					x_axis_label = 'Distribution', y_axis_label = 'Density')
		p.multi_line('x', 'y', color = 'color', legend = 'label',
					line_width = 3, source = src)
		hover = HoverTool(tooltips=[('parameter','@label'),
									#('Distribution', '@src'),
									#('Density', '@ys'),
									],
						  line_policy = 'next')

		p.add_tools(hover)

		p = style(p)
		return p

	def update(attr, old, new):

		parameters_to_plot = [param_selection.labels[i] for i in
							  param_selection.active]
		if bandwidth_choose.active == []:
			bandwidth = None
		else:
			bandwidth = bandwidth_select.value

		new_src = make_dataset(parameters_to_plot,
									range_start = range_select.value[0],
									range_end = range_select.value[1],
									bandwidth = bandwidth)
		src.data.update(new_src.data)

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

	# Parameter and colors
	available_parameters = list(webs.columns.get_level_values(0).drop_duplicates())
	available_parameters.sort()

	para_colors = Category20_16
	para_colors.sort()

	param_selection = CheckboxGroup(labels = available_parameters,
									active = [0,1])
	param_selection.on_change('active', update)

	range_select = RangeSlider(start = 0, end = 1, value = (0,1),
							   step = 0.0025, title = 'Range of Parameter')
	range_select.on_change('value', update)

	initial_parameter = [param_selection.labels[i] for
						i in param_selection.active]
	# Bandwidth of kernel
	bandwidth_select = Slider(start = 0.1, end = 5,
							  step = 0.1, value = 0.5,
							  title = 'Bandwidth for Density Plot')
	bandwidth_select.on_change('value', update)

	bandwidth_choose = CheckboxButtonGroup(
						labels = ['Choose Bandwidth (Else Auto)'], active = [])
	bandwidth_choose.on_change('active', update)

	# Make the density data source
	src = make_dataset(initial_parameter,
						range_start = range_select.value[0],
						range_end = range_select.value[1],
						bandwidth = bandwidth_select.value)

	p = make_plot(src)

	p = style(p)

	controls = WidgetBox(param_selection, range_select,
						bandwidth_select, bandwidth_choose)

	layout = row(controls, p)
	doc.title = "Density"
	doc.add_root(layout)


def table_tab(doc):

	def make_dataset(params_list):

		avg = []
		parms = []
		values = ["Standard", "input"]
		colors = ["#c9d9d3", "#718dbf"]
		# Iterate through all the parameters
		for i, para_name in enumerate(params_list):


			subset = usrInputDf[para_name] #.mean()
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

	list_of_params = list(usrInputDf.columns.unique())
	list_of_params.sort()

	src = make_dataset(list_of_params)

	p = make_plot(src)

	 # Put controls in a single element
	controls = WidgetBox(p)

	# Create a row layout
	layout = row(controls)
	doc.title = "Table view"
	doc.add_root(layout)
