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
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/search/cilo'

class Cilos(Resource):

    @restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def get(self):
        search_type = request.args.get('search_type', 'cilo')
        keyword = request.args.get('keyword', '')
        if search_type == 'cilo':
            cilos = [cilo.json() for cilo in CILO.find_cilo_by_keyword(keyword=keyword)]
        elif search_type == 'course':
            courses = Course.find_course_by_keyword(keyword=keyword)
            cilos = []
            for course in courses:
                for cilo in course.get_cilos():
                    cilos.append(cilo.json())
        else:
            raise ErrorMessage(get_str('INVALID_SEARCH_TYPE'))
        for cilo in cilos:
            cilo['course_name'] = Course.find_course_by_id(id=cilo['course_id']).course_name
        return {'cilos': cilos}, 200
