# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage
from utils.validation import is_valid_length
from utils.converter import to_int
from models.saveable_model import SaveableModel


class AssessmentMethod(SaveableModel):
    __tablename__ = 'assessment_method'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    method_name = db.Column(db.String(128))
    weight = db.Column(db.Integer)
    revision = db.Column(db.Integer)

    def __init__(self, course_id, method_name, weight, cilos_addressed, since, revision):
        # Clean the data
        course_id = str(course_id).strip()
        method_name = str(method_name).strip()
        weight = str(weight).strip()

        # Data validation
        from models.course import Course
        if not Course.find_course_by_id(course_id):
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course id', key=course_id))        
        if not is_valid_length(method_name, 1, 128):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='method name', min_len=1, max_len=128))
        weight = to_int(weight, 'weight')
        if weight <= 0 or weight > 100:
            raise ErrorMessage(get_str('INVALID_WEIGHT'))

        assert len(since) == 2
        since_semester = models.semester.Semester.get_semester(since[0], since[1])

        # Store the data in the object
        self.course_id = course_id
        self.method_name = method_name
        self.weight = weight
        self.revision = revision

    def edit_method(self, method):
        new_method = AssessmentMethod(self.course_id, method['name'], method['weight'])
        new_method.save()

    @classmethod
    def find_assessment_method_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_assessment_method_by_keyword(cls, keyword: str) -> list:
        return cls.query.filter(cls.cilo_description.like('%' + keyword + '%')).all()

    @classmethod
    def find_assessment_methods_by_course_id(cls, course_id) -> list:
        return cls.query.filter_by(course_id=course_id).all()
