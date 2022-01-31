from glob import glob
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time
import ssl


LOCATIE = None
GUID = None

HOST = "40.113.96.140"
# HOST_TEMI = "test.mosquitto.org"
PORT = 1883
TEMI_SERIAL = "00121175512"
# CA_CRT = "C:/ca.crt"


def on_connect(client, userdata, flags, rc):
    global TEMI_SERIAL
    print("[STATUS] Connected to: {} (rc:{})".format(client._client_id, rc))
    client.subscribe("F2B/connection")
    client.subscribe("F2B/locatie")
    client.subscribe("F2B/return")
    # client.subscribe(f"temi/{TEMI_SERIAL}/#")
    # client.subscribe("temi/test/talk")


def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")
    client.loop_stop()


def on_message(client, userdata, msg):
    global LOCATIE
    global GUID
    global TEMI_SERIAL
    print(msg.topic + " " + str(msg.payload))
    print(f"Raw message: {msg.payload}")
    print("------------------------------------------------------")

    topic = msg.topic

    data = msg.payload.decode("utf-8")
    dict = json.loads(data)

    if topic == "F2B/return":
        LOCATIE = dict["locatie"]
        GUID = dict["GUID"]
        client.publish(
            "B2F/return", payload=json.dumps({"locatie": LOCATIE, "GUID": GUID}))
        # client.publish(
        #    f"temi/{TEMI_SERIAL}/command/waypoint/goto", payload=json.dumps({"location": LOCATIE}))

    # elif topic == f"temi/{TEMI_SERIAL}/event/waypoint/goto":
    #     status = dict["status"]
    #     print("status: " + status)

    # elif topic == "temi/test/talk":
    #     client.publish(
    #         f"temi/{TEMI_SERIAL}/command/tts", payload=json.dumps({"utterance": "Dit is van de python"}))

    else:
        if "connectionStatus" in dict.keys():
            LOCATIE = None
            client.publish(
                "B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
            client.publish("B2F/connected", payload=json.dumps(dict))

        # hoe controleer je of temi bezig?
        if "locatie" in dict.keys():
            LOCATIE = dict["locatie"]
            client.publish(
                "B2F/locatie", payload=json.dumps({"locatie": LOCATIE}))
            time.sleep(2)

            if (LOCATIE == "onderweg naar kleedkamer"):
                # client.publish(
                #     f"temi/{TEMI_SERIAL}/command/waypoint/goto", payload=json.dumps({"location": "kleedkamer"}))
                # LOCATIE = "kleedkamer"
                time.sleep(10)
                client.publish(
                    "B2F/arrived", payload=json.dumps({"locatie": "kleedkamer", "status": "arrived"}))

            elif (LOCATIE == "onderweg naar sportscube"):
                # client.publish(
                #     f"temi/{TEMI_SERIAL}/command/waypoint/goto", payload=json.dumps({"location": "sportscube"}))
                # LOCATIE = "sportscube"
                time.sleep(10)
                client.publish(
                    "B2F/arrived", payload=json.dumps({"locatie": "sportscube", "status":"arrived"}))
            elif (LOCATIE == "onderweg naar onthaal"):
                # client.publish(
                #     f"temi/{TEMI_SERIAL}/command/waypoint/goto", payload=json.dumps({"location": "onthaal"}))
                # LOCATIE = "onthaal"
                time.sleep(10)
                client.publish(
                    "B2F/arrived", payload=json.dumps({"locatie": "onthaal", "status":"arrived"}))


def connect(host, port, username=None, password=None):
    client = mqtt.Client()
    # client.tls_set(tls_version=2)
    # client.tls_set(ca_certs=CA_CRT, tls_version=ssl.PROTOCOL_TLSv1_2)
    # attach general callbacks

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

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
