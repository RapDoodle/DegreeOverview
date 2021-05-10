# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from utils.validation import is_valid_length
from utils.converter import to_int
from models.saveable_model import SaveableModel


class CILOAssessmentMethod(SaveableModel):
    __tablename__ = 'cilo_assessment_method'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cilo_id = db.Column(db.Integer, db.ForeignKey('cilo.id'))
    assessment_method_id = db.Column(db.Integer, db.ForeignKey('assessment_method.id'))

    def __init__(self, course_id, cilo_id: int, assessment_method_id: int):
        cilo = models.cilo.CILO.find_cilo_by_id(cilo_id)
        assessment_method = models.assessment_method.AssessmentMethod.find_assessment_method_by_id(assessment_method_id)

        # Data validation
        if cilo is None:
            raise ErrorMessage(get_str('INVALID_REF', field_name='CILO', key=str(cilo_id)))
        if assessment_method is None:
            raise ErrorMessage(get_str('INVALID_REF', field_name='denpending assessment method', key=str(depending_cilo_id)))

        # Store the data in the object
        self.cilo_id = cilo.id
        self.assessment_method_id = assessment_method.id

    def delete_dependency(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_relationship_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_relationships_by_cilo_id(cls, cilo_id: str) -> list:
        return cls.query.filter_by(cilo_id=to_int(cilo_id)).all()

    @classmethod
    def find_relationships_by_assessment_method_id(cls, method_id: str) -> list:
        return cls.query.filter_by(assessment_method_id=to_int(method_id)).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        