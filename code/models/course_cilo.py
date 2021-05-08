# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from models.user import User

from utils.validation import is_valid_length
from utils.converter import to_int


class CourseCILO(db.Model):
    __tablename__ = 'course_cilo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    cilo_index = db.Column(db.Integer)
    cilo_description = db.Column(db.String(1024))

    def __init__(self, course_id, cilo_index, cilo_description):
        # Clean the data
        course_id = str(course_id).strip()
        cilo_index = str(cilo_index).strip()
        cilo_description = str(cilo_description).strip()

        # Data validation
        from models.course import Course
        if Course.find_course_by_id():
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course id', key=course_id))
        cilo_index = to_int(cilo_index, 'CILO index')
        if not is_valid_length(cilo_description, 0, 1024):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='method name', min_len=0, max_len=1024))

        # Store the data in the object
        self.course_id = course_id
        self.method_name = method_name
        self.weight = weight

    def edit_cilo(self, method):
        new_method = AssessmentMethod(self.course_id, self.method_name, method['weight'])
        new_method.save()

    def get_cilo_performance(self) -> dict:
        pass

    def get_dependent_cilos(self) -> list:
        pass

    def get_cilos_depended(self) -> list:
        pass

    @classmethod
    def find_cilo_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_cilo_by_keyword(cls, keyword: str) -> list:
        return cls.query.filter(CourseCILO.cilo_description.like('%' + keyword + '%')).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)