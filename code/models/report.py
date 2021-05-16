# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from utils.converter import to_int


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, course_id, semester_id):
        self.course_id = course_id
        self.semester_id = semester_id

    @classmethod
    def find_report_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()