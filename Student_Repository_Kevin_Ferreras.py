'''The purpose of this file is to implement multiple classes and functions'''

from HW08_Kevin_Ferreras import file_reader
from typing import List, Dict, DefaultDict, IO, Any, Tuple, Set
from collections import defaultdict
from prettytable import PrettyTable
import os

class Student:
    '''Student Class'''

    student_summary_header: List[str] = ['CWID', 'Name', 'Courses Completed', 'Remaining Required', 'Remaining Electives', 'GPA']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        '''To represent a single student'''

        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._completed_courses: Dict[str, str] = dict() #key = course name : value = letter grade
        self._gpa: str = ''
        self._required_courses_remaining: List[str] = list()
        self._elective_courses_remaining: List[str] = list()

    def add_completed_course(self, course_name: str, letter_grade: str) -> None:
        '''Adds a completed course and its grade'''

        self._completed_courses[course_name.upper()] = letter_grade.upper()

    def calculate_gpa(self) -> None:
        '''Calculates a students GPA'''

        letter_grade_values: Dict[str, int] = {'A':4.0, 'A-':3.75, 'B+':3.25, 'B':3.0,
                                            'B-':2.75, 'C+':2.25, 'C':2.0, 'C-':0,
                                            'D+':0, 'D':0, 'D-':0, 'F':0,} #key = letter grade : value = grade value

        sum_of_grade_values: float = sum([letter_grade_values[letter_grade] for letter_grade in self._completed_courses.values()])
        self._gpa += f'{sum_of_grade_values/len(self._completed_courses):.2f}'

    def remaining_required_courses(self, major_name: str, flag: str, course: str) -> None:
        '''Summarizes the remaining required courses that a student has'''

        failing_grades: List[str] = ['C-', 'D+', 'D', 'D-', 'F']
        
        if major_name == self._major and flag == 'R':
            if course not in self._completed_courses:
                self._required_courses_remaining.append(course)
            elif self._completed_courses[course] in failing_grades:
                self._required_courses_remaining.append(course)

    def remaining_elective_courses(self, major_name: str, flag: str, course: str) -> None:
        '''Summarizes the remaining elective courses that a student has'''
        
        failing_grades: List[str] = ['C-', 'D+', 'D', 'D-', 'F']

        if major_name == self._major and flag == 'E':
            if course not in self._completed_courses:
                self._elective_courses_remaining.append(course)
            elif self._completed_courses[course] in failing_grades:
                self._elective_courses_remaining.append(course)

    def student_summary_row(self) -> Tuple[Any]: 
        '''Creates a summary for a single student that can be added as a row in the student prettytable in the 
            Repository class'''

        return self._cwid, self._name, sorted(self._completed_courses.keys()), sorted(self._required_courses_remaining), sorted(self._elective_courses_remaining), self._gpa
    

class Instructor:
    '''Instructor Class'''

    instructor_summary_header: List[str] = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        '''To represent a single instructor'''

        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses_taught: DefaultDict[str, int] = defaultdict(int) #key = course name : value = number of students in course

    def add_course_taught(self, course_name: str) -> None:
        '''Records the name of a course that has been taught by the instructor,
            and notes that a student took this course'''

        self._courses_taught[course_name] += 1

    def instructor_summary_row(self) -> Tuple[str, str, str, str, int]:
        '''Creates a summary for a single instructor that can be added as a row in the instructor prettytable in the 
            Repository class'''

        for course, student_count in self._courses_taught.items():
            yield self._cwid, self._name, self._dept, course, student_count


