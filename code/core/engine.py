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

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

default_context = {
    'get_str': get_str,
    'STUDENT': STUDENT,
    'LECTURER': LECTURER,
    'COURSE_DESIGNER': COURSE_DESIGNER
}

def render(*args, **kwargs):
    return render_template(*args, **kwargs, **default_context)


def render_context(template = ''):
    def context(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = {}
            try:
                returned = fn(*args, **kwargs)
                if returned is not None:
                    if type(returned) == dict:
                        data = returned
                    else:
                        return returned
            except (ErrorMessage, ErrorMessagePromise) as e:
                flash(str(e))
            except Exception as e:
                current_app.logger.critical(str(e))
                traceback.print_exc(file=sys.stdout)
                flash(get_str('INTERNAL_ERROR'))
            return render(template, data=data)
        return wrapper
    return context