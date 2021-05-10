# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from utils.validation import is_valid_length
from utils.converter import to_int
from models.saveable_model import SaveableModel


class CILODependency(SaveableModel):
    __tablename__ = 'cilo_dependency'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cilo_id = db.Column(db.Integer, db.ForeignKey('cilo.id'))
    depending_cilo_id = db.Column(db.Integer, db.ForeignKey('cilo.id'))

    def __init__(self, course_id, cilo_id: int, depending_cilo_id: int):
        cilo = models.cilo.CILO.find_cilo_by_id(cilo_id)
        depending_cilo = models.cilo.CILO.find_cilo_by_id(depending_cilo_id)

        # Data validation
        if cilo is None:
            raise ErrorMessage(get_str('INVALID_REF', field_name='CILO id', key_name=str(cilo_id)))
        if depending_cilo is None:
            raise ErrorMessage(get_str('INVALID_REF', field_name='denpending CILO id', key_name=str(depending_cilo_id)))

        # Store the data in the object
        self.cilo_id = cilo.id
        self.depending_cilo_id = depending_cilo.id

    @classmethod
    def find_dependency_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()

    @classmethod
    def find_dependencies_by_cilo_id(cls, cilo_id: str) -> list:
        return cls.query.filter_by(cilo_id=to_int(cilo_id)).all()

    @classmethod
    def find_dependencies_by_denpending_cilo_id(cls, cilo_id: str) -> list:
        return cls.query.filter_by(depending_cilo_id=to_int(cilo_id)).all()
        
        