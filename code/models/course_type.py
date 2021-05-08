# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User

from utils.converter import to_int


class CourseType(db.Model):
    __tablename__ = 'course_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(32))

    def __init__(self, type):
        self.type = type

    @classmethod
    def get_all_types(cls):
        return cls.query.all()

    @classmethod
    def find_course_type_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id, 'course type id')).first()