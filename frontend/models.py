# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from solo.models import SingletonModel


class Config(SingletonModel):
    api_key = models.CharField(u'API key', max_length=128,
                               help_text=u'Api KEY на thingspeak.com (по умолчанию: 3BLVIV5M1A3COYBF)')


class Sensor(models.Model):
    sensor_id = models.IntegerField(u'id на thingspeak', primary_key=True)
    name = models.CharField(u'Имя', max_length=128, blank=True)
    description = models.CharField(u'Описание', max_length=256, blank=True)
    latitude = models.DecimalField(u'Широта', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(u'Долгота', decimal_places=6, max_digits=9, blank=True, null=True)
    elevation = models.CharField(u'Высота', max_length=128, blank=True)
    last_entry_id = models.IntegerField(u'id последнего отчета', blank=True, null=True)
    ranking = models.IntegerField(u'Ранк', blank=True, null=True)

    datetime_create = models.DateTimeField(u'Время добавления', auto_now_add=True, editable=False)
    write_key = models.CharField(u'Ключ записи', max_length=256, null=True)

    def __unicode__(self):
        return u"[%d] %s" % (self.sensor_id, self.name)

    class Meta:
        verbose_name = u"Сенсор"
        verbose_name_plural = u"Сенсоры"

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
        sensor.datetime_create = datetime.datetime.now()
        for api_key in json['api_keys']:
            if api_key['write_flag']:
                sensor.write_key = api_key['api_key']
                break
        return sensor
