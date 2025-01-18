import os
from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    
    # config mongodb
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/multilingual_form_db")
    mongo = PyMongo(app)
    
    return app, mongo