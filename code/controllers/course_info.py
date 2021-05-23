# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from core.lang import get_str
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from utils.converter import to_int
from models.course import Course
from models.report import Report

blueprint = Blueprint('course_info', __name__, template_folder='templates')


@blueprint.route('/course/<int:course_id>', methods=['GET'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('course_info.html', on_error_redirect_to='courses.courses')
def info(course_id):
    course = Course.find_course_by_id(course_id)
    analysis = {}
    if course is None:
        flash(get_str('COURSE_NOT_FOUND'))
        return redirect(url_for('courses.courses'))
    if session['user_type'] == COURSE_DESIGNER:
        all_reports = Report.find_reports_by_course_id(course.id)
        years = [report.get_semester().year for report in all_reports]
        # Remove duplicates
        years = list(set(years))
        analysis['years'] = years
        year = to_int(request.args.get('year', -1))
        # Check if it is a valid year (exists for the current course report)
        if year not in years:
            year = years[-1] if len(years) > 0 else -1
        analysis['year_selected'] = year
        if year > 0:
            reports = Report.find_course_reports_by_year(course_id=course.id, year=year)
            if len(reports) > 0:
                # Since there will be at least one report
                course_version = reports[0].get_course_version()
                cilos = course.get_cilos(course_version.id)
                analysis['reports'] = reports
                analysis['cilos'] = cilos
                analysis['scores'] = Report.get_cilo_performance_by_year(course.id, 2016)
    return {
        'course': course,
        'analysis': analysis
    }