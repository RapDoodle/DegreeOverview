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

from core.lang import render_with_lang
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

from models.user import User


blueprint = Blueprint('test', __name__, template_folder='templates')

@blueprint.route('/test/<name>', methods=['GET', 'POST'])
def test_route(name):
    session['user_type'] = 0
    return render_with_lang(name + '.html')