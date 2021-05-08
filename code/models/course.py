# -*- coding: utf-8 -*-
import models

from flask_language import current_language

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

from utils.validation import is_valid_length


class Course(db.Model):
    """The model related to users.

    Attributes:
        id (Integer): user's id
        username (String): user's username
        password (LargeBinary): user's hashed password

    """
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(128))
    course_code = db.Column(db.String(16))
    course_type_id = db.Column(db.Integer, db.ForeignKey('course_type.id'))
    since_semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    ends_semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=True)
    program_degree_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, course_name, course_code, course_type_id, program_degree_id, since, ends=None):
        """since and ends should be a list or tuple. The first element is the year 
        and the second element indicates the term
        """        
        # Clean the data
        course_name = str(course_name).strip()
        course_code = str(course_code).strip()

        # Data validation
        if not is_valid_length(course_name, 1, 128):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='course name', min_len=1, max_len=128))
        if not is_valid_length(course_code, 1, 16):
            raise ErrorMessage(get_str('INVALID_LENGTH', field_name='course code', min_len=1, max_len=16))
        
        # Foreign key validation
        course_type = models.course_type.CourseType.find_course_type_by_id(course_type_id)
        if course_type is None:
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course type id', key=course_type_id))
        assert len(since) == 2
        since_semester = models.semester.Semester.get_semester(since[0], since[1])
        if ends is not None:
            assert len(ends) == 2
            ends_semester = models.semester.Semester.get_semester(ends[0], ends[1])  
        program_degree = models.program_degree.ProgramDegree.find_program_degree_by_id(program_degree_id)
        if program_degree is None:
            raise ErrorMessage(get_str('INVALID_REF', ref_name='program degree id', key=program_degree_id))

        # Store the data in the object
        self.course_name = course_name
        self.course_code = course_code
        self.course_type_id = course_type_id
        self.since_semester_id = since_semester.id
        if ends is not None:
            self.ends_semester_id = ends_semester.id
        self.program_id = program_degree.id

    def get_couse_type(self):
        pass

    def get_since(self):
        pass

    def get_ends(self):
        pass

    def get_program(self):
        pass

    def edit_cilos(self, cilos: dict):
        pass

    def edit_assessment_method(self, methods: dict):
        pass

    def get_course_cilos(self):
        pass

    def get_course_assessment_methods(self):
        pass

    def get_course_prerequisites(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @classmethod
    def find_course_by_id(cls, id):
        return cls.query.filter_by(id=id).first()