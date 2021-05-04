# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User
from models.staff import Staff


class CourseDesigner(Staff):
    __tablename__ = 'course_designer'

    _id = db.Column(db.Integer, db.ForeignKey('staff._id'), primary_key=True)

    def __init__(self, username, password, full_name, staff_id):
        super().__init__(username, password, full_name, staff_id)
