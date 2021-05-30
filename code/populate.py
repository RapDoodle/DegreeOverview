from core.db import db
from core.startup import create_app

from models.student import Student
from models.lecturer import Lecturer
from models.course_designer import CourseDesigner
from models.semester import Semester
from models.degree import Degree
from models.course_type import CourseType
from models.course import Course
from models.program import Program
from models.course_version import CourseVersion
from models.report import Report
from models.student_report import StudentReport
from models.grade_item import GradeItem


def main():
    app = create_app(name=__name__, config_name='dev')
    with app.app_context():
        db.drop_all()
        db.create_all()

        populate_user()
        populate_semester()
        populate_program()
        populate_degree()
        populate_type()
        populate_course()
        populate_report()


def populate_user():
    # Create a student
    Student('teststudent1', '12345678', 'Test Student 1', 'n830026001').save(commit=True)
    Student('teststudent2', '12345678', 'Test Student 2', 'n830026002').save(commit=True)
    Student('teststudent3', '12345678', 'Test Student 3', 'n830026003').save(commit=True)
    Student('teststudent4', '12345678', 'Test Student 4', 'n830026004').save(commit=True)
    Student('teststudent5', '12345678', 'Test Student 5', 'n830026005').save(commit=True)
    Student('teststudent6', '12345678', 'Test Student 6', 'n830026006').save(commit=True)
    Student('teststudent7', '12345678', 'Test Student 7', 'n830026007').save(commit=True)
    Student('teststudent8', '12345678', 'Test Student 8', 'n830026008').save(commit=True)
    Student('teststudent9', '12345678', 'Test Student 9', 'n830026009').save(commit=True)
    Student('teststudent10', '12345678', 'Test Student 10', 'n8300260010').save(commit=True)
    Student('teststudent11', '12345678', 'Test Student 11', 'n8300260011').save(commit=True)
    Student('teststudent12', '12345678', 'Test Student 12', 'n8300260012').save(commit=True)
    Student('teststudent13', '12345678', 'Test Student 13', 'n8300260013').save(commit=True)
    Student('teststudent14', '12345678', 'Test Student 14', 'n8300260014').save(commit=True)
    Student('teststudent15', '12345678', 'Test Student 15', 'n8300260015').save(commit=True)
    Student('teststudent16', '12345678', 'Test Student 16', 'n8300260016').save(commit=True)

    # Create a lecturer (lecturer)
    Lecturer('testlecturer1', '12345678', 'Test Lecturer 1', 'a100000000').save(commit=True)

    # Create a course designer
    CourseDesigner('testcd1', '12345678', 'Test Course Designer 1', 'a100000001').save(commit=True)


def populate_semester():
    # Create semesters from 2012 to 2022
    for year in [year for year in range(2005, 2023)]:
        for term in [1, 2]:
            Semester.get_semester(year, term)

