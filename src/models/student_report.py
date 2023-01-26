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

    def get_cilo_performance(self, weights=None, cilo_weights=None):
        if weights is None or cilo_weights is None:
            report_obj = models.report.Report.find_report_by_id(self.report_id)
            weights, cilo_weights = report_obj.get_weights_matrix()

        result = db.session.query(
            models.grade_item.GradeItem,
            models.assessment_method.AssessmentMethod,
            StudentReport)\
            .filter(models.grade_item.GradeItem.student_report_id==self.id)\
            .join(models.grade_item.GradeItem, models.grade_item.GradeItem.student_report_id==StudentReport.id)\
            .join(models.assessment_method.AssessmentMethod, 
                models.assessment_method.AssessmentMethod.id==models.grade_item.GradeItem.assessment_method_id)\
            .all()

        score_raw = [0.0 for _ in range(len(cilo_weights))]
        for aidx, row in enumerate(result):
            grade_item = row[0]
            assessment_method = row[1]
            for idx in range(len(cilo_weights)):
                score_raw[idx] += grade_item.score * weights[idx][aidx]
        
        score = [0.0 for _ in range(len(cilo_weights))]
        for i in range(len(score_raw)):
            score[i] = score_raw[i] / cilo_weights[i]

        return score

    @classmethod
    def find_student_report_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_student_reports_by_report_id(cls, report_id: int):
        return cls.query.filter_by(report_id=report_id)