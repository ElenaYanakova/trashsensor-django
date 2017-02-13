# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from frontend.forms import SensorForm
from thingspeak.services import *

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


def sensor_delete(request, pk):
    if request.user.is_superuser:
        sensor = get_object_or_404(Sensor, pk=pk)
        response = delete_channel(pk)
        if response['result'] == 'error':
            return render(request, "sync.html", {
                'error': response['error'],
            })
        else:
            sensor.delete()
            return redirect('home')
    return render(request, "sync.html", {
        'my_error': u'Удалять сенсоры могут только администраторы'
    })


def sensor_page(request, pk):
    sensor = get_object_or_404(Sensor, pk=pk)
    data_sent = False
    if request.method == 'POST':
        volume = request.POST.get('volume')
        temperature = request.POST.get('temperature')
        mqttwork.work(sensor, volume, temperature)
        data_sent = True
    return render(request, "sensor.html", {
        'sensor': sensor,
        'data_sent': data_sent,
    })


def sec_to_hours(sec):
    return sec / (60.0 * 60.0)


def sync(request):
    result = list_my_channels()
    if result['result'] == 'error':
        return render(request, "sync.html", {
            'error': result['error'],
        })
    my_channels = result['body']
    Sensor.objects.all().delete()
    for channel in my_channels:
        sensor = Sensor.create(channel)
        sensor.save()
    return redirect('home')


def add_sensor(request):
    last_sensor = Sensor.objects.all().order_by('-datetime_create')
    wait_time = 0
    if len(last_sensor) > 0:
        last_sensor = last_sensor[0]
        delta = datetime.datetime.now().replace(tzinfo=None) - last_sensor.datetime_create.replace(tzinfo=None)
        wait_time = 12 - sec_to_hours(delta.total_seconds())
    can_create = wait_time <= 0 or request.user.is_superuser

    result = None
    result_ok = False
    form = None
    error = None
    if can_create:
        if request.method == 'POST':
            form = SensorForm(request.POST)
            if form.is_valid():
                r = create_channel(form.cleaned_data)
                if r['result'] == 'error':
                    error = r['error']
                else:
                    sensor = Sensor.create(r['body'])
                    sensor.save()
                    return redirect('sensor_page', sensor.pk)
        else:
            form = SensorForm()
    return render(request, "add_sensor.html", {
        'form': form,
        'result': result,
        'result_ok': result_ok,
        'can_create': can_create,
        'wait_time': "%.2f" % wait_time,
        'error': error
    })
