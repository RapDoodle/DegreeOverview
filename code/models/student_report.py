# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from utils.converter import to_int


class StudentReport(db.Model):
    """A student's grade entry"""
    __tablename__ = 'student_report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, report_id, student_id):
        self.report_id = report_id
        self.student_id = student_id

    @classmethod
    def find_report_entry_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()