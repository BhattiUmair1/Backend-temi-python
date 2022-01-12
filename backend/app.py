from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.publish as publish

# Start app
app = Flask(__name__)
CORS(app)


# Custom endpoint
endpoint = '/api/v1'

# ROUTES


@app.route(endpoint + '/afspraken', methods=['GET', 'POST'])
def get_entries():
    if request.method == 'GET':
        data = DataRepository.read_all_entries()
        if data is not None:
            publish.single("paho/test/sam/D4", data, hostname="13.81.105.139")
            return jsonify(data), 200
        else:
            return jsonify(message='error'), 404

    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        print(request)
        data = DataRepository.add_entry("test")
        return jsonify(data), 201


@app.route(endpoint + '/afspraken/<uid_afsrpaak>', methods=['GET', 'PUT', 'DELETE'])
def get_entries_UID(uid_afsrpaak):
    if request.method == 'GET':
        data = DataRepository.read_entry_on_uid(uid_afsrpaak)
        if data is not None:
            publish.single("paho/test/sam/D4", data, hostname="13.81.105.139")
            return jsonify(data), 200
        else:
            return jsonify(message='error'), 404

    elif request.method == 'PUT':  # update
        gegevens = DataRepository.json_or_formdata(request)
        data = DataRepository.update_entry(uid_afsrpaak)
        if data is not None:
            if data > 0:
                return jsonify(uid_afsrpaak), 200
            else:
                return jsonify(status=data), 200
        else:
            return jsonify(message='error'), 404

    elif request.method == 'DELETE':
        data = DataRepository.delete_entry(uid_afsrpaak)
        print(data)
        return jsonify(status=data), 200


# Start app
if __name__ == '__main__':
    app.run(debug=True)
