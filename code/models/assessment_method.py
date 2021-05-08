# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from models.user import User

from utils.validation import is_valid_length


class AssessmentMethod(db.Model):
    __tablename__ = 'assessment_method'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    method_name = db.Column(db.String(128))
    weight = db.Column(db.Integer)

    def __init__(self, course_id, method_name, weight):
        # Clean the data
        course_id = str(course_id).strip()
        method_name = str(method_name).strip()
        weight = str(weight).strip()

        # Data validation
        from models.course import Course
        if Course.find_course_by_id():
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course id', key=course_id))        
        if not is_valid_length(method_name, 1, 128):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='method name', min_len=1, max_len=128))
        weight = to_int(weight, 'weight')
        if weight <= 0 or weight > 100:
            raise ErrorMessage(get_str('INVALID_WEIGHT'))

        # Store the data in the object
        self.course_id = course_id
        self.method_name = method_name
        self.weight = weight

    def edit_method(self, method):
        new_method = AssessmentMethod(self.course_id, self.method_name, method['weight'])
        new_method.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)