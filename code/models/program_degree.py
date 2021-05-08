# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User

from utils.converter import to_int


class ProgramDegree(db.Model):
    __tablename__ = 'program_degree'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column(db.String(128))

    def __init__(self, degree):
        self.degree = degree

    @classmethod
    def get_all_degrees(cls):
        return cls.query.all()

    @classmethod
    def find_program_degree_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id, 'program degree id')).first()