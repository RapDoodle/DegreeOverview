# -*- coding: utf-8 -*-
import models
from sqlalchemy import func
from sqlalchemy import select
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
        if not models.course.Course.find_course_by_id(course_id):
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course id', key_name=course_id))
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

    def json(self, find_related=False):
        json_obj = {
            'id': self.id,
            'course_id': self.course_id,
            'cilo_index': self.cilo_index,
            'cilo_description': self.cilo_description,
            'course_version_id': self.course_version_id
        }
        if find_related:
            json_obj['pre_cilos'] = [
                CILO.find_cilo_by_id(cilo_dependency.depending_cilo_id).json(find_related=False)
                for cilo_dependency in self.get_dependee_cilos()
            ]
            json_obj['post_cilos'] = [
                CILO.find_cilo_by_id(cilo_dependency.cilo_id).json(find_related=False)
                for cilo_dependency in self.get_dependeding_cilos()
            ]
        return json_obj

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
        latest_versions = [cilo.course_version_id for cilo in cls.query.filter(cls.course_version_id)\
                    .group_by(cls.course_id)\
                    .having(cls.course_version_id==db.func.max(cls.course_version_id))\
                    .all()]
        return cls.query.filter(cls.cilo_description.like('%' + keyword + '%'))\
            .filter(cls.course_version_id.in_(latest_versions))\
            .order_by(cls.course_id)\
            .all()

    @classmethod
    def find_cilos_by_course_id(cls, course_id, course_version_id) -> list:
        return cls.query.filter_by(course_id=course_id, course_version_id=course_version_id).all()

    @classmethod
    def find_cilo_by_course_id_and_cilo_index(cls, course_id, cilo_index) -> list:
        return cls.query.filter_by(course_id=course_id, cilo_index=cilo_index).first()

