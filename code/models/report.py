# -*- coding: utf-8 -*-
import models
from core.db import db


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))

    def __init__(self, course_id, semester_id):
        self.course_id = course_id
        self.semester_id = semester_id

    def get_full_report(self):
        return db.session.query(Report, 
                models.student_report.StudentReport, 
                models.grade_item.GradeItem).filter(Report.id==self.id)\
            .join(models.student_report.StudentReport, models.student_report.StudentReport.report_id == Report.id)\
            .join(models.grade_item.GradeItem, models.student_report.StudentReport.id == models.student_report.StudentReport.id).all()

    @classmethod
    def get_student_completed_courses(cls, student_id):
        """Note: the student_id is the id of student, not student id (eg. n830026000)"""
        return db.session.query(models.course.Course, Report, models.student_report.StudentReport)\
            .filter(models.student_report.StudentReport.student_id==student_id)\
            .join(models.course.Course, Report.course_id == models.course.Course.id)\
            .join(models.student_report.StudentReport, Report.id == models.student_report.StudentReport.report_id)\
            .all()

    @classmethod
    def find_report_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()