# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import get_flashed_messages
from flask import session
from flask_language import current_language

from core.engine import render_context
from core.lang import lang
from core.lang import get_str
from core.db import db
from core.exception import ErrorMessage

from models.user import User
from models.course import Course
from models.course_version import CourseVersion

blueprint = Blueprint('courses', __name__, template_folder='templates')


@blueprint.route('/courses', methods=['GET', 'POST'])
@render_context('courses.html')
def courses():
    pass


@blueprint.route('/courses/add', methods=['POST'])
@render_context('courses.html', commit_on_success=False, rollback_on_exception=False)
def add_course():
    if request.method == 'POST':
        content = request.get_json()
        Course.add_course(content)
        flash(get_str('CREATED', obj_name=get_str('ACOURSE')))


@blueprint.route('/courses/edit', methods=['POST'])
@render_context('courses.html', commit_on_success=True, rollback_on_exception=True)
def modify_course():
    if request.method == 'POST':
        content = request.get_json()
        course = Course.find_course_by_id(content['course_id'])
        if course is None:
            raise ErrorMessage(get_str('NOT_FOUND_OBJECT', object_name='course'))
        course.modify_course(content)


@blueprint.route('/courses/', methods=['GET', 'POST'])
def empty_redirect():
    return redirect(url_for('courses.courses'))
