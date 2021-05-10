from core.db import db
from core.startup import create_app

from models.student import Student
from models.lecturer import Lecturer
from models.course_designer import CourseDesigner
from models.semester import Semester
from models.program_degree import ProgramDegree
from models.course_type import CourseType
from models.course import Course


def main():
    app = create_app(name=__name__, config_name='dev')
    with app.app_context():
        db.drop_all()
        db.create_all()

        populate_user()
        populate_semester()
        populate_degree()
        populate_type()
        populate_course()


def populate_user():
    # Create a student
    Student('teststudent1', '12345678', 'Test Student 1', 'n830000000').save()

    # Create a lecturer (lecturer)
    Lecturer('testlecturer1', '12345678', 'Test Lecturer 1', 'a100000000').save()

    # Create a course designer
    CourseDesigner('testcd1', '12345678', 'Test Course Designer 1', 'a100000001').save()


def populate_semester():
    # Create semesters from 2012 to 2022
    for year in [year for year in range(2005, 2023)]:
        for term in [1, 2]:
            Semester.get_semester(year, term)


def populate_degree():
    degrees = [
        'Bachelor of Business Administration (Honours) (Applied Economics)',
        'Bachelor of Business Administration (Honours) (Finance)',
        'Bachelor of Business Administration (Honours) (Accounting)',
        'Bachelor of Business Administration (Honours) (Management of Human Resources)',
        'Bachelor of Business Administration (Honours) (Marketing Management)',
        'Bachelor of Business Administration (Honours) (e-Business Management and Information Systems)',
        'Bachelor of Business Administration (Honours) (Entrepreneurship and Innovation)',
        'Bachelor of Business Administration (Honours) (Culture, Creativity and Management)',
        'Bachelor of Arts (Honours) in Cinema and Television',
        'Bachelor of Communication (Honours) in Media Arts and Design',
        'Bachelor of Arts (Honours) in Musical Arts',
        'Bachelor of Science (Honours) in Computer Science and Technology',
        'Bachelor of Science (Honours) in Environmental Science',
        'Bachelor of Science (Honours) in Statistics',
        'Bachelor of Science (Honours) in Food Science and Technology',
        'Bachelor of Science (Honours) in Applied Psychology',
        'Bachelor of Science (Honours) in Financial Mathematics',
        'Bachelor of Science (Honours) in Data Science',
        'Bachelor of Science (Honours) in Applied Mathematics',
        'Bachelor of Social Sciences (Honours) in Government and International Relations',
        'Bachelor of Arts (Honours) in International Journalism',
        'Bachelor of Arts (Honours) in Public Relations and Advertising',
        'Bachelor of Social Work and Social Administration (Honours)',
        'Bachelor of Arts (Honours) in Teaching English as a Second Language',
        'Bachelor of Arts (Honours) in Applied Translation Studies',
        'Bachelor of Arts (Honours) in Contemporary English Language and Literature',
        'Bachelor of Arts (Honours) in English Language and Literature Studies',
        'Bachelor of Communication (Honours) in Media and Communication Studies',
        'Bachelor of Social Sciences (Honours) in Globalisation and Development'
    ]
    for degree in degrees:
        program_degree = ProgramDegree(degree)
        save(program_degree)
    

def populate_type():
    course_types = [
        'Major Required (MR)',
        'Major Elective (ME)',
        'General Education Core (GEC)',
        'General Education Distribution (GED)',
        'Whole Person Education (WPE)'
        'Free Elective Courses (FE)'
    ]
    for course_type in course_types:
        type_obj = CourseType(course_type)
        save(type_obj)


def populate_course():
    courses = [
        Course(
            course_name='Linear Algebra', 
            course_code='MATH1003', 
            course_type_id=1,
            program_degree_id=12,
            since=[2008, 1], 
            ends=None),
        Course(
            course_name='Data Structures and Algorithms', 
            course_code='COMP2003', 
            course_type_id=1,
            program_degree_id=12,
            since=[2015, 1], 
            ends=None),
        Course(
            course_name='Object-Oriented Programming', 
            course_code='COMP2013', 
            course_type_id=1,
            program_degree_id=12,
            since=[2015, 1], 
            ends=None),
        Course(
            course_name='Operating Systems', 
            course_code='COMP3033', 
            course_type_id=2,
            program_degree_id=12,
            since=[2015, 1], 
            ends=None),
        Course(
            course_name='Software Testing', 
            course_code='COMP3123', 
            course_type_id=2,
            program_degree_id=12,
            since=[2015, 1], 
            ends=None),
        Course(
            course_name='Quantum Finance and Intelligent Financial Trading Systems', 
            course_code='COMP4153', 
            course_type_id=2,
            program_degree_id=12,
            since=[2018, 1], 
            ends=None),
    ]

    all_courses = []

    for idx, course in enumerate(courses):
        course.save()
        all_courses.append(course)

        if idx == 0:
            course.add_cilos([
                        {
                            "cilo_index": 0,
                            "cilo_description": "Perform basic calculations on a given matrix and find properties for that matrix.",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 1,
                            "cilo_description": "Identify relationship among different concepts of matrices and prove algebraic statements about them.",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 2,
                            "cilo_description": "Present basic ideas of matrix use as shown in the textbook or distributed materials.",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 3,
                            "cilo_description": "Analyse real problems and apply matrix theory to solve them.",
                            "depending_cilos": []
                        },
                    ])
            
        
        if idx == 3:
            course.add_cilos([
                        {
                            "cilo_index": 0,
                            "cilo_description": "Explain the conceptual framework of object-oriented programming.",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 1,
                            "cilo_description": "Programme in JAVA to enable the solution of non-elementary programming tasks.",
                            "depending_cilos": []
                        }
                    ])

        if idx == 4:
            course.add_cilos([
                        {
                            "cilo_index": 0,
                            "cilo_description": "Explain the basic principles of the operating system.",
                            "depending_cilos": [1]
                        },
                        {
                            "cilo_index": 1,
                            "cilo_description": "Implement operating systems concepts in detail.",
                            "depending_cilos": [5]
                        }
                    ])

        if idx == 5:
            course.add_cilos([
                        {
                            "cilo_index": 0,
                            "cilo_description": "explain the basic concepts of quantum finance and its underlying technologies;",
                            "depending_cilos": [1]
                        },
                        {
                            "cilo_index": 1,
                            "cilo_description": "incorrect cilo;",
                            "depending_cilos": []
                        },
                        {
                            "cilo_index": 2,
                            "cilo_description": "apply the quantum finance and intelligent trading methodologies, tools and codes to develop intelligent financial trading systems, individually and as a group.",
                            "depending_cilos": [1]
                        },
                    ])

            course.edit_cilos([
                        {
                            "id": 9,
                            "cilo_index": 0,
                            "cilo_description": "explain the basic concepts of quantum finance and its underlying technologies;"
                        },
                        {
                            "id": 10,
                            "cilo_index": 1,
                            "cilo_description": "formulate financial models and intelligent trading strategies from the quantum finance perspective"
                        },
                        {
                            "id": 11,
                            "cilo_index": 2,
                            "cilo_description": "apply the quantum finance and intelligent trading methodologies, tools and codes to develop intelligent financial trading systems, individually and as a group."
                        },
                    ])

    for idx, course in enumerate(courses):
        print('========== ' + str(idx + 1) + ' ==========')
        print(course.course_name)
        print(course.get_cilos())
        print(course.get_course_prerequisites())
        print(course.get_dependent_courses())


def save(obj):
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)


if __name__ == '__main__':
    main()