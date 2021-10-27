import os
from sys import platform
from passlib.context import CryptContext
from jose import jwt, JWTError
from . import db_sqlite as db


crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")


def get_hashed_password(password: str) -> str:
    return crypt_context.hash(password)


def is_auth_user_password(email, password) -> bool:
    try:
        return crypt_context.verify(password, db.get_user_from_email(email).password)
    except:
        return False


def is_valid_user(user: db.User) -> None:
    if is_auth_user_password(user.email, user.password):
        return True
    elif db.get_user_from_email(user.email).id == -1:
        db.set_user(user.copy(update={"password": get_hashed_password(user.password)}))
        return True
    else:
        return False


def get_jwt_token_from_email(email: str) -> str:
    return jwt.encode({"email": email}, APP_SECRET_KEY)


def get_email_from_jwt_token(token: str) -> str:
    try:
        return jwt.decode(token, APP_SECRET_KEY)["email"]
    except:
        return db.EMPTY_USER.email
