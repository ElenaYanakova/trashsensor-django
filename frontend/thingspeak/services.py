import requests

from frontend.models import Sensor, Config
from frontend.thingspeak.error_handler import get_error

BASE_URL = 'https://api.thingspeak.com/%s'


def make_request(url, method='get', params={}, key_required=False):
    full_url = BASE_URL % url
    method = method.lower()
    if key_required:
        params['api_key'] = Config.get_solo().api_key  # 3BLVIV5M1A3COYBF
    response = requests.request(method, full_url, params=params).json()
    error = get_error(response)
    result = {}
    if error:
        result['result'] = 'error'
        result['error'] = error
    else:
        result['result'] = 'ok'
        result['body'] = response
    return result


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
    channel_info = make_request(url, method)
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
    return make_request(url, method, key_required=True)


def delete_channel(id):
    method = 'DELETE'
    url = 'channels/%s.json' % id
    return make_request(url, method, key_required=True)
