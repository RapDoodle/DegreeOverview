# -*- coding: utf-8 -*-
from core.db import db
from utils.converter import to_int


class Degree(db.Model):
    __tablename__ = 'degree'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    related_program_id = db.Column(db.Integer, db.ForeignKey('program.id'))

    def __init__(self, name, related_program_id):
        self.name = name
        self.related_program_id = related_program_id

    @classmethod
    def get_all_degrees(cls):
        return cls.query.all()

    @classmethod
    def find_degree_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id, 'degree')).first()