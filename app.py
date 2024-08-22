from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from backend import openmeteoapi

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/data', methods=['GET'])
def getData():
    lat = request.args.get('lat', default=1, type=float)
    long = request.args.get('long', default=1, type=float)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)
    return jsonify(openmeteoapi.getData(lat, long, start_date, end_date))


if __name__ == '__main__':
    app.run()
