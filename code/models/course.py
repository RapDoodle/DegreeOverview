# -*- coding: utf-8 -*-
import models

from flask_language import current_language
from sqlalchemy.sql import text

from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from utils.validation import is_valid_length
from models.saveable_model import SaveableModel


class Course(SaveableModel):
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
    program_degree_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    revision = db.Column(db.Integer, default=0)

    def __init__(self, course_name, course_code, course_type_id, program_degree_id):
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
        
        program_degree = models.program_degree.ProgramDegree.find_program_degree_by_id(program_degree_id)
        if program_degree is None:
            raise ErrorMessage(get_str('INVALID_REF', ref_name='program degree id', key=program_degree_id))

        # Store the data in the object
        self.course_name = course_name
        self.course_code = course_code
        self.course_type_id = course_type_id
        self.program_degree_id = program_degree.id

    def add_cilos(self, cilos: list):
        """Add CILOs to the current course
        
        Args:
            cilos: a list of dictionaries containing the information of ALL the CILOs
                An example of the list goes as follows:
                    [
                        {
                            "cilo_index": 0,
                            "cilo_description": "Learn how to copy and paste code.",
                            "depending_cilos": [144, 128]  // The id of the denpended CILO
                        },
                        {
                            "cilo_index": 1,
                            "cilo_description": "Know the basics of how to use Notepad++.",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 2,
                            "cilo_description": "Learn the fundamental principles of crashing a system.",
                            "depending_cilos": []
                        },
                    ]
        """
        for cilo in cilos:
            cilo_obj = models.cilo.CILO(self.id, cilo['cilo_index'], cilo['cilo_description'], 0)
            cilo_obj.save()

            # Add dependency relationships
            for denpend_cilo_id in cilo['depending_cilos']:
                linkage_obj = models.cilo_dependency.CILODependency(self.id, cilo_obj.id, denpend_cilo_id)
                linkage_obj.save()

    def revise_course(self, cilos: list, methods: list):
        """Perform a course revision. In other words, update the course's CILOs and assessment methods

        Args:
            cilos: a list of dictionaries containing the information of ALL the CILOs
                An example of the list goes as follows:
                    [
                        {
                            "id": 15,
                            "cilo_index": 0,
                            "cilo_description": "Modified text.",
                            "depending_cilos": [144, 128]  // The id of the denpended CILO
                        },
                        {
                            "id": 16,
                            "cilo_index": 2,
                            "cilo_description": "Know the basics of how to use Notepad++.",
                            "depending_cilos": []
                        },
                        {
                            "id": 17,
                            "cilo_index": 1,
                            "cilo_description": "Learn how to crash a system.",
                            "depending_cilos": []
                        },
                    ]
            methods: a list of dictionaries containing the information of ALL the 
                assessment methods. An example of the list goes as follows:
                    [
                        {
                            "id": 16,
                            "method_index": 0,
                            "method_name": "Assignments",
                            "weight": 40
                        },
                        {
                            "id": 17,
                            "method_index": 1,
                            "method_name": "Group project",
                            "weight": 30
                        },
                        {
                            "id": 18,
                            "method_index": 2,
                            "method_name": "Final examination",
                            "weight": 30
                        },
                    ]
        """
        pass


    def edit_cilos(self, cilos: list):
        for cilo in cilos:
            cilo_obj = models.cilo.CILO.find_cilo_by_id(cilo['id'])
            if cilo_obj is None:
                raise ErrorMessage(get_str('INVALID_MODIFICATION'))
            if cilo_obj.course_id != self.id:
                raise ErrorMessage(get_str('NOT_FOUND_OBJECT', object_name='CILO'))
            cilo_obj.edit_cilo(cilo, self.revision + 1)
        self.revision = self.revision + 1
        self.save()

    def add_assessment_methods(self, methods: list):
        """Add assessment method to the current course
        
        Args:
            methods: a list of dictionaries containing the information of ALL the 
                assessment methods. An example of the list goes as follows:
                    [
                        {
                            "method_index": 0,
                            "method_name": "Assignments",
                            "weight": 40,
                            "cilos_addressed": []  // 
                        },
                        {
                            "method_index": 1,
                            "method_name": "Group project",
                            "weight": 30,
                            "cilos_addressed": []
                        },
                        {
                            "method_index": 2,
                            "method_name": "Final examination",
                            "weight": 30,
                            "cilos_addressed": []
                        },
                    ]'
                Note: In the list `cilos_addressed`, it contains the INDEX of 
                    the course's CILOs, NOT the id of the CILO.
        """
        # Check for "cilos_addressed"
        for method in methods:
            if len(method['cilos_addressed']) == 0:
                raise ErrorMessage(get_str('NO_RELATED_CILO'))

        # Check for the weights (in total, it should add up to 100%)
        weight_total = 0
        for method in methods:
            weight_total = weight_total + method['weight']
        if weight_total != 100:
            raise ErrorMessage('INVALID_TOTAL_WEIGHT')
        
        # Add methods to database
        for method in methods:
            method_obj = models.assessment_method.AssessmentMethod(
                self.id, method['method_name'], method['weight'], method['cilos_addressed'], method['since'], 0)
            method_obj.save()

            # Add linkage between assessment method and CILO
            for cilo_index in method['cilos_addressed']:
                linkage_obj = models.cilo_assessment_method.CILOAssessmentMethod(self.id, method_obj.id, cilo_index)
                linkage_obj.save()

    def edit_assessment_methods(self, methods: list):
        """Edit assessment methods of the current course
        
        
        """
        # Check for the weights (in total, it should add up to 100%)
        weight_total = 0
        for method in methods:
            weight_total = weight_total + method['weight']
        if weight_total != 100:
            raise ErrorMessage('INVALID_TOTAL_WEIGHT')

        for method in methods:
            method_obj = models.assessment_method.find_assessment_method_by_id(method['id'])
            if method_obj is None:
                raise ErrorMessage(get_str('NOT_FOUND_OBJECT', object_name='method'))
            method_obj.edit_assessment_methods()

    def get_course_prerequisites(self):
        return db.session.query(Course).from_statement(
            text("""SELECT * FROM course, cilo 
                WHERE course.id = cilo.course_id AND cilo.id IN 
                (SELECT DISTINCT cilo_dependency.depending_cilo_id 
                FROM course, cilo, cilo_dependency 
                WHERE course.id = cilo.course_id 
                AND cilo.id = cilo_dependency.cilo_id 
                AND course.id=:course_id)""")
        ).params(course_id=self.id).all()

    def get_dependent_courses(self):
        return db.session.query(Course).from_statement(
            text("""SELECT * FROM course, cilo, cilo_dependency 
                WHERE course.id = cilo.course_id 
                AND cilo.id = cilo_dependency.cilo_id
                AND cilo_dependency.depending_cilo_id IN
                (SELECT cilo.id FROM course, cilo 
                WHERE course.id = cilo.course_id 
                AND course.id=:course_id)""")
        ).params(course_id=self.id).all()

    def get_couse_type(self):
        return models.course_type.CourseType.find_course_type_by_id(self.course_type_id)

    def get_since(self):
        return models.semester.Semester.find_semester_by_id(self.since_semester_id)

    def get_ends(self):
        return models.semester.Semester.find_semester_by_id(self.ends_semester_id)

    def get_program(self):
        return models.program_degree.ProgramDegree.find_program_degree_by_id(self.program_degree_id)

    def get_cilos(self):
        return models.cilo.CILO.find_cilos_by_course_id(self.id)

    def get_assessment_methods(self):
        return models.program_degree.ProgramDegree.find_program_degree_by_id(self.program_degree_id)

    @classmethod
    def find_course_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_course_by_keyword(cls, keyword):
        return cls.query.filter(
            db.or_(
                cls.course_name.like('%' + keyword + '%'), 
                cls.course_code.like('%' + keyword + '%'))).all()
