#!/usr/bin/python3
"""flask api-web-application"""
from flask import Flask, jsonify, make_response, request
from models import storage
from os import getenv
from api.v1.views import app_views


hbnb_host = getenv('HBNB_API_HOST')
hbmb_port = getenv('HBNB_API_PORT')
app = Flask(__name__)
app.register_blueprint(app_views)


def set_port_host(HBNB_API_HOST, HBNB_API_PORT):
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = '5000'

@app.teardown_appcontext
def shutdown(self):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    if request.path != '/api/v1/status':
        return make_response(jsonify({"error": "Not found"}), 404)
    return make_response(jsonify({"status": "OK"}), 200)


if __name__ == "__main__":
    set_port_host(hbnb_host, hbmb_port)
    app.run(host=hbnb_host, port=hbmb_port, threaded=True)
