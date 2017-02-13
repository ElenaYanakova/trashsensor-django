import requests

from frontend.models import Sensor

BASE_URL = 'https://api.thingspeak.com/%s'
API_KEY = '3BLVIV5M1A3COYBF'


def make_request(url, method='get', params={}, key_required=False):
    full_url = BASE_URL % url
    method = method.lower()
    if key_required:
        params['api_key'] = API_KEY
    return requests.request(method, full_url, params=params)


def create_channel(clean):
    method = 'POST'
    url = 'channels.json'
    params = {
        'name': clean['name'],
        'description': clean['description'],
        'elevation': clean['elevation'],
        'latitude': clean['latitude'],
        'longitude': clean['longitude'],
        'field1': 'Volume',
        'field2': 'Temperature',
        'field3': 'Firmware',
        'public_flag': 'true',
    }
    return make_request(url, method, params, key_required=True)


def view_channel(id):
    method = 'GET'
    url = 'channels/%s.json' % id
    r = make_request(url, method)
    channel_info = r.json()
    sensors = Sensor.objects.filter(sensor_id=id)
    if len(sensors) == 0:
        sensor = Sensor.create(channel_info)
        sensor.save()
    else:
        sensor = sensors[0]
    return sensor


def list_my_channels():
    method = 'GET'
    url = 'channels.json'
    return make_request(url, method, key_required=True).json()


def delete_channel(id):
    method = 'DELETE'
    url = 'channels/%s.json' % id
    return make_request(url, method, key_required=True).json()
