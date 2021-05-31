# -*- coding: utf-8 -*-
import models
from sqlalchemy.sql import text
from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from utils.validation import is_valid_length
from utils.converter import to_int
from models.saveable_model import SaveableModel


class Course(SaveableModel):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(128))
    course_code = db.Column(db.String(16))
    course_type_id = db.Column(db.Integer, db.ForeignKey('course_type.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, course_name, course_code, course_type_id, program_id):
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
            raise ErrorMessage(get_str('INVALID_REF', ref_name='course type id', key_name=course_type_id))
        
        program = models.program.Program.find_program_by_id(program_id)
        if program is None:
            raise ErrorMessage(get_str('INVALID_REF', ref_name='program id', key_name=program_id))

        # Store the data in the object
        self.course_name = course_name
        self.course_code = course_code
        self.course_type_id = course_type_id
        self.program_id = program.id

    @classmethod
    def add_course(cls, content):
        """Add a course to the database

        Args:
            content (dict): The content of the course. 
                An example of the content goes as follows:
                    {
                        "course_name": "Software Engineering",
                        "course_code": "COMP3063",
                        "course_type_id": "1",
                        "program_id": 20,
                        "effective_since": 2012,
                        "cilos": [
                            {
                                "cilo_index": 1,
                                "cilo_description": "explain software development life cycle and key activities in each phase of the cycle.",
                                "depending_cilos": []
                            },
                            {
                                "cilo_index": 2,
                                "cilo_description": "apply UML to OO software development",
                                "depending_cilos": []
                            },
                            {
                                "cilo_index": 3,
                                "cilo_description": "plan a test in unit, module and system levels",
                                "depending_cilos": []
                            },
                            {
                                "cilo_index": 4,
                                "cilo_description": "manage a project through configuration management and cost estimation",
                                "depending_cilos": []
                            }
                        ],
                        "assessment_methods": [
                            {
                                "method_index": 1,
                                "method_name": "Assignments",
                                "weight": 40,
                                "cilos_addressed": [1]
                            },
                            {
                                "method_index": 2,
                                "method_name": "Group project",
                                "weight": 30,
                                "cilos_addressed": [1]
                            },
                            {
                                "method_index": 3,
                                "method_name": "Final examination",
                                "weight": 30,
                                "cilos_addressed": [1]
                            }
                        ]
                    }
        """
        course_obj = Course(
            course_name=content['course_name'], 
            course_code=content['course_code'], 
            course_type_id=content['course_type_id'], 
            program_id=content['program_id'])
        course_obj.save(commit=False)

        # Create a course version object
        course_version_obj = models.course_version.CourseVersion(
            course_id=course_obj.id,
            effective_since=content['effective_since'])
        course_version_obj.save(commit=False)

        # Add CILOs
        course_obj.add_cilos(
            cilos=content['cilos'],
            course_version_id=course_version_obj.id)

        # Add assessment methods
        course_obj.add_assessment_methods(
            methods=content['assessment_methods'], 
            course_version_id=course_version_obj.id)
            
        # Attempt to commit all changes
        db.session.commit()

    def add_cilos(self, cilos: list, course_version_id: int):
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
            course_version_id: The id number of the version entry.
        """
        for cilo in cilos:
            cilo_obj = models.cilo.CILO(self.id, cilo['cilo_index'], cilo['cilo_description'], course_version_id)
            cilo_obj.save(commit=False)

            # Add dependency relationships
            depending_cilos = cilo.get('depending_cilos', [])
            for depending_cilo_id in depending_cilos:
                linkage_obj = models.cilo_dependency.CILODependency(self.id, cilo_obj.id, depending_cilo_id)
                linkage_obj.save(commit=False)

    def add_assessment_methods(self, methods: list, course_version_id: int):
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
                    ]
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
            weight_total = weight_total + to_int(method['weight'], 'weight')
        if weight_total != 100:
            raise ErrorMessage(get_str('INVALID_TOTAL_WEIGHT'))
        
        # Add methods to database
        for method in methods:
            method_obj = models.assessment_method.AssessmentMethod(
                course_id=self.id, 
                method_name=method['method_name'], 
                weight=method['weight'], 
                course_version_id=course_version_id)
            method_obj.save(commit=False)

            # Add linkage between assessment method and CILO
            for cilo_index in method['cilos_addressed']:
                linkage_obj = models.cilo_assessment_method.CILOAssessmentMethod(self.id, method_obj.id, cilo_index)
                linkage_obj.save(commit=False)

    def modify_course(self, content: dict):
        """Perform a course revision. In other words, update the course's CILOs and assessment methods

        Args:
            content (dict): The content of the course. 
                An example of the content goes as follows:
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
        """
        current_cilos = self.get_cilos()
        current_assessment_methods = self.get_assessment_methods()

        # Length validation
        if len(current_cilos) != len(content['cilos']):
            raise ErrorMessage(get_str('CILO_NUM_MISMATCH'))

        new_course_vesion_obj = models.course_version.CourseVersion(
            course_id=self.id,
            effective_since=content['effective_since'])
        new_course_vesion_obj.save(commit=False)

        for current_cilo, new_cilo in zip(current_cilos, content['cilos']):
            # Check for CILO index
            if current_cilo.cilo_index != to_int(new_cilo['cilo_index'], 'CILO index'):
                raise ErrorMessage(get_str('INVALID_INDEX_OF',  index=new_cilo['cilo_index'], correct_index=current_cilo.cilo_index))

            new_cilo_obj = models.cilo.CILO(self.id, current_cilo.cilo_index, new_cilo['cilo_description'], new_course_vesion_obj.id)
            new_cilo_obj.save(commit=False)

            # Linkage update for the CILOs this CILO dependes on.
            cilos_depending_on = current_cilo.get_dependee_cilos()

            # There is nothing wrong with the current CILO does not depend on any CILO.
            if cilos_depending_on is not None:
                for dependee in cilos_depending_on:
                    dependee.cilo_id = new_cilo_obj.id
                    dependee.save(commit=False)

            # Linkage update for the CILOs that depends on the current CILO.
            cilos_depended_on = current_cilo.get_dependeding_cilos()

            # There is nothing wrong with the current CILO was not depended by any CILO.
            if cilos_depended_on is not None:
                for depending in cilos_depended_on:
                    depending.depending_cilo_id = new_cilo_obj.id
                    depending.save(commit=False)

        # The logic is exactly the same as adding assessment methods
        self.add_assessment_methods(
            methods=content['assessment_methods'], 
            course_version_id=new_course_vesion_obj.id)

        db.session.commit()

    def get_course_prerequisites(self):
        """In the returned list, for each entry, the first pararmeter
        is the Course object and the second parameter is the CILO object.
        Equivalent SQL:
            SELECT * FROM course, cilo 
            WHERE course.id = cilo.course_id AND cilo.id IN 
            (SELECT DISTINCT cilo_dependency.depending_cilo_id 
            FROM course, cilo, cilo_dependency 
            WHERE course.id = cilo.course_id 
            AND cilo.id = cilo_dependency.cilo_id 
            AND course.id=:course_id)
        """
        depending_cilo_ids = [cilo[0].depending_cilo_id for cilo in db.session.query(
            models.cilo_dependency.CILODependency,
            models.cilo.CILO)\
            .filter(models.cilo.CILO.id==models.cilo_dependency.CILODependency.cilo_id)\
            .filter(Course.id==models.cilo.CILO.course_id)\
            .filter(models.cilo.CILO.course_id==self.id).all()]
        return db.session.query(Course, models.cilo.CILO)\
            .filter(Course.id==models.cilo.CILO.course_id)\
            .filter(models.cilo.CILO.id.in_(depending_cilo_ids)).all()

    def get_dependent_courses(self):
        """In the returned list, for each entry, the first pararmeter
        is the Course object, the second parameter is the CILO object,
        and the third parameter is the CILODependency object
        Equivalent SQL:
            SELECT * FROM course, cilo, cilo_dependency 
            WHERE course.id = cilo.course_id 
            AND cilo.id = cilo_dependency.cilo_id
            AND cilo_dependency.depending_cilo_id IN
            (SELECT cilo.id FROM course, cilo 
            WHERE course.id = cilo.course_id 
            AND course.id=:course_id)
        """
        depending_cilo_ids = [cilo[0].id for cilo in db.session.query(
            models.cilo.CILO,
            models.course.Course)\
            .filter(models.course.Course.id==self.id)\
            .filter(models.course.Course.id==models.cilo.CILO.course_id)\
            .all()]
        return db.session.query(
            models.course.Course, 
            models.cilo.CILO,
            models.cilo_dependency.CILODependency)\
            .filter(Course.id==models.cilo.CILO.course_id)\
            .filter(models.cilo.CILO.id==models.cilo_dependency.CILODependency.cilo_id)\
            .filter(models.cilo_dependency.CILODependency.depending_cilo_id.in_(depending_cilo_ids))\
            .all()

    def get_cilos(self, course_version_id=None):
        return models.cilo.CILO.find_cilos_by_course_id(
            course_id=self.id,
            course_version_id=course_version_id if course_version_id is not None \
                else models.course_version.CourseVersion.find_course_latest_version(self.id).id)

    def get_assessment_methods(self, course_version_id=None):
        return models.assessment_method.AssessmentMethod.find_assessment_methods_by_course_id(
            course_id=self.id,
            course_version_id=course_version_id if course_version_id is not None \
                else models.course_version.CourseVersion.find_course_latest_version(self.id).id)

    def json(self, request_cilos=False, request_related_cilos=False):
        json_obj = {
            'course_id': self.id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_type': self.get_couse_type().name,
            'program': self.get_program().name
        }
        if request_cilos:
            json_obj['cilos'] = [cilo.json(request_related_cilos) for cilo in self.get_cilos()]
        return json_obj

    def get_couse_type(self):
        return models.course_type.CourseType.find_course_type_by_id(self.course_type_id)

    def get_since(self):
        return models.semester.Semester.find_semester_by_id(self.since_semester_id)

    def get_ends(self):
        return models.semester.Semester.find_semester_by_id(self.ends_semester_id)

    def get_program(self):
        return models.program.Program.find_program_by_id(self.program_id)

    @classmethod
    def find_course_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_courses_by_program_id(cls, program_id, recursive=False):
        courses = cls.query.filter_by(program_id=program_id).all()
        if recursive:
            courses_add = []
            course_ids = [course.id for course in courses]
            for course in courses:
                prerequisites = course.get_course_prerequisites()
                for prerequisite_course in prerequisites:
                    if prerequisite_course[0].id not in course_ids:
                        courses_add.append(prerequisite_course[0])
                        course_ids.append(prerequisite_course[0].id)
            for course in courses_add:
                courses.append(course)
        return courses

    @classmethod
    def find_courses_cilo_by_keyword(cls, keyword: str) -> list:
        latest_versions = [cilo.id 
        for cilo in models.cilo.CILO.query.filter(models.cilo.CILO.course_version_id)\
                    .group_by(models.cilo.CILO.course_id)\
                    .having(models.cilo.CILO.course_version_id==db.func.max(models.cilo.CILO.course_version_id))\
                    .all()]
        return db.session.query(Course, models.cilo.CILO)\
            .filter(Course.id==models.cilo.CILO.course_id)\
            .filter(models.cilo.CILO.course_version_id.in_(latest_versions))\
            .filter(db.or_(
                models.cilo.CILO.cilo_description.like('%' + keyword + '%'),
                cls.course_name.like('%' + keyword + '%'),
                cls.course_code.like('%' + keyword + '%')))\
            .all()

    @classmethod
    def find_course_by_keyword(cls, keyword):
        return cls.query.filter(
            db.or_(
                cls.course_name.like('%' + keyword + '%'), 
                cls.course_code.like('%' + keyword + '%'))).all()
