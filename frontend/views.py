from django.shortcuts import render


# Create your views here.
from frontend.mqtt import mqttwork


def home(request):
    if request.method == 'POST':
        volume = request.POST.get('volume')
        temperature = request.POST.get('temperature')
        channel_id = request.POST.get('channel_id')
        mqttwork.work(volume, temperature, channel_id)
    return render(request, "home.html")
