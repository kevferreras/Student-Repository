'''The purpose of this file is to test multiple classes'''

from HW09_Kevin_Ferreras import Student, Instructor, Repository
from HW08_Kevin_Ferreras import file_reader
from typing import Dict, List
import unittest
import os

class StudentTest(unittest.TestCase):
    '''To test Student class'''

    def test_add_student(self) -> None:
        '''Tests that the method correctly adds a new student's detail: CWID,
            Name, Major to the student_detail dictionary'''
        
        student_class: Student = Student()
        student_cwid: int = 12345
        student_class.add_student(student_cwid, 'Smith, J', 'Comp Sci')

        expected_dictionary: Dict[int, Dict[str, str]] = {

                12345 : {'Name':'Smith, J', 'Major':'Comp Sci'}
        }

        self.assertEqual(student_class.student_detail, expected_dictionary)
        
    def test_add_student_detail(self) -> None:
        '''Tests that the method adds additional student detail that is 
            associated with the student's CWID'''

        student_class: Student = Student()
        student_cwid: int = 12345

        student_class.add_student(student_cwid, 'Smith, J', 'Comp Sci')
        student_class.add_student_detail(student_cwid, 'Email', 'SmithJ@school.com')

        expected_dictionary: Dict[int, Dict[str, str]] = {

                12345 : {'Name':'Smith, J', 'Major':'Comp Sci', 'Email':'SmithJ@school.com'}
        }

        self.assertEqual(student_class.student_detail, expected_dictionary)
        
    def test_change_student_detail(self) -> None:
        '''Tests that the method changes a students detail associated 
            with her/his CWID'''

        student_class: Student = Student()
        student_cwid: int = 12345
        
        student_class.add_student(student_cwid, 'Smith, J', 'Comp Sci')
        expected_dictionary: Dict[int, Dict[str, str]] = {

                12345 : {'Name':'Smith, J', 'Major':'Comp Sci'}
        }

        self.assertEqual(student_class.student_detail, expected_dictionary)

        student_class.change_student_detail(student_cwid, 'Major', 'Math')
        expected_dictionary_after_change: Dict[int, Dict[str, str]] = {

                12345 : {'Name':'Smith, J', 'Major':'Math'}
        }

        self.assertEqual(student_class.student_detail, expected_dictionary_after_change)

    def test_change_student_detail_error(self) -> None:
        '''Test that the method raises a ValuError when a detail that
            does not exist is entered'''

        student_class: Student = Student()
        student_cwid: int = 12345
        
        student_class.add_student(student_cwid, 'Smith, J', 'Comp Sci')

        with self.assertRaises(ValueError):
            student_class.change_student_detail(student_cwid, 'Minor', 'Psychology')

    def test_add_completed_course(self) -> None:
        '''Tests that the method adds the completed course name and grade'''

        student_class: Student = Student()
        student_cwid: int = 12345
        course_completed: str = 'Software 101'
        course_grade: str = 'A'

        student_class.add_completed_course(student_cwid, course_completed, course_grade)
        expected_dictionary: Dict[int, Dict[str, str]] = {

                12345: {'SOFTWARE 101':'A'}
        
        }

        self.assertEqual(student_class.completed_courses, expected_dictionary)

    def test_student_summary(self) -> None:
        '''Test that the two dictionaries (student_detail & completed_courses) in class Student hold the expected
            data, in order to generate a prettytable summary for a single student'''

        student_class: Student = Student()
        student_cwid: int = 12345

        student_class.add_student(student_cwid, 'Smith, J', 'Comp Sci')
        student_class.add_completed_course(student_cwid, 'Software 101', 'A')
        student_class.add_completed_course(student_cwid, 'Comp Sci 101', 'A')
        student_class.add_completed_course(student_cwid, 'Programming 101', 'A')

        expected_student_detail_dictionary: Dict[int, Dict[str, str]] = {

                12345 : {'Name':'Smith, J', 'Major':'Comp Sci'}
        }

        expected_completed_courses_dictionary: Dict[int, Dict[str, str]] = {

                12345 : {'COMP SCI 101':'A', 
                        'PROGRAMMING 101':'A', 
                        'SOFTWARE 101':'A',}
        
        }          
        
        self.assertEqual(student_class.student_detail, expected_student_detail_dictionary)
        self.assertEqual(student_class.completed_courses, expected_completed_courses_dictionary)


