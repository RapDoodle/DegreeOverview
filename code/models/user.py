# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from utils.hash import hash_data
from utils.hash import verify_hash

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER


class User(db.Model):
    """The model related to users.

    Attributes:
        id (Integer): user's id
        username (String): user's username
        password (LargeBinary): user's hashed password

    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32))
    _password = db.Column(db.LargeBinary(60))
    full_name = db.Column(db.String(64))

    def __init__(self, username, password, full_name):
        # Clean the data
        username = str(username).strip()
        password = str(password).strip()
        full_name = str(full_name).strip()

        # Hash the password
        password_hash = hash_data(password)

        # Store the data in the object
        self.username = username
        self._password = password_hash
        self.full_name = full_name

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.full_name

    def verify_password(self, password):
        return verify_hash(password, self._password)

    def get_user_type(self):
        if User.is_course_designer(self.id):
            return COURSE_DESIGNER
        elif User.is_lecturer(self.id):
            return LECTURER
        elif User.is_student(self.id):
            return STUDENT
        else:
            return -1

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def is_student(cls, id):
        return models.student.Student.query.filter_by(id=id).first() is not None

    @classmethod
    def is_lecturer(cls, id):
        return models.lecturer.Lecturer.query.filter_by(id=id).first() is not None
    
    @classmethod
    def is_course_designer(cls, id):
        return models.course_designer.CourseDesigner.query.filter_by(id=id).first() is not None