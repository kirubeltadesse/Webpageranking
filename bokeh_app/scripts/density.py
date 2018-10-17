import pandas as pd
import numpy as np

from scipy.stats import gaussian_kde

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker,LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def density_tab(webs):

	def make_dataset(param_list, range_start, range_end, bandwidth):

		xs = []
		ys = []
		colors = []
		labels = []

		for i, param in enumerate(param_list):
			subset = webs[param].between(range_start,range_end)
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
	available_parameters = list(set(webs.columns[1:]))
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

	tab = Panel(child=layout, title = 'Density Plot')
	return tab #tabs = Tabs(tabs=[tab])
	

		


