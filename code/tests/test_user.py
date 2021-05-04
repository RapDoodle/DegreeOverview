import unittest

from flask import request

from base import BaseTestCase

from models.user import User
from models.lecturer import Lecturer
from models.student import Student
from models.course_designer import CourseDesigner

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER


class TestUser(BaseTestCase):

    def test_user_verify_password(self):
        # Student
        student = Student('student1', 'Testpassword@123', 'Dummy Student', 'n830000001')
        self.assertTrue(student.verify_password('Testpassword@123'))
        self.assertFalse(student.verify_password('wrongpassword'))

        # Lecturer
        lecturer = Lecturer('lecturer1', 'Testpassword@123', 'Test Lecturer 1', 'a200000001')
        self.assertTrue(lecturer.verify_password('Testpassword@123'))
        self.assertFalse(lecturer.verify_password('wrongpassword'))

        # Course Designer
        cd = CourseDesigner('student1', 'Testpassword@123', 'Dummy Student', 'a200000002')
        self.assertTrue(cd.verify_password('Testpassword@123'))
        self.assertFalse(cd.verify_password('wrongpassword'))

    
    def test_user_type(self):
        # Student
        self.assertTrue(self.test_student.is_student(self.test_student.get_id()), 'Student type mismatch')
        self.assertFalse(self.test_student.is_lecturer(self.test_student.get_id()), 'Student type mismatch')
        self.assertFalse(self.test_student.is_course_designer(self.test_student.get_id()), 'Student type mismatch')
        self.assertEqual(self.test_student.get_user_type(), STUDENT, 'Student type mismatch')

        # Lecturer
        self.assertFalse(self.test_lecturer.is_student(self.test_lecturer.get_id()), 'Lecturer type mismatch')
        self.assertTrue(self.test_lecturer.is_lecturer(self.test_lecturer.get_id()), 'Lecturer type mismatch')
        self.assertFalse(self.test_lecturer.is_course_designer(self.test_lecturer.get_id()), 'Lecturer type mismatch')
        self.assertEqual(self.test_lecturer.get_user_type(), LECTURER, 'Lecturer type mismatch')

        # Course Designer
        self.assertFalse(self.test_course_designer.is_student(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.test_course_designer.is_lecturer(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.test_course_designer.is_course_designer(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertEqual(self.test_course_designer.get_user_type(), COURSE_DESIGNER, 'Course Designer type mismatch')

    def test_verify_password(self):
        # Correct password
        self.assertTrue(self.test_student.verify_password('12345678'))
        self.assertTrue(self.test_lecturer.verify_password('12345678'))
        self.assertTrue(self.test_course_designer.verify_password('12345678'))

        # Incorrect password
        self.assertFalse(self.test_student.verify_password('wrongpwd'))
        self.assertFalse(self.test_lecturer.verify_password('wrongpwd'))
        self.assertFalse(self.test_course_designer.verify_password('wrongpwd'))