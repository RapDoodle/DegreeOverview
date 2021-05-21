# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import redirect
from flask import url_for
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

blueprint = Blueprint('dashboard', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET', 'POST'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
def dashboard():
    return redirect(url_for('courses.courses'))