def populate_program():
    programs = [
        'Accounting Programme',
        'Applied Economics Programme',
        'e-Business Management and Information Systems Programme',
        'Entrepreneurship and Innovation Programme',
        'Finance Programme',
        'Management of Human Resources Programme',
        'Marketing Management Programme',
        'Cinema and Television Programme',
        'Culture, Creativity and Management Programme',
        'Media Arts and Design Programme',
        'Musical Arts Programme',
        'Applied Translation Studies Programme',
        'English Language and Literature Studies Programme',
        'Globalisation and Development Programme',
        'Media and Communication Studies Programme',
        'Public Relations and Advertising Programme',
        'Social Work and Social Administration Programme',
        'Applied Mathematics Programme',
        'Applied Psychology Programme',
        'Computer Science and Technology Programme',
        'Data Science Programme',
        'Environmental Science Programme',
        'Financial Mathematics Programme',
        'Food Science and Technology Programme',
        'Statistics Programme',
        'Whole Person Education',
        'General Education',
        'Chinese Language and Culture Centre',
        'English Language Centre',
        'Continuing Education'
    ]
    for program_name in programs:
        program = Program(program_name)
        save(program)

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
    related_programs = [
        2, 5, 1, 6, 7,
        3, 4, 9, 8, 10,
        11, 20, 22, 25, 24,
        19, 23, 21, 18, 15,
        15, 16, 17, 13, 12,
        13, 13, 15, 14

    ]
    for idx, degree in enumerate(degrees):
        degree_obj = Degree(degree, related_programs[idx])
        save(degree_obj)


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
        {
            "course_name": "Speaking of Statistics",
            "course_code": "GCNU1003",
            "course_type_id": 3,
            "program_id": 27,
            "effective_since": 2012,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Manipulate the tool of statistics for exploring quantitative relationships",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Apply statistics to identify, model and solve relevant problems in our society",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "Explain the interrelationships between everyday phenomena and statistics",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Quizzes",
                    "weight": 10,
                    "cilos_addressed": [1]
                },
                {
                    "method_index": 2,
                    "method_name": "Assignments",
                    "weight": 20,
                    "cilos_addressed": [2, 3]
                },
                {
                    "method_index": 3,
                    "method_name": "Group projects",
                    "weight": 20,
                    "cilos_addressed": [2, 3]
                },
                {
                    "method_index": 4,
                    "method_name": "Mid-term test",
                    "weight": 10,
                    "cilos_addressed": [1, 2, 3]
                },
                {
                    "method_index": 5,
                    "method_name": "Final examination",
                    "weight": 40,
                    "cilos_addressed": [2, 3]
                }
            ]
        },
        {
            "course_name": "Structured Programming",
            "course_code": "COMP1003",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2019,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Explain the basic principles of structured programming;",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Use a structured programming language and apply structured programming principles to develop medium-scale program individually and as a team ",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Assignments / Quizzes",
                    "weight": 15,
                    "cilos_addressed": [1]
                },
                {
                    "method_index": 2,
                    "method_name": "Labs",
                    "weight": 25,
                    "cilos_addressed": [2]
                },
                {
                    "method_index": 3,
                    "method_name": "Projects",
                    "weight": 10,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 4,
                    "method_name": "Examination",
                    "weight": 50,
                    "cilos_addressed": [1, 2]
                }
            ]
        },
        {
            "course_name": "Data Structures and Algorithms",
            "course_code": "COMP2003",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2016,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Describe abstract data types such as heaps, trees and graphs",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Implement abstract data types such as heaps, trees and graphs using C++",
                    "depending_cilos": [5]
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "Design efficient algorithm using appropriate data structures to basic problems such as sorting and searching",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 4,
                    "cilo_description": "Evaluate the complexity of algorithms",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Written Assignments",
                    "weight": 15,
                    "cilos_addressed": [1, 4]
                },
                {
                    "method_index": 2,
                    "method_name": "Programming Assignments",
                    "weight": 15,
                    "cilos_addressed": [1, 2, 3]
                },
                {
                    "method_index": 3,
                    "method_name": "Midterm Test",
                    "weight": 30,
                    "cilos_addressed": [1, 4]
                },
                {
                    "method_index": 4,
                    "method_name": "Final Examination",
                    "weight": 40,
                    "cilos_addressed": [1, 3, 4]
                }
            ]
        },
        {
            "course_name": "Database Management Systems",
            "course_code": "COMP3013",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2016,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "write relational algebra and SQL queries to retrieve information from a database proficiently;",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "design a relational database management system;",
                    "depending_cilos": [5]
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "write discipline-related documents for a project to be presented; and",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 4,
                    "cilo_description": "collaborate in a team.",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Assignment",
                    "weight": 10,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 2,
                    "method_name": "Midterm Examination",
                    "weight": 20,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 3,
                    "method_name": "Group Project",
                    "weight": 30,
                    "cilos_addressed": [1, 2, 3, 4]
                },
                {
                    "method_index": 4,
                    "method_name": "Final Examination",
                    "weight": 40,
                    "cilos_addressed": [1, 2]
                }
            ]
        },
        {
            "course_name": "Linear Algebra",
            "course_code": "MATH1003",
            "course_type_id": 1,
            "program_id": 27,
            "effective_since": 2016,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Perform basic calculations on a given matrix and find properties for that matrix.",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Identify relationship among different concepts of matrices and prove algebraic statements about them.",
                    "depending_cilos": [5]
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "Present basic ideas of matrix use as shown in the textbook or distributed materials. ",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 4,
                    "cilo_description": "Analyse real problems and apply matrix theory to solve them.",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Assignment",
                    "weight": 15,
                    "cilos_addressed": [1, 2, 3, 4]
                },
                {
                    "method_index": 2,
                    "method_name": "Class exercises",
                    "weight": 5,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 3,
                    "method_name": "Quiz",
                    "weight": 20,
                    "cilos_addressed": [1, 2, 3]
                },
                {
                    "method_index": 4,
                    "method_name": "Final Examination",
                    "weight": 60,
                    "cilos_addressed": [1, 2, 3, 4]
                }
            ]
        },
        {
            "course_name": "Computer Graphics",
            "course_code": "COMP4033",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2016,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Explain the underlying concepts and write representations of different algorithms of computer graphics.",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Apply fundamental techniques in computer graphics using OpenGL API or Java.",
                    "depending_cilos": [5, 8, 14]
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "Present basic ideas of matrix use as shown in the textbook or distributed materials. ",
                    "depending_cilos": [8]
                },
                {
                    "cilo_index": 4,
                    "cilo_description": "Analyse real problems and apply matrix theory to solve them.",
                    "depending_cilos": []
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Assignment",
                    "weight": 15,
                    "cilos_addressed": [1, 2, 3, 4]
                },
                {
                    "method_index": 2,
                    "method_name": "Class exercises",
                    "weight": 5,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 3,
                    "method_name": "Quiz",
                    "weight": 20,
                    "cilos_addressed": [1, 2, 3]
                },
                {
                    "method_index": 4,
                    "method_name": "Final Examination",
                    "weight": 60,
                    "cilos_addressed": [1, 2, 3, 4]
                }
            ]
        },
        {
            "course_name": "Operating Systems",
            "course_code": "COMP3033",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2020,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Explain the basic principles of the operating system.",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Implement operating systems concepts in detail.",
                    "depending_cilos": [5]
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Hands-on Exercise",
                    "weight": 10,
                    "cilos_addressed": [1]
                },
                {
                    "method_index": 2,
                    "method_name": "Programming Assignment",
                    "weight": 20,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 3,
                    "method_name": "Project",
                    "weight": 10,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 4,
                    "method_name": "Quiz",
                    "weight": 10,
                    "cilos_addressed": [1]
                },
                {
                    "method_index": 5,
                    "method_name": "Final examination",
                    "weight": 50,
                    "cilos_addressed": [1, 2]
                }
            ]
        },
        {
            "course_name": "Design and Analysis of Algorithms",
            "course_code": "COMP3023",
            "course_type_id": 1,
            "program_id": 20,
            "effective_since": 2020,
            "cilos": [
                {
                    "cilo_index": 1,
                    "cilo_description": "Describe problem solving techniques, such as dynamic programming and greedy, and their representative algorithms",
                    "depending_cilos": []
                },
                {
                    "cilo_index": 2,
                    "cilo_description": "Design algorithms to common problems using the techniques introduced.",
                    "depending_cilos": [7]
                },
                {
                    "cilo_index": 3,
                    "cilo_description": "Evaluate the correctness of algorithms and their efficiency.",
                    "depending_cilos": [9]
                }
            ],
            "assessment_methods": [
                {
                    "method_index": 1,
                    "method_name": "Written Assignment",
                    "weight": 15,
                    "cilos_addressed": [1, 3]
                },
                {
                    "method_index": 2,
                    "method_name": "Programming Assignment",
                    "weight": 15,
                    "cilos_addressed": [1, 2]
                },
                {
                    "method_index": 3,
                    "method_name": "Quizzes",
                    "weight": 30,
                    "cilos_addressed": [1, 3]
                },
                {
                    "method_index": 4,
                    "method_name": "Final Examination",
                    "weight": 40,
                    "cilos_addressed": [1, 2, 3]
                }
            ]
        },
    ]

    for content in courses:
        Course.add_course(content)
        
    db.session.commit()
    

