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

from models.cilo import CILO
from models.course import Course


VERSION = 'v1'
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/dependencies'

class Dependencies(Resource):

    @restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def get(self):
        degree_id = request.args.get('degree_id', '')
        courses = Course.find_course_by_keyword('')
        courses_json = [course.json(
            request_cilos=True, 
            request_related_cilos=True
            ) for course in courses]
        return {'courses': courses_json}, 200
