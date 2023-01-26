# -*- coding: utf-8 -*-
from core.db import db
from utils.converter import to_int


class Program(db.Model):
    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_all_programs(cls):
        return cls.query.all()

    @classmethod
    def find_program_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id, 'program')).first()