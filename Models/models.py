
from flask_sqlalchemy import SQLAlchemy
# from enum import StrEnum
from db_config import database
class UserLogin(database.Model):
    __tablename__ = 'User'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True)
    password = database.Column(database.String())
    # role = database.Column(database.StrEnum(RoleEnum))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.role = RoleEnum.USER

    def __repr__(self):
        return f'<UserLogin {self.username}>'

# class RoleEnum(StrEnum):
#     ADMIN = 'ADMIN'
#     USER = 'USER'
#
#     def __init__(self):
#         pass
#
#     def __repr__(self):
#         return f'<RoleEnum {self.value}>'