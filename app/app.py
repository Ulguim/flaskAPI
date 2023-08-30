import matplotlib.pyplot as plt
import os
import requests
from flask import Flask
from flask import session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from Auth.twAuth import twit_auth
from Resource.games import games_blueprint
from db import cur
from flask_session import Session
from flask_migrate import Migrate


from Models.models import db,UserLogin

app = Flask(__name__)
# Importing the routes
app.register_blueprint(games_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://flask:flask@{os.environ.get("POSTGRES_HOST")}:5432/{os.environ.get("POSTGRES_DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Configuring the database
# db = SQLAlchemy(app)


app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    data = twit_auth()
