import unittest

from flask import request

from base import BaseTestCase

from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER


class TestUser(BaseTestCase):

    # Ensure user can register
    def test_user_type(self):
        # Student
        self.assertTrue(self.test_student.is_student(self.test_student.get_id()), 'Student type mismatch')
        self.assertFalse(self.test_student.is_lecturer(self.test_student.get_id()), 'Student type mismatch')
        self.assertFalse(self.test_student.is_course_designer(self.test_student.get_id()), 'Student type mismatch')
        self.assertEqual(self.test_student.get_user_type(), STUDENT, 'Student type mismatch')

        # Lecturer
        self.assertFalse(self.test_staff.is_student(self.test_staff.get_id()), 'Lecturer type mismatch')
        self.assertTrue(self.test_staff.is_lecturer(self.test_staff.get_id()), 'Lecturer type mismatch')
        self.assertFalse(self.test_staff.is_course_designer(self.test_staff.get_id()), 'Lecturer type mismatch')
        self.assertEqual(self.test_staff.get_user_type(), LECTURER, 'Lecturer type mismatch')

        # Course Designer
        self.assertFalse(self.test_course_designer.is_student(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.test_course_designer.is_lecturer(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.test_course_designer.is_course_designer(self.test_course_designer.get_id()), 'Course Designer type mismatch')
        self.assertEqual(self.test_course_designer.get_user_type(), COURSE_DESIGNER, 'Course Designer type mismatch')

    def test_verify_password(self):
        # Correct password
        self.assertTrue(self.test_student.verify_password('12345678'))
        self.assertTrue(self.test_staff.verify_password('12345678'))
        self.assertTrue(self.test_course_designer.verify_password('12345678'))

        # Incorrect password
        self.assertFalse(self.test_student.verify_password('wrongpwd'))
        self.assertFalse(self.test_staff.verify_password('wrongpwd'))
        self.assertFalse(self.test_course_designer.verify_password('wrongpwd'))