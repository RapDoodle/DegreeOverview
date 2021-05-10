# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage
from utils.validation import is_valid_length
from utils.converter import to_int
from models.saveable_model import SaveableModel


class CILO(SaveableModel):
    __tablename__ = 'cilo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    cilo_index = db.Column(db.Integer)
    cilo_description = db.Column(db.String(1024))
    display = db.Column(db.Boolean)

    def __init__(self, course_id, cilo_index, cilo_description):
        # Clean the data
        course_id = str(course_id).strip()
        cilo_index = str(cilo_index).strip()
        cilo_description = str(cilo_description).strip()

        # Data validation
        from models.course import Course
        if not Course.find_course_by_id(course_id):
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course id', key=course_id))
        cilo_index = to_int(cilo_index, 'CILO index')
        if not is_valid_length(cilo_description, 0, 1024):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='method name', min_len=0, max_len=1024))

        # Store the data in the object
        self.course_id = course_id
        self.cilo_index = cilo_index
        self.cilo_description = cilo_description
        self.display = True

    def edit_cilo(self, cilo):  
        # The description is the same, no need to change
        if cilo['cilo_description'] == self.cilo_description:
            return

        new_cilo = CILO(self.course_id, self.cilo_index, cilo['cilo_description'])
        new_cilo.save()

        self.display = False
        self.save()

    def get_cilo_performance(self) -> dict:
        pass

    def get_dependent_cilos(self) -> list:
        return CILO.query(CILO).join(CILO, CILO.id == models.cilo_dependency.CILODependency.cilo_id)\
            .filter(models.cilo_dependency.CILODependency.cilo_id==to_int(cilo_id)).all()

    def get_cilos_depended(self) -> list:
        return CILO.query(CILO).join(CILO, CILO.id == models.cilo_dependency.CILODependency.cilo_id)\
            .filter(models.cilo_dependency.CILODependency.depending_cilo_id==to_int(cilo_id)).all()

    @classmethod
    def find_cilo_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_cilo_by_keyword(cls, keyword: str) -> list:
        return cls.query.filter(cls.cilo_description.like('%' + keyword + '%')).all()

    @classmethod
    def find_cilos_by_course_id(cls, course_id) -> list:
        return cls.query.filter_by(course_id=course_id).all()
        
