"""trashsensor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from frontend.views import home, sensor_page, add_sensor, sync, sensor_delete

urlpatterns = [
    url(r'^sensor/add/$', add_sensor, name='add_sensor'),
    url(r'^sensor/sync/$', sync, name='sync'),
    url(r'^sensor/(?P<pk>\d+)/$', sensor_page, name='sensor_page'),
    url(r'^sensor/(?P<pk>\d+)/delete$', sensor_delete, name='sensor_delete'),
    url(r'^$', home, name='home'),
]
