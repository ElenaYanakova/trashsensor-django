from django.forms import ModelForm

from frontend.models import Sensor


class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = ['name', 'description', 'elevation', 'latitude', 'longitude']
