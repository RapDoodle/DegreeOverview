# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User


class Lecturer(User):
    __tablename__ = 'lecturer'

    _id = db.Column(db.Integer, db.ForeignKey('user._id'), primary_key=True)
    _staff_id = db.Column(db.String(32))

    def __init__(self, username, password, full_name, lecturer_id):
        super().__init__(username, password, full_name)

        # Clean the data
        lecturer_id = str(lecturer_id).strip()

        # Store the data in the object
        self._lecturer_id = lecturer_id

    def get_staff_id(self):
        return self._staff_id