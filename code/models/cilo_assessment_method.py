# -*- coding: utf-8 -*-
import models
from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage
from utils.converter import to_int
from models.saveable_model import SaveableModel


class CILOAssessmentMethod(SaveableModel):
    __tablename__ = 'cilo_assessment_method'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cilo_id = db.Column(db.Integer, db.ForeignKey('cilo.id'))
    assessment_method_id = db.Column(db.Integer, db.ForeignKey('assessment_method.id'))

    def __init__(self, course_id: int, assessment_method_id: int, cilo_index: int):
        cilo = models.cilo.CILO.find_cilo_by_course_id_and_cilo_index(course_id, cilo_index)
        assessment_method = models.assessment_method.AssessmentMethod.find_assessment_method_by_id(assessment_method_id)

        # Data validation
        # TO-DO: The validation error message is not complete
        if cilo is None:
            raise ErrorMessage(get_str('INVALID_REF'))
        if assessment_method is None:
            raise ErrorMessage(get_str('INVALID_REF'))

        # Store the data in the object
        self.cilo_id = cilo.id
        self.assessment_method_id = assessment_method.id

    @classmethod
    def find_relationship_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_relationships_by_cilo_id(cls, cilo_id: str) -> list:
        return cls.query.filter_by(cilo_id=to_int(cilo_id)).all()

    @classmethod
    def find_relationships_by_assessment_method_id(cls, method_id: str) -> list:
        return cls.query.filter_by(assessment_method_id=to_int(method_id)).all()
        
        