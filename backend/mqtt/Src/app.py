from glob import glob
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time
import ssl
from Src import pytemi as temi

LOCATIE = None

HOST = "40.113.96.140"
PORT = 1883
TEMI_SERIAL = "00121175512"
ROBOT = ""
# CA_CRT = "C:/ca.crt"

def on_connect(client, userdata, flags, rc):
    global LOCATIE

    print("[STATUS] Connected to: {} (rc:{})".format(client._client_id, rc))
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
    print("------------------------------------------------------")

    data = msg.payload.decode("utf-8")
    dict = json.loads(data)

    if "connectionStatus" in dict.keys():
        LOCATIE = None
        client.publish("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
        ROBOT.webview("https://temi-tablet.azurewebsites.net/")

    if "locatie" in dict.keys():
        LOCATIE = dict["locatie"]
        client.publish("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
        # for testing

    if "status" in dict.keys():
        if(LOCATIE == "onderweg naar kleedkamer" and dict["status"] == "gearriveerd"):
            LOCATIE = "kleedkamer"
            client.publish("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
        elif(LOCATIE == "onderweg naar sportscube" and dict["status"] == "gearriveerd"):
            LOCATIE = "sportscube"
            client.publish("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
        elif(LOCATIE == "onderweg naar onthaal" and dict["status"] == "gearriveerd"):
            LOCATIE = "onthaal"
            client.publish("B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
        else:
            print(f"ERROR PARSING 'ARRIVED', CURRENT LOCATION: {LOCATIE}")


    # actually doing something with the message...

def connect(host, port, username=None, password=None):
    global ROBOT

    # create a new MQTT client instance
    client = mqtt.Client()
    # client.tls_set(tls_version=2)
    # client.tls_set(ca_certs=CA_CRT, tls_version=ssl.PROTOCOL_TLSv1_2)
    # attach general callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    ROBOT = temi.Robot(client, TEMI_SERIAL)

    # connect to MQTT broker
    client.connect(host=host, port=port, keepalive=60)

    # start listening to topics
    client.loop_forever()

    # wait for client to connect
    # TODO check using on_connect()
    # time.sleep(1)

    # return client

if __name__ == '__main__':
    connect(HOST, PORT)