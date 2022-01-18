import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time

LOCATIE = None


def on_connect(client, userdata, flags, rc):
    global LOCATIE

    print(f"Connected with result code {rc}")
    client.subscribe("F2B/connection")
    client.subscribe("F2B/locatie")


    # subscribe to Temi To Back (Jave Mqtt Client) & Front To Back (JavaScript Mqtt Client) topics
    # client.subscribe("Temi/...")


def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")
    client.loop_stop()

def on_message(client, userdata, msg):
    global LOCATIE

    print(msg.topic + " " + str(msg.payload))
    print(f"Raw message: {msg.payload}")

    data = msg.payload.decode("utf-8")
    dict = json.loads(data)
    print(f"Incoming dictionary: {dict}")

    if "connectionStatus" in dict.keys():
        LOCATIE = None
        publish.single("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}), hostname="13.81.105.139", qos=0)

    if "locatie" in dict.keys():
        LOCATIE = dict["locatie"]
        publish.single("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}), hostname="13.81.105.139", qos=0)
        # for testing


    # actually doing something with the message...

def connect(host, port, username=None, password=None):
    # create a new MQTT client instance
    client = mqtt.Client()

    # attach general callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # set username and password
    if username and password:
        client.username_pw_set(username=username, password=password)

    # connect to MQTT broker
    client.connect(host=host, port=port, keepalive=60, bind_address="")

    # start listening to topics
    client.loop_forever()

    # wait for client to connect
    # TODO check using on_connect()
    # time.sleep(1)

    # return client

if __name__ == '__main__':
    connect("13.81.105.139", 1883)