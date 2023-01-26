# -*- coding: utf-8 -*-
from core.db import db
from models.user import User


class Lecturer(User):
    __tablename__ = 'lecturer'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    staff_id = db.Column(db.String(32))

    def __init__(self, username, password, full_name, staff_id):
        super().__init__(username, password, full_name)

        # Clean the data
        staff_id = str(staff_id).strip()

        # Store the data in the object
        self.staff_id = staff_id

    def get_staff_id(self):
        return self.staff_id