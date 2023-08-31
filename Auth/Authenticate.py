
from flask import Blueprint

from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from  Models.models import UserLogin

database = SQLAlchemy()

auth_blueprint = Blueprint('auth', __name__)

# @auth is a decorator that tells Flask what URL to trigger the function
@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        userData = "UserLogin.query.filter_by(username=username).first()"
        if userData is None:
            return jsonify({'error': 'User not found'})

        return jsonify(userData)
    except Exception as e:
        return jsonify({'error': str(e)})

@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    try:
        username = request.json['username']
        password = request.json['password']
        # role = request.json['role']
        userData = UserLogin.query.filter_by(username=username).first()
        if userData is not None:
            return jsonify(userData)

        user = UserLogin(username, password, role)
        database.session.add(user)
        database.session.commit()
        return jsonify(user)

    except Exception as e:
        return jsonify({'error': str(e)})

