# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from utils.hash import hash_data
from utils.hash import verify_hash


class UserModel(db.Model):
    """The model related to users.

    Attributes:
        id (Integer): user's id
        username (String): user's username
        password (LargeBinary): user's hashed password

    """
    __tablename__ = 'user'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _username = db.Column(db.String(32))
    _password = db.Column(db.LargeBinary(60))
    _full_name = db.Column(db.String(64))

    def __init__(self, username, password, full_name):
        # Clean the data
        username = str(username).strip()
        password = str(password).strip()
        full_name = str(full_name).strip()

        # Hash the password
        password_hash = hash_data(password)

        # Store the data in the object
        self._username = username
        self._password = password_hash
        self._full_name = full_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def get_full_name(self):
        return self._full_name

    def verify_password(self, password):
        return verify_hash(password, self._password)

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(_username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()
