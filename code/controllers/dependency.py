# -*- coding: utf-8 -*-
from core.exception import ErrorMessage
from operator import index
from flask import Blueprint
from flask import session
from flask import request
from flask import flash
from core.lang import get_str
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER

blueprint = Blueprint('dependency', __name__, template_folder='templates')

@blueprint.route('/dependency', methods=['GET'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('dependency.html')
def dependency():
    return redirect(url_for('dependency.dependency'))
#FIXME: Server internal error.