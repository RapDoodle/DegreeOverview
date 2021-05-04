# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User


class Staff(User):
    __tablename__ = 'staff'

    _id = db.Column(db.Integer, db.ForeignKey('user._id'), primary_key=True)
    _staff_id = db.Column(db.String(32))

    def __init__(self, username, password, full_name, staff_id):
        super().__init__(username, password, full_name)

        # Clean the data
        staff_id = str(staff_id).strip()

        # Store the data in the object
        self._staff_id = staff_id

    def get_staff_id(self):
        return self._staff_id