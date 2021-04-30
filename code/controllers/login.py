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

blueprint = Blueprint('login', __name__, template_folder='/templates')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    print(current_language)
    print(session['test_value'])
    session['test_value'] = 15
    # if request.method == 'POST':
    #     res = staff_login(request.values.get('username'), request.values.get('password'))
    #     if isinstance(res, dict) and len(res) == 3:
    #         session['user_id'] = res['user_id']
    #         session['is_staff'] = True
    #         session['username'] = res['username']
    #         return redirect(url_for('admin_dashboard.dashboard'))
    #     if isinstance(res, ErrorMessage):
    #         flash(res.get())
    return render_template('/login.html')

@blueprint.route('/login/', methods=['GET', 'POST'])
def login_redirect():
    return redirect(url_for('login.login'))

@blueprint.route('/logout', methods=['GET'])
# @staff_permission_required()
def logout():
    session.clear()
    return redirect(url_for('login.login'))