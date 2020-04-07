'''The purpose of this file is to test multiple classes'''

from Student_Repository_Kevin_Ferreras import Student, Instructor, Repository
from HW08_Kevin_Ferreras import file_reader
from typing import Dict, List, Tuple, Any
import unittest
import os
 

class RepositoryTest(unittest.TestCase):
    '''To test Repository class'''

    directory: str = input(f'Please enter a test directory to test all_students_summary and all_instructors_summary: ')

    def test_Students_attributes(self) -> None:
        '''Tests that the correct information for a student is stored in the student repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)
        
        expected: Dict[str, Student] = {

                '10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 513', 'CS 545'], '3.44'),
                '10115': ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513'], '3.81'),
                '10172': ('10172', 'Forbes, I', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], '3.88'),
                '10175': ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], '3.58'),
                '10183': ('10183', 'Chapman, O',['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], '4.00'), 
                '11399': ('11399', 'Cordova, I', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 565', 'SSW 810'], '3.00'), 
                '11461': ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.92'), 
                '11658': ('11658', 'Kelly, P', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], '0.00'),
                '11714': ('11714', 'Morton, A', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.00'),
                '11788': ('11788', 'Fuller, E', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 565', 'SSW 810'], '4.00'),
                             
            }

        calculated: Dict[str, Tuple[Any]] = {cwid: student.student_summary_row() for cwid, student in school_repository._student_repository.items()}
        
        self.assertEqual(expected, calculated)

    def test_Instructors_attributes (self) -> None:
        '''Test that the correct information for an istructor is stored in the instructor repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)

        expected: Set[Tuple[Any]] = {

            ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
            ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
            ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
            ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
            ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
            ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
            ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
            ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),            
            ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1),

            }

        calculated: Tuple[Any] = {tuple(detail) for instructor in school_repository._instructor_repository.values() for detail in instructor.instructor_summary_row()}

        self.assertEqual(expected, calculated)

    def test_majors_attribute(self) -> None:
        '''Test that the correct information for a major is stored in the majors repository'''

        school_repository: Repository = Repository(RepositoryTest.directory)

        expected: DefaultDict[str, Defaultdict[str, List[str]]] = {


            'SFEN': {'Required Courses': ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], 'Electives': ['CS 501', 'CS 513', 'CS 545']},
            'SYEN': {'Required Courses': ['SYS 671', 'SYS 612', 'SYS 800'], 'Electives': ['SSW 810', 'SSW 565', 'SSW 540']},

        }


        self.assertEqual(expected, school_repository._majors_repository)


if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 2)
