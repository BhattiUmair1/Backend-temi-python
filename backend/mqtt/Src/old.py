# import pytemi as temi
import logging
import time
from flask_socketio import SocketIO, send, emit
# from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date

# parameters
# MQTT_HOST = "test.mosquitto.org"
# MQTT_PORT = 1883
# TEMI_SERIAL = "01234567890"

# connect to the MQTT broker
# mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)

# create robot object
# robot = temi.Robot(mqtt_client, TEMI_SERIAL)

# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!aBcdXyZ'


socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=1,
                    logger=True, engineio_logger=True, ssl_verify=False)
CORS(app)


# # SOCKET.IO EVENTS

@socketio.on("connect")
def initial_connection():
    print("New user detected")
    socketio.emit("B2F_locatie_changed", {"locatie": None})


@socketio.on_error()
def error_handler(e):
    print(e)


@socketio.on("F2B_locatie_changed")
def locatie_changed(msg):
    print(f"received: {msg}")
    value = msg["locatie"]
    socketio.emit("B2F_locatie_changed", {"locatie": value})
    # code om robot naar een locatie te laten gaan komt dan ook hier

# @socketio.on('F2B_go_to')
# def goto(waypoint):
#     robot.goto(waypoint)  # command the robot to go to a saved location
#     time.sleep(3)  # wait some time for action to complete
#     emit('B2F_arrived', {'Status': 'arrived'})


# START THE APP
if __name__ == '__main__':
    context = ('cert.crt', 'key.key')
    socketio.run(app, debug=False, host='0.0.0.0', ssl_context=context)
