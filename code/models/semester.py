# -*- coding: utf-8 -*-
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessagePromise

from models.user import User


class Semester(db.Model):
    __tablename__ = 'semester'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)

    def __init__(self, year: int, term: int):
        if term not in [1, 2]:
            raise Exception('Invalid term')

        self.year = year
        self.term = term

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @classmethod
    def get_semester(cls, year, term):
        semester = cls.query.filter(Semester.year==year, Semester.term==term).first()
        if semester is None:
            semester = Semester(year, term)
            semester.save()
        return semester