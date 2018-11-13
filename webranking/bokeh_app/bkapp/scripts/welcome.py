# from bokeh.io import output_notebook

from bokeh.layouts import WidgetBox, row
from bokeh.models import CustomJS, TextInput, Paragraph , Panel
from bokeh.plotting import output_file, show

# connecting with the JavaScript file
from Naked.toolshed.shell import execute_js, muterun_js

# CALLBACKS
def welcome_tab():
    welcome_message = 'Please put your web address: (none)'

    text_banner = Paragraph(text=welcome_message, width=200, height=100)

    def callback_print(text_banner=text_banner):
        user_input = str(cb_obj.value)
        welcome_message = 'Collecting paramaters for: ' + user_input
        text_banner.text = welcome_message
        print("caaling")
        # passing the website to the webtest_analysis.js
        response = muterun_js('webtest_analysis.js', user_input)
        print("SUCCEED")
        # if response.exitcode == 0:
        #     print("SUCCEED")
        #     msg.text = "SUCCEDED \n" + response.stdout
        # else:
        #     msg.text = sys.stderr.write(response.stderr)
        # print(msg)
    # USER INTERACTIONS
    text_input = TextInput(value="", title="Enter your web address: ",
                          callback=CustomJS.from_py_func(callback_print))

    # LAYOUT
    widg = WidgetBox(text_input, text_banner)

    # find a way to center the widgets
    layout = row(widg) #, sizing_mode = 'scale_width')
    tab = Panel(child = layout, title = "Welcome")
    # show(widg)
    return tab
