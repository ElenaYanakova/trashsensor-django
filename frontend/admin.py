from django.contrib import admin

# Register your models here.
from solo.admin import SingletonModelAdmin

from frontend.models import Sensor, Config

admin.site.register(Sensor)
admin.site.register(Config, SingletonModelAdmin)
