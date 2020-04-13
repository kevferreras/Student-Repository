'''The purpose of this file is to test multiple classes'''

from Student_Repository_Kevin_Ferreras import Student, Instructor, Repository
from HW08_Kevin_Ferreras import file_reader
from typing import Dict, List, Tuple, Any, Set
import unittest
import os
import sqlite3

DB_FILE: str = r'C:\Users\Kevin\Documents\SSW810 - Software Dev Tools & Techniques\student_repository_database.sqlite'
 

class RepositoryTest(unittest.TestCase):
    '''To test Repository class'''

    directory: str = input(f'Please enter a test directory to test all_students_summary and all_instructors_summary: ')

    def test_Students_attributes(self) -> None:
        '''Tests that the correct information for a student is stored in the student repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)
        
        expected: Dict[str, Student] = {

                '10103': ('10103', 'Jobs, S', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], '3.38'),
                '10115': ('10115', 'Bezos, J', ['CS 546', 'SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], '2.00'),
                '10183': ('10183', 'Musk, E', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], '4.00'), 
                '11714': ('11714', 'Gates, B', ['CS 546', 'CS 570', 'SSW 810'], [], [], '3.50'),
                             
            }

        calculated: Dict[str, Tuple[Any]] = {cwid: student.student_summary_row() for cwid, student in school_repository._student_repository.items()}
        
        self.assertEqual(expected, calculated)

    def test_Instructors_attributes (self) -> None:
        '''Test that the correct information for an istructor is stored in the instructor repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)

        expected: Set[Tuple[Any]] = {

            ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
            ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
            ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), 
            ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
            ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
            ('98762', 'Hawking, S', 'CS', 'CS 570', 1),

            }

        calculated: Set[Tuple[Any]] = {tuple(detail) for instructor in school_repository._instructor_repository.values() for detail in instructor.instructor_summary_row()}

        self.assertEqual(expected, calculated)

    def test_majors_attribute(self) -> None:
        '''Test that the correct information for a major is stored in the majors repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)

        expected: DefaultDict[str, Defaultdict[str, List[str]]] = {


            'SFEN': {'R': ['SSW 540', 'SSW 810', 'SSW 555'], 'E': ['CS 501', 'CS 546']},
            'CS': {'R': ['CS 570', 'CS 546'], 'E': ['SSW 810', 'SSW 565']},

        }


        self.assertEqual(expected, school_repository._majors_repository)

    def test_student_grades_table_db(self) -> None:
        '''Tests that the correct data is retrieved from the student repository database'''


        expected: Set[Tuple[str]] = {

                ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),

        }

        db: sqlite3.Connection = sqlite3.connect(DB_FILE)
        query: str = '''select students.Name, students.CWID, grades.Course, grades.Grade, instructors.Name
                        from students join grades on students.CWID = grades.StudentCWID
                        join instructors on grades.InstructorCWID = instructors.CWID order by students.Name ASC;'''
        
        calculated: Set[Tuple[str]] = {tuple(row) for row in db.execute(query)}

        self.assertEqual(expected, calculated)

        db.close()


if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 2)
