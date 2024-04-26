#!/usr/bin/python3
"""flask api-web-application"""
from flask import Flask, jsonify, make_response, request
from models import storage
from os import getenv
from api.v1.views import app_views


hbnb_host = getenv('HBNB_API_HOST')
hbnb_port = getenv('HBNB_API_PORT')
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
def error_404(exception=None):
    """error_404 view function"""
    return jsonify({"error":"Not found"}), 404


if __name__ == "__main__":
    set_port_host(hbnb_host, hbnb_port)
    app.run(host=hbnb_host, port=hbnb_port, threaded=True)