class InstructorTest(unittest.TestCase):
    '''To test Instructor class'''

    def test_add_instructor(self) -> None:
        '''Tests that the method correctly adds a new instructor's detail: CWID,
            Name, Dept to the instructor_detail dictionary'''
        
        instructor_class: Instructor = Instructor()
        instructor_cwid: int = 98765 
        instructor_class.add_instructor(instructor_cwid, 'Professor, R', 'Software')

        expected_dictionary: Dict[int, Dict[str, str]] = {

                98765 : {'Name':'Professor, R', 'Dept':'Software'}
        }

        self.assertEqual(instructor_class.instructor_detail, expected_dictionary)

    def test_add_instructor_detail(self) -> None:
        '''Test that the method adds additional detail that is associated 
            with the instructor CWID'''

        instructor_class: Instructor = Instructor()
        instructor_cwid: int = 98765 
        
        instructor_class.add_instructor(instructor_cwid, 'Professor, R', 'Software')
        instructor_class.add_instructor_detail(instructor_cwid, 'Email', 'ProfessorR@school.com')

        expected_dictionary: Dict[int, Dict[str, str]] = {

                98765 : {'Name':'Professor, R', 'Dept':'Software', 'Email':'ProfessorR@school.com'}
        }

        self.assertEqual(instructor_class.instructor_detail, expected_dictionary)

    def test_change_instructor_detail(self) -> None:
        '''Tests that the method changes an instructor's detail associated 
            with her/his CWID'''

        instructor_class: Instructor = Instructor() 
        instructor_cwid: int = 98765
        
        instructor_class.add_instructor(instructor_cwid, 'Professor, R', 'Software')
        expected_dictionary: Dict[int, Dict[str, str]] = {

                98765 : {'Name':'Professor, R', 'Dept':'Software'}
        }

        self.assertEqual(instructor_class.instructor_detail, expected_dictionary)

        instructor_class.change_instructor_detail(instructor_cwid, 'Dept', 'Systems')
        expected_dictionary_after_change: Dict[int, Dict[str, str]] = {

                98765 : {'Name':'Professor, R', 'Dept':'Systems'}
        }

        self.assertEqual(instructor_class.instructor_detail, expected_dictionary_after_change)
       
    def test_change_instructor_detail_error(self) -> None:
        '''Test that the method raises a ValuError when a detail that
            does not exist is entered'''
        
        instructor_class: Instructor = Instructor() 
        instructor_cwid: int = 98765
        
        instructor_class.add_instructor(instructor_cwid, 'Professor, R', 'Software')

        with self.assertRaises(ValueError):
            instructor_class.change_instructor_detail(instructor_cwid, 'Minor', 'Comp Sci')
        
    def test_add_course_taught(self) -> None:
        '''Tests that the method adds a course that has been taught by the
            instructor and the number of students in the course'''

        instructor_class: Instructor = Instructor() 
        instructor_cwid: int = 98765
        course_taught: str = 'Software 101'

        instructor_class.add_course_taught(instructor_cwid, course_taught)
        expected_dictionary: Dict[int, Dict[str, int]] = {

                98765: {'Software 101': 1}

        }

        self.assertEqual(instructor_class.courses_taught, expected_dictionary)

    def test_instructor_summary(self) -> None:
        '''Test that the two dictionaries (instructor_detail & courses_taught) in class Instructor hold the expected
            data, in order to generate a prettytable summary for a single instructor'''

        instructor_class: Instructor = Instructor() 
        instructor_cwid: int = 98765

        instructor_class.add_instructor(instructor_cwid, 'Professor, R', 'Software')
        instructor_class.add_course_taught(instructor_cwid, 'Software 101')
        instructor_class.add_course_taught(instructor_cwid, 'Cyber 101')

        expected_instructor_detail_dictionary: Dict[int, Dict[str, str]] = {

                98765 : {'Name':'Professor, R', 'Dept':'Software'}
        }  

        expected_courses_taught_dictionary: Dict[int, Dict[str, int]] = {

                98765 : {'Software 101': 1, 'Cyber 101': 1}
        }  

        self.assertEqual(instructor_class.instructor_detail, expected_instructor_detail_dictionary)
        self.assertEqual(instructor_class.courses_taught, expected_courses_taught_dictionary)


