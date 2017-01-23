from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext

from services import *

# Create your views here.
from frontend.mqtt import mqttwork


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def home(request):
    sensors = Sensor.objects.all()
    return render(request, "home.html", {
        'sensors': sensors
    })


def sensor_page(request, pk):
    sensor = get_object_or_404(Sensor, pk=pk)
    if request.method == 'POST':
        volume = request.POST.get('volume')
        temperature = request.POST.get('temperature')
        channel_id = request.POST.get('channel_id')
        mqttwork.work(volume, temperature, channel_id)
    return render(request, "sensor.html", {
        'sensor': sensor
    })
