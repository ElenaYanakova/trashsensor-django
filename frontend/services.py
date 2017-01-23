import requests

from frontend.models import Sensor

BASE_URL = 'https://api.thingspeak.com/%s'
API_KEY = 'D6OIEIT5E9EZ3WJU'


def make_request(url, method='get', params={}, key_required=False):
    full_url = BASE_URL % url
    method = method.lower()
    if key_required:
        params['api_key'] = API_KEY
    r = requests.request(method, full_url, params=params)
    return r


def create_channel(name=None, description=None, elevation=None, latitude=None, longitude=None):
    method = 'POST'
    url = 'channels'
    params = {
        'name': name,
        'description': description,
        'elevation': elevation,
        'latitude': latitude,
        'longitude': longitude,
    }
    r = make_request(url, method, params, key_required=True)


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
