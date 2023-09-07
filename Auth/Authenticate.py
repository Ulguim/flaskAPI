
from flask import Blueprint

from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from  Models.models import UserLogin
from  db_config import database
# Authentication with JWT
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

auth_blueprint = Blueprint('auth', __name__)
# @auth is a decorator that tells Flask what URL to trigger the function
@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        userData = UserLogin.query.filter_by(username=username).first()
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
            return jsonify({'error': 'User already exists'})

        user = UserLogin(username, password)
        database.session.add(user)
        database.session.commit()
        body = {
            "username": username,
            "password": password
        }
        return(body)

    except Exception as e:
        return jsonify({'error': str(e)})

