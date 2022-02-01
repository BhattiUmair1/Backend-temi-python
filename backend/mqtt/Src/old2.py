from glob import glob
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time
import ssl
import pytemi as temi


LOCATIE = None
GUID = None

HOST = "40.113.96.140"
PORT = 1883
TEMI_SERIAL = "00121175512"
ROBOT = ""
# CA_CRT = "C:/ca.crt"

MQTT_HOST = "40.113.96.140"
MQTT_PORT = 1883


def on_connect(client, userdata, flags, rc):
    global LOCATIE

    print("[STATUS] Connected to: {} (rc:{})".format(client._client_id, rc))
    client.subscribe("F2B/connection")
    client.subscribe("F2B/locatie")
    client.subscribe("F2B/return")
    # subscribe to Temi To Back (Jave Mqtt Client) & Front To Back (JavaScript Mqtt Client) topics
    # client.subscribe("Temi/...")


def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")
    client.loop_stop()


def on_message(client, userdata, msg):
    global LOCATIE
    global GUID
    print(msg.topic + " " + str(msg.payload))
    print(f"Raw message: {msg.payload}")
    print("------------------------------------------------------")

    topic = msg.topic

    data = msg.payload.decode("utf-8")
    dict = json.loads(data)

    if topic == "F2B/return":
        LOCATIE = dict["locatie"]
        GUID = dict["GUID"]
        waypoint = "G2" + LOCATIE
        client.publish(
            "B2F/return", payload=json.dumps({"locatie": LOCATIE, "GUID": GUID}))
        resp = go_to_waypoint(client, waypoint)
        if resp == 0:
            client.publish(
                "B2F/locatie", payload=json.dumps({"locatie": LOCATIE, "status": "arrived"}))

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
                resp = go_to_waypoint(client, "g2kleedkamer")
                if resp == 0:
                    client.publish(
                        "B2F/locatie", payload=json.dumps({"locatie": "kleedkamer", "status": "arrived"}))

            elif (LOCATIE == "onderweg naar sportscube"):
                resp = go_to_waypoint(client, "g2sportscube")
                if resp == 0:
                    client.publish(
                        "B2F/locatie", payload=json.dumps({"locatie": "sportscube", "status": "arrived"}))

            elif (LOCATIE == "onderweg naar onthaal"):
                resp = go_to_waypoint(client, "g2onthaal")
                if resp == 0:
                    client.publish(
                        "B2F/locatie", payload=json.dumps({"locatie": "onthaal", "status": "arrived"}))

            # for testing


def go_to_waypoint(client, waypoint):
    print("In goto")
    global ROBOT
    ROBOT.goto(waypoint)
    time.sleep(2)
    while ROBOT.goto_status != ROBOT.GOTO_COMPLETE:
        if ROBOT.goto_status == ROBOT.GOTO_ABORT:  # Temi could not arrive
            ROBOT.stop()
            client.publish(
                "B2F/admin", payload=json.dumps({"message": "Movement abborted", "locatie": waypoint}))
            sleep(1)
            return -1

    # Temi arrived
    return 0


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

    mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)
    ROBOT = temi.Robot(mqtt_client, TEMI_SERIAL)

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
