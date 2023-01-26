# -*- coding: utf-8 -*-
from flask import current_app
from flask import request
from flask_restful import Resource

from core.lang import get_str
from core.exception import excpetion_handler
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from core.exception import ErrorMessage
from models.program import Program
from models.degree import Degree
from models.cilo import CILO
from models.course import Course


VERSION = 'v1'
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/dependencies'

class Dependencies(Resource):

    @restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def get(self):
        degree_id = request.args.get('degree', 1)
        degree_obj = Degree.find_degree_by_id(id=degree_id)
        if degree_obj is None:
            raise ErrorMessage(get_str('INVALID_INDEX'))
        courses = Course.find_courses_by_program_id(
            program_id=degree_obj.related_program_id, 
            recursive=True)
        courses_json = [course.json(
            request_cilos=True, 
            request_related_cilos=True
            ) for course in courses]
        return {'courses': courses_json}, 200
