# -*- coding: utf-8 -*-
from models import course
import models
from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, course_id, semester_id):
        self.course_id = course_id
        self.semester_id = semester_id

    def query_full_report(self):
        return db.session.query(
            models.report.Report,
            models.student_report.StudentReport,
            models.grade_item.GradeItem,
            models.assessment_method.AssessmentMethod,
            models.course_version.CourseVersion)\
            .filter(
                models.report.Report.id==self.id,
                models.student_report.StudentReport.report_id==models.report.Report.id,
                models.grade_item.GradeItem.student_report_id==models.student_report.StudentReport.id,
                models.assessment_method.AssessmentMethod.id==models.grade_item.GradeItem.assessment_method_id,
                models.course_version.CourseVersion.id==models.assessment_method.AssessmentMethod.course_version_id)

    def get_course_version(self):
        print('--------------', self.query_full_report().all())
        result = self.query_full_report().first()
        if result is None:
            raise ErrorMessage(get_str('INVALID_REPORT'))
        return result[4]

    def get_weights_matrix(self):
        print(self.query_full_report().first())
        result = self.query_full_report().first()
        if result is None:
            raise ErrorMessage(get_str('INVALID_REPORT'))
            
        course_id = result[-1].course_id
        course_version_id = result[-1].id
        course = models.course.Course.find_course_by_id(course_id)
        cilos = course.get_cilos(course_version_id=course_version_id)
        assessment_methods = course.get_assessment_methods(course_version_id=course_version_id)

        # Allocate an m * n matrix where m is the number of CILOs and
        # n is the number of assessment method
        weights = [[0.0 for _ in range(len(assessment_methods))] for _ in range(len(cilos))]
        cilo_weights = [0.0 for _ in range(len(cilos))]

        for i, assessment_method in enumerate(assessment_methods):
            related_cilos = assessment_method.get_cilos_addressed()
            for related_cilo in related_cilos:
                weight = 1 / len(related_cilos)
                weights[related_cilo.cilo_index-1][i] = weight
                cilo_weights[related_cilo.cilo_index-1] += weight * assessment_method.weight
        
        return weights, cilo_weights

    def get_report_cilo_performance(self):
        weights, cilo_weights = self.get_weights_matrix()
        total_score = [0.0 for _ in range(len(cilo_weights))]
        student_reports = models.student_report.StudentReport.find_student_reports_by_report_id(self.id).all()
        for student_report in student_reports:
            # Calculate the sum first
            total_score = [sum(x) for x in zip(student_report.get_cilo_performance(weights=weights, cilo_weights=cilo_weights), total_score)]
        num_reports = len(student_reports)
        return [score/num_reports for score in total_score]

    def get_semester(self):
        return models.semester.Semester.find_semester_by_id(self.semester_id)

    @classmethod
    def get_student_completed_courses(cls, student_id):
        """Note: the student_id is the id of student (eg. 2), not student id (eg. n830026000)"""
        return db.session.query(models.course.Course, Report, models.student_report.StudentReport)\
            .filter(models.student_report.StudentReport.student_id==student_id)\
            .join(models.course.Course, Report.course_id == models.course.Course.id)\
            .join(models.student_report.StudentReport, Report.id == models.student_report.StudentReport.report_id)\
            .all()

    @classmethod
    def find_report_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_reports_by_course_id(cls, course_id: int):
        return cls.query.filter_by(course_id=course_id).all()

    @classmethod
    def find_course_reports_by_year(cls, course_id: int, year: int):
        semesters = [semester.id for semester in models.semester.Semester.find_semesters_by_year(year=year)]
        return cls.query.filter(cls.course_id==course_id)\
            .filter(cls.semester_id.in_(semesters))\
            .all()

    @classmethod
    def get_cilo_performance_by_year(cls, course_id: int, year: int):
        course_reports = cls.find_course_reports_by_year(course_id=course_id, year=year)
        total_score = []
        for idx, course_report in enumerate(course_reports):
            if idx == 0:
                total_score = course_report.get_report_cilo_performance()
            else:
                total_score = [sum(x) for x in zip(course_report.get_report_cilo_performance(), total_score)]
        num_reports = len(course_reports)
        return [score/num_reports for score in total_score]