class Repository:
    '''Repository Class'''

    def __init__(self, target_directory: str) -> None:
        '''Sets the directory in which the necessary data files are stored'''

        try:
            os.chdir(target_directory)
        except FileNotFoundError as file_not_found:
            print(file_not_found)

        self._student_repository: Dict[str, Student] = dict() #key = CWID : value = an instacne of class Student
        self._instructor_repository: Dict[str, Instructor] = dict() #key = CWID: value = an instance of class Instructor
        self._majors_repository: DefaultDict[str, Defaultdict[str, List[str]]] = defaultdict(lambda: defaultdict(list)) #key = major : value = {'Required Courses': List, 'Electives': List}

        #Read students file:
        student_file_path: str = os.path.join(target_directory, 'students.txt')

        for cwid, name, major in file_reader(student_file_path, 3, ';', header = True):
            self._student_repository[cwid] = Student(cwid, name, major)
        
        #Read instructor file:
        instructor_file_path: str = os.path.join(target_directory, 'instructors.txt')

        for cwid, name, dept in file_reader(instructor_file_path, 3, '|', header = True):
            self._instructor_repository[cwid] = Instructor(cwid, name, dept)
            
        #Read grades file:
        grades_file_path: str = os.path.join(target_directory, 'grades.txt')

        for student_cwid, course, grade, instructor_cwid in file_reader(grades_file_path, 4, '|', header = True):
            if student_cwid not in self._student_repository:
                print(f'\nWARNING: Student CWID {student_cwid} has been identified as unknown. This CWID does not exist in the student repository.')
            elif instructor_cwid not in self._instructor_repository:
                print(f'WARNING: The Instructor CWID {instructor_cwid} has been identified as unkown. This CWID does not exist in the instructor repository.')
            else:
                self._student_repository[student_cwid].add_completed_course(course, grade)
                self._instructor_repository[instructor_cwid].add_course_taught(course)

        #Calculate student GPA:
        for student in self._student_repository.values():
            student.calculate_gpa()

        #Read majors file:
        majors_file_path: str = os.path.join(target_directory, 'majors.txt')

        for major, flag, course in file_reader(majors_file_path, 3, '\t', header = True):
            if flag == 'R':
                self._majors_repository[major]['Required Courses'].append(course)
            elif flag == 'E':
                self._majors_repository[major]['Electives'].append(course)

            for student in self._student_repository.values():
                student.remaining_required_courses(major, flag, course)
                student.remaining_elective_courses(major, flag, course)

    def all_students_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all students'''

        all_students_pretty_table: PrettyTable = PrettyTable(field_names = Student.student_summary_header)
        
        for key, value in self._student_repository.items():
            all_students_pretty_table.add_row(self._student_repository[key].student_summary_row())

        return all_students_pretty_table

    def all_instructors_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all instructors'''

        all_instructors_pretty_table: PrettyTable = PrettyTable(field_names = Instructor.instructor_summary_header)

        for key, value in self._instructor_repository.items():
            for row in self._instructor_repository[key].instructor_summary_row():
                all_instructors_pretty_table.add_row(row)

        return all_instructors_pretty_table

    def all_majors_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all majors'''

        all_majors_pretty_table: PrettyTable = PrettyTable(field_names = ['Major', 'Required Courses', 'Electives'])
        
        for key, value in self._majors_repository.items():
            all_majors_pretty_table.add_row([key, value['Required Courses'], value['Electives']])

        return all_majors_pretty_table


def main() -> None:
    '''Generates and returns student and instructor summary tables for a given unviversity directory'''

    stevens: Repository = Repository(input('Please enter a directory for Stevens: '))
    colombia: Repository = Repository(input('Please enter a directory for Colombia: '))
    nyu: Repository = Repository(input('Please enter a directory for NYU: '))

    university_names: List[str] = ['stevens', 'colombia', 'nyu']
    university_repositories: List[Repository] = [stevens, colombia, nyu]

    university_names: List[str] = ['stevens']
    university_repositories: List[Repository] = [stevens]

    for university_name, university_repository in zip(university_names, university_repositories):
        print(f'\nSummaries for {university_name.capitalize()}:')
        print(university_repository.all_majors_summary())
        print(university_repository.all_students_summary())
        print(university_repository.all_instructors_summary())


if __name__ == '__main__':
    main()



# x = Repository(r'C:\Users\Kevin\Documents\SSW810 - Software Dev Tools & Techniques')
# print(x.all_majors_summary())
# print(x.all_students_summary())
# print(x.all_instructors_summary())




