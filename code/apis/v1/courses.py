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

from models.course import Course


VERSION = 'v1'
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/courses'

class Courses(Resource):

    @restricted_access(allowed=[COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def post(self):
        content = request.get_json()
        print(content)
        Course.add_course(content)
        return {'message': get_str('CREATED', obj_name=get_str('ACOURSE'))}, 201

    @restricted_access(allowed=[COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def patch(self):
        content = request.get_json()
        course = Course.find_course_by_id(content['course_id'])
        if course is None:
            raise ErrorMessage(get_str('NOT_FOUND_OBJECT', object_name='course'))
        course.modify_course(content)
        return {'message': get_str('COURSE_UPDATED', course_name=course.course_name)}, 200
