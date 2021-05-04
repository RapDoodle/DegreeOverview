from functools import wraps

from flask import session
from flask import flash
from flask import redirect
from flask import url_for

from core.lang import get_str

STUDENT = 0
LECTURER = 1
COURSE_DESIGNER = 2

def restricted_access(allowed: list):
    def verify_access(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            print(session.get('user_id'))
            # No login credential found
            if not session.get('user_id'):
                flash(get_str('LOGIN_REQUIRED'))
                return redirect(url_for('login.login'))

            # Check for permission
            if session.get('user_type') not in allowed:
                flash(get_str('PERMISSION_DENIED'))
                return redirect(url_for('dashboard.dashboard'))

            return fn(*args, **kwargs)
        return wrapper
    return verify_access