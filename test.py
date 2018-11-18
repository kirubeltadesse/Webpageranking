import pandas as pd
import numpy as np

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, layout
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button


def scatterplot(source):
    tools = ['pan', 'box_select', 'wheel_zoom', 'reset']
    scatter = figure(title='scatterplot', tools=tools,
                     active_drag='box_select')
    scatter.circle(source=source, x='x', y='y')
    return scatter


def save_selected(dataframe, selection):
    data = dataframe.iloc[selection]
    def save():
        print(f'I got your df right here! {data.shape}')
        pass # ??? Provide csv to user
    return save


def clear_click_callbacks(button):
    button._callbacks['clicks'].clear()


def generate_makedoc_function(dataframe):
    def makedoc(doc):
        source = ColumnDataSource(dataframe)
        scatter = scatterplot(source)
        savebutton = Button(label='download selected points')
        savebutton.on_click(save_selected(dataframe, selection=[]))

        def update_selection(attr, old, new):
            clear_click_callbacks(savebutton)  # on_click appends, want replace
            savebutton.on_click(save_selected(dataframe,
                                              selection=new.indices))

        source.on_change('selected', update_selection)
        page_content = layout([[scatter], [savebutton]])
        doc.title = 'save selected points!'
        doc.add_root(page_content)
    return makedoc


def main(path='/', port=5000):
    df = pd.DataFrame({'x': np.random.random(100),
                       'y': np.random.random(100),
                       'useful': np.random.randint(0, 100, size=100)})
    apps = {path: Application(FunctionHandler(generate_makedoc_function(df)))}
    server = Server(apps, port=port, allow_websocket_origin=['8000'])
    server.run_until_shutdown()


if __name__ == '__main__':
    main()
