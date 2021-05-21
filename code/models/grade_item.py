# -*- coding: utf-8 -*-
import models
from core.db import db


class GradeItem(db.Model):
    """A student's grade entry"""
    __tablename__ = 'report_entry'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_report_id = db.Column(db.Integer, db.ForeignKey('student_report.id'))
    assessment_method_id = db.Column(db.Integer, db.ForeignKey('assessment_method.id'))
    score = db.Column(db.Float)

    def __init__(self, student_report_id, assessment_method_id, score, use_percentage=False):
        """When `use_percentage` is specified, the percentage should be a 
        float ranging from 0 to 100. The `use_percentage` option is only
        used for testing purposes.
        """
        self.student_report_id = student_report_id
        self.assessment_method_id = assessment_method_id
        self.assessment_method_id = assessment_method_id
        if use_percentage:
            assessment_method_obj = models.assessment_method.AssessmentMethod.\
                find_assessment_method_by_id(assessment_method_id)
            self.score = (score/100) * assessment_method_obj.weight
        else:
            self.score = score

    @classmethod
    def find_grade_item_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()