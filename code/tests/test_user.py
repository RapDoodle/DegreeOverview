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

    """Override the exisiting setUp method since in this test case, we handle all user objects by ourselves."""
    def setUp(self):
        self.password = 'Testpassword@123'

        # Student
        self.student = Student('n830000000', self.password, 'Shawn WU', '1830000001')
        self.student.save(commit=True)

        # Lecturer
        self.lecturer = Lecturer('alicelee', self.password, 'Alice LEE', 'a200000001')
        self.lecturer.save(commit=True)

        # Course Designer
        self.cd = CourseDesigner('davidwong', self.password, 'David WONG', 'a200000002')
        self.cd.save(commit=True)

    def test_user_verify_password(self):
        # Student
        self.assertTrue(self.student.verify_password('Testpassword@123'))
        self.assertFalse(self.student.verify_password('wrongpassword'))

        # Lecturer
        self.assertTrue(self.lecturer.verify_password('Testpassword@123'))
        self.assertFalse(self.lecturer.verify_password('wrongpassword'))

        # Course Designer
        self.assertTrue(self.cd.verify_password('Testpassword@123'))
        self.assertFalse(self.cd.verify_password('wrongpassword'))

    def test_user_basic_getters(self):
        # Student
        self.assertEqual(self.student.get_full_name(), 'Shawn WU')
        self.assertEqual(self.student.get_student_id(), '1830000001')
        self.assertNotEqual(self.student.get_id(), None)
        self.assertEqual(self.student.get_username(), 'n830000000')

        # Lecturer
        self.assertEqual(self.lecturer.get_full_name(), 'Alice LEE')
        self.assertEqual(self.lecturer.get_staff_id(), 'a200000001')
        self.assertNotEqual(self.lecturer.get_id(), None)
        self.assertEqual(self.lecturer.get_username(), 'alicelee')

        # Course Designer
        self.assertEqual(self.cd.get_full_name(), 'David WONG')
        self.assertEqual(self.cd.get_staff_id(), 'a200000002')
        self.assertNotEqual(self.cd.get_id(), None)
        self.assertEqual(self.cd.get_username(), 'davidwong')

    def test_find_user_by_id(self):
        # Find the exisiting user by id
        self.assertEqual(Student.find_user_by_id(self.student.get_id()).get_id(), self.student.get_id())
        self.assertEqual(Lecturer.find_user_by_id(self.lecturer.get_id()).get_id(), self.lecturer.get_id())
        self.assertEqual(CourseDesigner.find_user_by_id(self.cd.get_id()).get_id(), self.cd.get_id())

        # Find non-exisiting user by id (id always starts at 1, should never become 0)
        self.assertEqual(Student.find_user_by_id(0), None)
        self.assertEqual(Lecturer.find_user_by_id(0), None)
        self.assertEqual(CourseDesigner.find_user_by_id(0), None)

    def test_find_user_by_username(self):
        # Find the exisiting user by username
        self.assertEqual(Student.find_user_by_username(self.student.get_username()).get_username(), self.student.get_username())
        self.assertEqual(Lecturer.find_user_by_username(self.lecturer.get_username()).get_username(), self.lecturer.get_username())
        self.assertEqual(CourseDesigner.find_user_by_username(self.cd.get_username()).get_username(), self.cd.get_username())

        # Find non-exisiting user by username
        self.assertEqual(Student.find_user_by_username('invalidusername'), None)
        self.assertEqual(Lecturer.find_user_by_username('invalidusername'), None)
        self.assertEqual(CourseDesigner.find_user_by_username('invalidusername'), None)
    
    def test_user_type(self):
        # Student
        self.assertTrue(self.student.is_student(self.student.get_id()), 'Student type mismatch')
        self.assertFalse(self.student.is_lecturer(self.student.get_id()), 'Student type mismatch')
        self.assertFalse(self.student.is_course_designer(self.student.get_id()), 'Student type mismatch')
        self.assertEqual(self.student.get_user_type(), STUDENT, 'Student type mismatch')

        # Lecturer
        self.assertFalse(self.lecturer.is_student(self.lecturer.get_id()), 'Lecturer type mismatch')
        self.assertTrue(self.lecturer.is_lecturer(self.lecturer.get_id()), 'Lecturer type mismatch')
        self.assertFalse(self.lecturer.is_course_designer(self.lecturer.get_id()), 'Lecturer type mismatch')
        self.assertEqual(self.lecturer.get_user_type(), LECTURER, 'Lecturer type mismatch')

        # Course Designer
        self.assertFalse(self.cd.is_student(self.cd.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.cd.is_lecturer(self.cd.get_id()), 'Course Designer type mismatch')
        self.assertTrue(self.cd.is_course_designer(self.cd.get_id()), 'Course Designer type mismatch')
        self.assertEqual(self.cd.get_user_type(), COURSE_DESIGNER, 'Course Designer type mismatch')

    def test_verify_password(self):
        # Correct password
        self.assertTrue(self.student.verify_password(self.password))
        self.assertTrue(self.lecturer.verify_password(self.password))
        self.assertTrue(self.cd.verify_password(self.password))

        # Incorrect password
        self.assertFalse(self.student.verify_password('wrongpwd'))
        self.assertFalse(self.lecturer.verify_password('wrongpwd'))
        self.assertFalse(self.cd.verify_password('wrongpwd'))
