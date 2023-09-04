from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DECISION_ENGINE_URL
from config import DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    # the error for debug
    app.logger.error(str(error))
    return jsonify({"error": "Internal server error"}), 500

from app import routes
from flask_migrate import Migrate

migrate = Migrate(app, db)
