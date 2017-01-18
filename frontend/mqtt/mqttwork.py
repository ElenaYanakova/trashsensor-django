import paho.mqtt.client as paho

BROKER_ADDRESS = "mqtt.thingspeak.com"
API_KEY = "D6OIEIT5E9EZ3WJU"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def work(volume, temp, channel_id):
    client = paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_start()

    topic = "channels/%s/publish/%s" % (channel_id, API_KEY)
    payload = "field1=%s&field2=%s" % (volume, temp)
    (rc, mid) = client.publish(topic, str(payload), qos=0)
