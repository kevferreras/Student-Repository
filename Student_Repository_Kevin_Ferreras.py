'''The purpose of this file is to implement multiple classes and functions'''

from HW08_Kevin_Ferreras import file_reader
from typing import List, Dict, DefaultDict, IO, Any
from collections import defaultdict
from prettytable import PrettyTable
import os

class Student:
    '''Student Class'''

    def __init__(self) -> None:
        '''To set a container for student detail and for completed courses'''

        self.student_detail: Dict[int, Dict[str, str]] = dict()
        self.completed_courses: DefaultDict[int, Dict[str, str]] = defaultdict(dict)
    
    def add_student(self, cwid: int, name: str, major: str) -> None:
        '''Adds new student standard detail (CWID, Name, Major) to the student_detail container'''

        self.student_detail[cwid] = {'Name': name, 'Major': major}

    def add_student_detail(self, cwid: int, detail_name: str, detail: str) -> None:
        '''Adds additional detail that is associated with the student CWID (i.e. email address)'''

        self.student_detail[cwid][detail_name] = detail
    
    def change_student_detail(self, cwid: int, detail_name: str, new_detail: str) -> None:
        '''Changes student detail associated with her/his CWID'''

        if detail_name in self.student_detail[cwid]:
            self.student_detail[cwid][detail_name] = new_detail
        else:
            raise ValueError('The detail you are trying to change does not exist. Please add the detail first.')

    def add_completed_course(self, cwid: int, course_name: str, grade: str) -> None:
        '''Adds a completed course and its grade'''

        self.completed_courses[cwid]
        self.completed_courses[cwid][course_name.upper()] = grade.upper()

    def student_summary(self, cwid: int) -> PrettyTable: 
        '''Generates a prettytable summary about a single student'''

        student_pretty_table: PrettyTable = PrettyTable(field_names = ['CWID', 'Name', 'Completed Courses'])

        completed_course_list: List[str] = list()

        for course in self.completed_courses[cwid].keys():
            completed_course_list.append(course)

        student_pretty_table.add_row([cwid, self.student_detail[cwid]['Name'], sorted(completed_course_list)])

        return student_pretty_table


class Instructor:
    '''Instructor Class'''

    def __init__(self) -> None:
        '''To set a container for instructor detail and for courses taught'''

        self.instructor_detail: Dict[int, Dict[str, str]] = dict()
        self.courses_taught: DefaultDict[int, DefaultDict[str, int]] = defaultdict(lambda: defaultdict(int))

    def add_instructor(self, cwid: int, name: str, dept: str) -> None:
        '''Adds new instructor standard detail (CWID, Name, Dept) to the instructor_detail container'''

        self.instructor_detail[cwid] = {'Name': name, 'Dept': dept}

    def add_instructor_detail(self, cwid: int, detail_name: str, detail: str) -> None:
        '''Adds additional detail that is associated with the instructor CWID (i.e. email address)'''

        self.instructor_detail[cwid][detail_name] = detail
    
    def change_instructor_detail(self, cwid: int, detail_name: str, new_detail: str) -> None:
        '''Changes instructor detail asociated with her/his CWID'''

        if detail_name in self.instructor_detail[cwid]:
            self.instructor_detail[cwid][detail_name] = new_detail
        else:
            raise ValueError('The detail you are trying to change does not exist. Please add the detail first.')

    def add_course_taught(self, cwid: int, course_name: str) -> None:
        '''Adds a course that has been taught by the instructor and the number of students in the course'''

        self.courses_taught[cwid][course_name] += 1

    def instructor_summary(self, cwid: int) -> PrettyTable:
        '''Generates a prettytable summary about a single instructor'''

        instructor_pretty_table: PrettyTable = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for course, students in self.courses_taught[cwid].items():
            instructor_pretty_table.add_row([cwid, self.instructor_detail[cwid]['Name'], self.instructor_detail[cwid]['Dept'], course, students])

        return instructor_pretty_table


class Repository:
    '''Repository Class'''

    def __init__(self, target_directory: str) -> None:
        '''Sets the directory in which the necessary data files are stored'''

        os.chdir(target_directory)
        self.student_class: Student = Student()
        self.instructor_class: Instructor = Instructor()

        self.student_repository: DefaultDict[int, DefaultDict[str, Any]] = defaultdict(lambda: defaultdict(dict))
        self.instructor_repository: DefaultDict[int, DefaultDict[str, int]] = defaultdict(lambda: defaultdict(dict))
        self.instructor_courses_taught_repository: DefaultDict[int, DefaultDict[str, int]] = defaultdict(lambda: defaultdict(int))

        #read students file:
        student_file_path: str = os.path.join(target_directory, 'students.txt')

        for cwid, name, major in file_reader(student_file_path, 3, '\t'):
            self.student_class.add_student(cwid, name, major)
            self.student_repository[cwid]
            self.student_repository[cwid]['Name'] = name
            self.student_repository[cwid]['Major'] = major

        #reads instructor file:
        instructor_file_path: str = os.path.join(target_directory, 'instructors.txt')

        for cwid, name, dept in file_reader(instructor_file_path, 3, '\t'):
            self.instructor_class.add_instructor(cwid, name, dept)
            self.instructor_repository[cwid]
            self.instructor_repository[cwid]['Name'] = name
            self.instructor_repository[cwid]['Dept'] = dept
        
        #reads grades file:
        grades_file_path: str = os.path.join(target_directory, 'grades.txt')

        for student_cwid, course, grade, instructor_cwid in file_reader(grades_file_path, 4, '\t'):
            self.student_class.add_completed_course(student_cwid, course, grade)
            self.instructor_class.add_course_taught(instructor_cwid, course)

            self.student_repository[student_cwid]['Completed Courses']
            self.student_repository[student_cwid]['Completed Courses'][course.upper()] = grade.upper()

            self.instructor_courses_taught_repository[instructor_cwid][course.upper()] += 1

    def all_students_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all students'''

        all_students_pretty_table: PrettyTable = PrettyTable(field_names = ['CWID', 'Name', 'Courses Completed'])

        for key, value in self.student_repository.items():
            all_students_pretty_table.add_row([key, value['Name'], sorted(list(value['completed courses'].keys()))])

        return all_students_pretty_table

    def all_instructors_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all instructors'''

        all_instructors_pretty_table: PrettyTable = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for key, value in self.instructor_repository.items():
            for course, students in self.instructor_courses_taught_repository[key].items():
                all_instructors_pretty_table.add_row([key, value['Name'], value['Dept'], course, students])

        return all_instructors_pretty_table


def main() -> None:
    '''Generates and returns student and instructor summary tables for a given unviversity directory'''

    stevens: Repository = Repository(input('Please enter a directory for Stevens: '))
    colombia: Repository = Repository(input('Please enter a directory for Colombia: '))
    nyu: Repository = Repository(input('Please enter a directory for NYU: '))

    university_names: List[str] = ['stevens', 'colombia', 'nyu']
    university_repositories: List[Repository] = [stevens, colombia, nyu]

    for university_name, university_repository in zip(university_names, university_repositories):
        print(f'\nSummaries for {university_name.capitalize()}')
        print(university_repository.all_students_summary())
        print(university_repository.all_instructors_summary())


if __name__ == '__main__':
    main()
