# -*- coding: utf-8 -*-
from core.db import db
from models.lecturer import Lecturer


class CourseDesigner(Lecturer):
    __tablename__ = 'course_designer'

    id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), primary_key=True)

    def __init__(self, username, password, full_name, lecturer_id):
        super().__init__(username, password, full_name, lecturer_id)
