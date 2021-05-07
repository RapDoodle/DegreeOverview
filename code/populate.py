from core.db import db
from core.startup import create_app

from models.student import Student
from models.lecturer import Lecturer
from models.course_designer import CourseDesigner



def main():
    app = create_app(name=__name__, config_name='dev')
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create a student
        Student('teststudent1', '12345678', 'Test Student 1', 'n830000000').save()

        # Create a lecturer (lecturer)
        Lecturer('testlecturer1', '12345678', 'Test Lecturer 1', 'a100000000').save()

        # Create a course designer
        CourseDesigner('testcd1', '12345678', 'Test Course Designer 1', 'a100000001').save()

if __name__ == '__main__':
    main()