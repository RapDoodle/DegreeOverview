# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import flash
from core.lang import get_str
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from models.course import Course

blueprint = Blueprint('course_info', __name__, template_folder='templates')


@blueprint.route('/course/<int:course_id>', methods=['GET'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('course_info.html')
def info(course_id):
    course = Course.find_course_by_id(course_id)
    if course is None:
        flash(get_str('COURSE_NOT_FOUND'))
        return redirect(url_for('courses.courses'))
    return {'course': course}