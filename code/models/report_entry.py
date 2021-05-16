# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from utils.converter import to_int


class ReportEntry(db.Model):
    """A student's grade entry"""
    __tablename__ = 'report_entry'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, report_id, semester_id):
        self.semester_id = report_id
        self.semester_id = semester_id

    @classmethod
    def find_report_entry_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()