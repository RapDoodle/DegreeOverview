from flask_testing import TestCase
from flask import current_app

from core.db import db
from core.lang import get_str
from core.startup import create_app as get_app

from models.user import User
from models.staff import Staff
from models.student import Student
from models.course_designer import CourseDesigner

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = get_app(name=__name__, config_name='test')
        app.template_folder = '../templates'
        return app

    def setUp(self):
        # Create a student (staff)
        self.test_student = Student('teststudent1', '12345678', 'Test Student 1', 'n830000000')
        self.test_student.save()

        # Create a lecturer (staff)
        self.test_staff = Staff('testlecturer1', '12345678', 'Test Lecturer 1', 'a100000000')
        self.test_staff.save()

        # Create a course designer
        self.test_course_designer = CourseDesigner('testcd1', '12345678', 'Test Course Designer 1', 'a100000001')
        self.test_course_designer.save()

    def tearDown(self):
        # pass
        db.session.remove()
        db.drop_all()

    def get_lang(self, response) -> str:
        """Return the name of the language given a response"""
        for entry in response.headers.getlist('Set-Cookie'):
            if str(entry).startswith('lang='):
                return entry.split(';')[0].split('=')[1]

    def assertInResponseWithLang(self, key: str, response):
        """Assert whether a string is the response with translation"""
        self.assertIn(bytearray(get_str(key, language=response), 'utf8'), response.data)
