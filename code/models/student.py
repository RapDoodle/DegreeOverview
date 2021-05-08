# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User


class Student(User):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    student_id = db.Column(db.String(32))

    def __init__(self, username, password, full_name, student_id):
        super().__init__(username, password, full_name)

        # Clean the data
        student_id = str(student_id).strip()

        # Store the data in the object
        self.student_id = student_id

    def get_student_id(self):
        return self.student_id