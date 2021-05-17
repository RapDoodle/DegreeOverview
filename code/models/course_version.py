# -*- coding: utf-8 -*-
import models
from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from utils.converter import to_int


class CourseVersion(models.saveable_model.SaveableModel):
    __tablename__ = 'course_version'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    version = db.Column(db.Integer)
    effective_since = db.Column(db.Integer)

    def __init__(self, course_id, effective_since):
        # Clean the data
        effective_since = str(effective_since).strip()

        # Data validation
        effective_since = to_int(effective_since, name='year')
        
        old_course_version = CourseVersion.find_course_latest_version(course_id=course_id)
        if old_course_version is None:
            self.version = 0
        else:
            # Logic validation:
            # The current (to become the previous) version must have an 
            # effective year ealier 
            if old_course_version.effective_since >= effective_since:
                raise ErrorMessage(get_str('INVALID_EFFECTIVE_SINCE', year=old_course_version.effective_since))
            self.version = old_course_version.version + 1

        self.course_id = course_id
        self.effective_since = effective_since

    @classmethod
    def find_course_versions(cls, course_id: int):
        return cls.query.filter_by(course_id=course_id).all().order_by(cls.version.desc())

    @classmethod
    def find_course_latest_version(cls, course_id: int):
        return cls.query.filter_by(course_id=course_id).order_by(cls.version.desc()).first()

    @classmethod
    def find_course_version_by_year(cls, course_id: int, year: int):
        pass

    @classmethod
    def find_course_version_by_id(cls, id: int):
        return cls.query.filter_by(id=to_int(id, 'course type id')).first()
