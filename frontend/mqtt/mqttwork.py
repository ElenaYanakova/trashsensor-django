import paho.mqtt.client as paho

BROKER_ADDRESS = "mqtt.thingspeak.com"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def work(sensor, volume, temp):
    client = paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_start()

    topic = "channels/%s/publish/%s" % (sensor.sensor_id, sensor.write_key)
    payload = "field1=%s&field2=%s" % (volume, temp)
    (rc, mid) = client.publish(topic, str(payload), qos=0)