def populate_report():
    # Grade for Structured Programming
    report_obj_1 = Report(
        course_id=2, 
        semester_id=24)
    save(report_obj_1)
    report_obj_2 = Report(
        course_id=2, 
        semester_id=25)
    save(report_obj_2)
    report_obj_3 = Report(
        course_id=2, 
        semester_id=26)
    save(report_obj_3)

    # For course 3
    report_obj_4 = Report(
        course_id=3, 
        semester_id=26)
    save(report_obj_4)

    student_grade_obj_1 = StudentReport(
        report_id=report_obj_1.id, 
        student_id=1)
    save(student_grade_obj_1)
    student_grade_obj_2 = StudentReport(
        report_id=report_obj_1.id, 
        student_id=2)
    save(student_grade_obj_2)
    student_grade_obj_3 = StudentReport(
        report_id=report_obj_1.id, 
        student_id=3)
    save(student_grade_obj_3)
    student_grade_obj_4 = StudentReport(
        report_id=report_obj_2.id, 
        student_id=4)
    save(student_grade_obj_4)
    student_grade_obj_5 = StudentReport(
        report_id=report_obj_2.id, 
        student_id=5)
    save(student_grade_obj_5)
    student_grade_obj_6 = StudentReport(
        report_id=report_obj_2.id, 
        student_id=6)
    save(student_grade_obj_6)
    student_grade_obj_7 = StudentReport(
        report_id=report_obj_3.id, 
        student_id=7)
    save(student_grade_obj_7)

    student_grade_obj_8 = StudentReport(
        report_id=report_obj_4.id, 
        student_id=1)
    save(student_grade_obj_8)

    grade_items = [
        [student_grade_obj_1.id, 6, 14.71, False],
        [student_grade_obj_1.id, 7, 23.50, False],
        [student_grade_obj_1.id, 8, 9.63, False],
        [student_grade_obj_1.id, 9, 49.75, False],

        [student_grade_obj_2.id, 6, 14.13, False],
        [student_grade_obj_2.id, 7, 23.88, False],
        [student_grade_obj_2.id, 8, 9.63, False],
        [student_grade_obj_2.id, 9, 47.00, False],

        [student_grade_obj_3.id, 6, 14.10, False],
        [student_grade_obj_3.id, 7, 22.19, False],
        [student_grade_obj_3.id, 8, 8.88, False],
        [student_grade_obj_3.id, 9, 48.75, False],

        [student_grade_obj_4.id, 6, 12.58, False],
        [student_grade_obj_4.id, 7, 23.73, False],
        [student_grade_obj_4.id, 8, 8.88, False],
        [student_grade_obj_4.id, 9, 45.75, False],

        [student_grade_obj_5.id, 6, 13.35, False],
        [student_grade_obj_5.id, 7, 22.32, False],
        [student_grade_obj_5.id, 8, 10.00, False],
        [student_grade_obj_5.id, 9, 44.00, False],

        [student_grade_obj_6.id, 6, 12.96, False],
        [student_grade_obj_6.id, 7, 24.55, False],
        [student_grade_obj_6.id, 8, 10.00, False],
        [student_grade_obj_6.id, 9, 41.00, False],

        [student_grade_obj_7.id, 6, 13.22, False],
        [student_grade_obj_7.id, 7, 22.41, False],
        [student_grade_obj_7.id, 8, 8.88, False],
        [student_grade_obj_7.id, 9, 43.75, False],

        [student_grade_obj_8.id, 10, 86, True],
        [student_grade_obj_8.id, 11, 72, True],
        [student_grade_obj_8.id, 12, 90, True],
        [student_grade_obj_8.id, 13, 85, True],
    ]

    for item in grade_items:
        grade_item_obj = GradeItem(
            student_report_id=item[0], 
            assessment_method_id=item[1],
            score=item[2],
            use_percentage=item[3])
        save(grade_item_obj)

def save(obj):
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)


if __name__ == '__main__':
    main()