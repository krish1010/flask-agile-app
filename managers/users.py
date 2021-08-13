from database.models.tables.users import User
from database.models.enums.user_types import UserType
from uuid import uuid4


def create_user(name, password, user_type):
    User.create(idx=str(uuid4()), username=name, password=password, user_type=UserType(user_type))


def get_user(username, password):
    user = User.get_by_username(username)
    if user.check_password(password):
        return user
