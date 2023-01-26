# -*- coding: utf-8 -*-
import pandas as pd
from xlrd.biffh import XLRDError
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
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/excel_parser'

class ExcelParser(Resource):

    @restricted_access(allowed=[COURSE_DESIGNER], return_json=True)
    @excpetion_handler
    def post(self):
        try:
            df = pd.read_excel(request.files.get('file'), sheet_name='Sheet1')
        except (IOError, XLRDError):
            raise ErrorMessage(get_str('INVALID_EXCEL'))
        columns = [column for column in df.columns]
        json_list = []
        for index, row in df.iterrows():
            json_obj = {
                'index': index
            }
            for column in columns:
                json_obj[column] = row[column]
            json_list.append(json_obj)
        return {'content': json_list}, 200
