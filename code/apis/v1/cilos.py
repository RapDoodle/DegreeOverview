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


VERSION = 'v1'
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/search/cilo'

class Cilos(Resource):

    @restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def get(self):
        keyword = request.args.get('keyword', '')
        cilos = [cilo.json() for cilo in CILO.find_cilo_by_keyword(keyword=keyword)]
        return {'cilos': cilos}, 200
