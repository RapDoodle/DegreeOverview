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
    course_version_id = db.Column(db.Integer, db.ForeignKey('course_version.id'))

    def __init__(self, course_id, cilo_index, cilo_description, course_version_id):
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
        self.course_version_id = course_version_id

    def edit_cilo(self, cilo, revision):
        new_cilo = CILO(self.course_id, self.cilo_index, cilo['cilo_description'], revision)
        new_cilo.save()

        self.save()

    def get_cilo_performance(self) -> dict:
        pass

    def get_dependee_cilos(self) -> list:
        """Get the CILOs that this CILOs dependes on."""
        return models.cilo_dependency.CILODependency.find_dependencies_by_cilo_id(self.id)

    def get_dependeding_cilos(self) -> list:
        """Get the CILOs that depend on this CILO."""
        return models.cilo_dependency.CILODependency.find_dependencies_by_denpending_cilo_id(self.id)

    @classmethod
    def find_cilo_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_cilo_by_keyword(cls, keyword: str) -> list:
        return cls.query.filter(cls.cilo_description.like('%' + keyword + '%')).all()

    @classmethod
    def find_cilos_by_course_id(cls, course_id, course_version_id) -> list:
        return cls.query.filter_by(course_id=course_id, course_version_id=course_version_id).all()

    @classmethod
    def find_cilo_by_course_id_and_cilo_index(cls, course_id, cilo_index) -> list:
        return cls.query.filter_by(course_id=course_id, cilo_index=cilo_index).first()

