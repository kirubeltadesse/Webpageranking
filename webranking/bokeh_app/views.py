from django.shortcuts import render
from bokeh_app.forms import UserForm
from bokeh_app.forms import WebForm
#just to see the models
from bokeh_app.models import UserInfo

# view types
from django.utils import timezone
from django.views.generic import ListView, DetailView


# Create your views here.
import logging
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# library for bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components, file_html, server_session
from bokeh.server.server import Server

#
from bokeh.io import curdoc
from bokeh.client import push_session
# import the function

# def usrweb_view(request):
#     form = forms.UserWeb()         #request.POST  # just enables "This field is required."
#
#     # Check to see if we get a POST back.
#     if request.method == 'POST':
#         form = forms.UserWeb(request.POST)
#
#         web_name = form.data['usrweb']
#         print("reaching here")
#         print(data)
#
#
#             # call the funcition here and pass the parameters
#
#     # Pass request, name of the html file to hold the form and pass a dictionary {key:value}
#     return render(request, 'bokeh_app/forms.html',{'form':form})


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
    # return HttpResponse("Hello THere")

# def front_view(request):
#     return render(request, 'front_end/front.html')
# this request will be coming from contiue button on forms
# def process_view(request):
#     UserInfo.objects.all()
#     # form = forms.UserWeb()        #request.POST  # just enables "This field is required."
    #
    # # Check to see if we get a POST back.
    # if request.method == 'POST':
    #     form = forms.UserWeb(data=request.POST)
    #     form.save()
    # #
    #
    #     web_name = form.data
    #     print("reaching here")
    #     print(web_name)
# class showWebRequestView(ListView):
#     model = UserInfo
#     def get_queryset(self):
#         return UserInfo.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')

# class showWebRequestDetail(DetailView):
#     model = UserInfo


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

    # server = Server(
    #  # list of Bokeh applications
    #  bokeh_applications,
    #  # Tornado IOLoop
    #  io_loop = loop,
    #  # port, num_procs, etc.
    #  **server_kwargs
    # )
    # server.start()

    #creat a session
    # session  = push_session(curdoc())


    # context = {'script': autoload_server(f, session_id=session.id)}
    # additonal argument to the autoload_server can be passed
    #                          app_path="/selection_histogram",
    # context = {'script': autoload_server(model=None)#, url="http://localhost:5006/")

    # return render_to_response('plot.html', context=context)

    #Store components
    script, div = components(plot)
    # html = file_html(plot, CDN, "MY PLOT")
    # print(html)

    # context = {'script': autoload_server}
    # return render(request, html)
    # return HttpResponse("yest it works")

    return render_to_response('bokeh_app/plot.html', {'script' : script , 'div' : div})
    # return render_to_response(show(plot))