class RepositoryTest(unittest.TestCase):
    '''To test Repository class'''

    directory: str = input(f'Please enter a test directory to test all_students_summary and all_instructors_summary: ')

    def test_all_students_summary(self) -> None:
        '''Test that this class correctly updates the student_repository with the expected
            data, in order to generate a prettytable summary for all students'''

        school_repository: Repository = Repository(RepositoryTest.directory)
        
        expected_student_repository: Dict[str, Dict[str, Any]] = {

                '10103': {'Name': 'Baldwin, C', 'Major': 'SFEN', 'Completed Courses': {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'}},
                '10115': {'Name': 'Wyatt, X', 'Major': 'SFEN', 'Completed Courses': {'SSW 567': 'A', 'SSW 564': 'B+', 'SSW 687': 'A', 'CS 545': 'A'}},
                '10172': {'Name': 'Forbes, I', 'Major': 'SFEN', 'Completed Courses': {'SSW 555': 'A', 'SSW 567': 'A-'}},
                '10175': {'Name': 'Erickson, D', 'Major': 'SFEN', 'Completed Courses': {'SSW 567': 'A', 'SSW 564': 'A', 'SSW 687': 'B-'}},
                '10183': {'Name': 'Chapman, O', 'Major': 'SFEN', 'Completed Courses': {'SSW 689': 'A'}},
                '11399': {'Name': 'Cordova, I', 'Major': 'SYEN', 'Completed Courses': {'SSW 540': 'B'}},
                '11461': {'Name': 'Wright, U', 'Major': 'SYEN', 'Completed Courses': {'SYS 800': 'A', 'SYS 750': 'A-', 'SYS 611': 'A'}},
                '11658': {'Name': 'Kelly, P', 'Major': 'SYEN', 'Completed Courses': {'SSW 540': 'F'}},
                '11714': {'Name': 'Morton, A', 'Major': 'SYEN', 'Completed Courses': {'SYS 611': 'A', 'SYS 645': 'C'}},
                '11788': {'Name': 'Fuller, E', 'Major': 'SYEN', 'Completed Courses': {'SSW 540': 'A'}},
                             
            }

        self.assertEqual(school_repository.student_repository, expected_student_repository)

    def test_all_instructors_summary(self) -> None:
        '''Test that this class correctly updates the instructor_repository and instructor_courses_taught with the expected
            data, in order to generate a prettytable summary for all instructors'''

        school_repository: Repository = Repository(RepositoryTest.directory)

        expected_instructor_repository: Dict[str, Dict[str, str]] = {

            '98765' : {'Name': 'Einstein, A', 'Dept': 'SFEN'},
            '98764' : {'Name': 'Feynman, R', 'Dept': 'SFEN'},
            '98763' : {'Name': 'Newton, I', 'Dept': 'SFEN'},
            '98762' : {'Name': 'Hawking, S', 'Dept': 'SYEN'},
            '98761' : {'Name': 'Edison, A', 'Dept': 'SYEN'},
            '98760' : {'Name': 'Darwin, C', 'Dept': 'SYEN'},

            }

        expected_instructor_courses_taught_repository: Dict[str, Dict[str, int]] = {

            '98765' : {'SSW 567': 4, 'SSW 540': 3},
            '98764' : {'SSW 564': 3, 'SSW 687': 3, 'CS 501': 1, 'CS 545': 1},
            '98763' : {'SSW 555': 1, 'SSW 689': 1},
            '98760' : {'SYS 800': 1, 'SYS 750': 1, 'SYS 611': 2, 'SYS 645': 1},


            }


        self.assertEqual(school_repository.instructor_repository, expected_instructor_repository)
        self.assertEqual(school_repository.instructor_courses_taught_repository, expected_instructor_courses_taught_repository)




if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 2)
