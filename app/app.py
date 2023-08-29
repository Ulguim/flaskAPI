import matplotlib.pyplot as plt
import os
import requests
from flask import Flask
from flask import session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from Auth.twAuth import twit_auth
from Resource.games import games_blueprint
from db import cur
from flask_session import Session


app = Flask(__name__)
# Importing the routes
app.register_blueprint(games_blueprint)

db = SQLAlchemy()
app.logger.info(app.url_map)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@{os.environ.get("POSTGRES_HOST")}:5432/{os.environ.get("POSTGRES_DB")}'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    data = twit_auth()
