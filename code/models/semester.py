# -*- coding: utf-8 -*-
from core.db import db
from utils.converter import to_int


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

    @classmethod
    def find_semester_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id)).first()
        
    @classmethod
    def find_semesters_by_year(cls, year: int):
        return cls.query.filter_by(year=to_int(year)).all()