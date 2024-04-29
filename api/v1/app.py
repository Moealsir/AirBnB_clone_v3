from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown app context"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
