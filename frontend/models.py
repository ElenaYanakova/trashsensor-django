from __future__ import unicode_literals

from django.db import models


class Sensor(models.Model):
    sensor_id = models.IntegerField(u'thingspeak id', primary_key=True)
    name = models.CharField(u'Name', max_length=128, blank=True)
    description = models.CharField(u'Description', max_length=256, blank=True)
    latitude = models.DecimalField(u'latitude', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(u'longitude', decimal_places=6, max_digits=9, blank=True, null=True)
    elevation = models.CharField(u'elevation', max_length=128, blank=True)
    last_entry_id = models.IntegerField(u'Last entry id', blank=True, null=True)
    ranking = models.IntegerField(u'Ranking', blank=True, null=True)

    @classmethod
    def create(cls, json):
        sensor = cls()
        sensor.sensor_id = json['id']
        sensor.name = json['name']
        sensor.description = json['description']
        sensor.latitude = json['latitude']
        sensor.longitude = json['longitude']
        sensor.elevation = json['elevation']
        sensor.last_entry_id = json['last_entry_id']
        sensor.ranking = json['ranking']
        return sensor
