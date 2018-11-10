# Pandas for data management
import pandas as pd
# os methods for manipulating paths
# import os
import os.path
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.welcome import welcome_tab
from scripts.barranking import barrank_tab
from scripts.histogram import histogram_tab
from scripts.density import density_tab
#from scripts.table import table_tab
#from scripts.draw_map import map_tab
#from scripts.routes import route_tab
#
# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# print(os.path('__file__'))
# path = '/c/Users/ktadesse/Desktop/Project/Webpageranking/bokeh_app/data'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, 'data')

# Read data into dataframes
webs = pd.read_csv(os.path.join(RESOURCE_DIR, 'nor_time.csv'),
                                index_col=0).dropna()
# webs = pd.read_csv(join(dirname('__file__'), path, 'nor_time.csv'),
	                                          # index_col=0).dropna()

#webs = webs_paras.drop(['(Doc complete) Byets in','(Fully loaded) Bytes in',
#						'(Fully loaded) Requests', '(Fully loaded) Requests',
#						'(Doc complete) Requests'], axis = 1)
#webs_requests = webs_paras[['Site name','(Fully loaded) Requests',
#							'(Fully loaded) Requests','(Doc complete) Requests']]
## Formatted Flight Delay Data for map
##map_data = pd.read_csv(join(dirname('__file__'), path, 'flights_map.csv'),
                           # header=[0,1], index_col=0)

#? need to import the paramaters for the one website
usrweb = webs.iloc[2]


# Create each of the tabs
tab1 = welcome_tab()
tab2 = barrank_tab(webs, usrweb)
tab3 = histogram_tab(webs)
tab4 = density_tab(webs)

#tab5 = table_tab(flights)

#tab6 = map_tab(map_data, states)
#tab7 = route_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4]) # tab4, tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
