#!/usr/bin/python3
"""flask api-web-application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def shutdown(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found(exception=None):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
