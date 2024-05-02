#!/usr/bin/python3
"""flask api-web-application"""
from flask import Flask, jsonify, make_response
from os import getenv
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


hbnb_host = getenv('HBNB_API_HOST')
hbmb_port = getenv('HBNB_API_PORT')
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


def set_port_host(HBNB_API_HOST, HBNB_API_PORT):
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = '5000'


@app.teardown_appcontext
def shutdown(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found(exception=None):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    set_port_host(hbnb_host, hbmb_port)
    app.run(host=hbnb_host, port=hbmb_port, threaded=True, debug=True)
