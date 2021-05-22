# -*- coding: utf-8 -*-
import models
from core.db import db
from core.lang import get_str
from core.exception import ErrorMessage

class StudentReport(db.Model):
    """A student's grade entry"""
    __tablename__ = 'student_report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, report_id, student_id):
        self.report_id = report_id
        self.student_id = student_id

    def get_cilo_performance(self):
        result = db.session.query(
            models.course_version.CourseVersion, 
            models.report.Report,
            StudentReport,
            models.grade_item.GradeItem,
            models.assessment_method.AssessmentMethod)\
            .filter(models.report.Report.id==self.report_id)\
            .join(models.report.Report, models.report.Report.id==StudentReport.report_id)\
            .join(models.grade_item.GradeItem, models.grade_item.GradeItem.student_report_id==StudentReport.id)\
            .join(models.assessment_method.AssessmentMethod, \
                models.assessment_method.AssessmentMethod.id==models.grade_item.GradeItem.assessment_method_id)\
            .join(models.course_version.CourseVersion,
                models.course_version.CourseVersion.id==models.assessment_method.AssessmentMethod.course_version_id)\
            .first()
        if result is None:
            raise ErrorMessage(get_str('INVALID_REPORT'))
        course_id = result[0].course_id
        course_version_id = result[0].id
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

        result = db.session.query(
            models.grade_item.GradeItem,
            models.assessment_method.AssessmentMethod,
            StudentReport)\
            .filter(models.grade_item.GradeItem.student_report_id==self.id)\
            .join(models.grade_item.GradeItem, models.grade_item.GradeItem.student_report_id==StudentReport.id)\
            .join(models.assessment_method.AssessmentMethod, 
                models.assessment_method.AssessmentMethod.id==models.grade_item.GradeItem.assessment_method_id)\
            .all()

        score_raw = [0.0 for _ in range(len(cilos))]
        for aidx, row in enumerate(result):
            grade_item = row[0]
            assessment_method = row[1]
            for idx in range(len(cilos)):
                score_raw[idx] += grade_item.score * weights[idx][aidx]
        
        score = [0.0 for _ in range(len(cilos))]
        for i in range(len(score_raw)):
            score[i] = score_raw[i] / cilo_weights[i]

        return score, cilos

    @classmethod
    def find_report_entry_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()