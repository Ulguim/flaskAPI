from flask import Flask
import os
from flask import session
from flask_migrate import Migrate
from Auth.twAuth import twit_auth
# from Auth.Authenticate import auth_blueprint
from Resource.games import games_blueprint
from db_config import cur
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.register_blueprint(games_blueprint)
    from Auth.Authenticate import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://flask:flask@{os.environ.get("POSTGRES_HOST")}:5432/{os.environ.get("POSTGRES_DB")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from Models.models import database as db
    db.init_app(app)
    migrate = Migrate(app, db)
    # Configuring the database
    # db = SQLAlchemy(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Session(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
    data = twit_auth()
