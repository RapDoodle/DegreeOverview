# -*- coding: utf-8 -*-
import sys
import traceback
from functools import wraps

from flask import flash
from flask import render_template
from flask import current_app

from core.lang import get_str
from core.exception import ErrorMessage
from core.exception import ErrorMessagePromise
from core.db import db

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

default_context = {
    'get_str': get_str,
    'STUDENT': STUDENT,
    'LECTURER': LECTURER,
    'COURSE_DESIGNER': COURSE_DESIGNER,
    'enumerate': enumerate
}

def render(*args, **kwargs):
    return render_template(*args, **kwargs, **default_context), kwargs.get('status_code', 200)


def render_context(template = '', commit_on_success=True, rollback_on_exception=True):
    def context(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = {}
            status_code = 200
            try:
                returned = fn(*args, **kwargs)
                if commit_on_success:
                    db.session.commit()
                if returned is not None:
                    if type(returned) == dict:
                        data = returned
                    else:
                        return returned
            except (ErrorMessage, ErrorMessagePromise) as e:
                flash(str(e))
                status_code = 400
                if rollback_on_exception:
                    db.session.rollback()
            except Exception as e:
                current_app.logger.critical(str(e))
                traceback.print_exc(file=sys.stdout)
                flash(get_str('INTERNAL_ERROR'))
                status_code = 500
                if rollback_on_exception:
                    db.session.rollback()
            return render(template, data=data, status_code=status_code)
        return wrapper
    return context