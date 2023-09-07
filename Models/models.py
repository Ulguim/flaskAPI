

from enum import StrEnum
from db_config import database

# Login enum
class RoleEnum(StrEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class UserLogin(database.Model):
    __tablename__ = 'User'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True)
    password = database.Column(database.String())
    role = database.Column(database.String(), default=RoleEnum.USER.value)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = RoleEnum.USER

    def __repr__(self):
        return f'<UserLogin {self.username}>'

