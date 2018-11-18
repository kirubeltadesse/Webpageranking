"""webranking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bokeh_app import views


from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# endpoints for data consumed by the bokeh apps
# router.register(r'histogram',)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('slider/', views.histogram_tab, name='histogram'),
    # path('bokeh_app/histogram/(?P<bokeh_app>\w+)/$', views.embed_bokeh, name='embed-bokeh'),
    path('bokeh_app/', include('bokeh_app.urls')),
]
