'''The purpose of this file is to implement multiple classes and functions'''

from HW08_Kevin_Ferreras import file_reader
from typing import List, Dict, DefaultDict, IO, Any, Tuple, Set
from collections import defaultdict
from prettytable import PrettyTable
import os
import sqlite3

DB_FILE: str = r'C:\Users\Kevin\Documents\SSW810 - Software Dev Tools & Techniques\student_repository_database.sqlite'


class Student:
    '''Student Class'''

    student_summary_header: List[str] = ['CWID', 'Name', 'Courses Completed', 'Remaining Required', 'Remaining Electives', 'GPA']
    _failing_grades: List[str] = ['C-', 'D+', 'D', 'D-', 'F']
    _letter_grade_values: Dict[str, float] = {'A':4.0, 'A-':3.75, 'B+':3.25, 'B':3.0,
                                    'B-':2.75, 'C+':2.25, 'C':2.0, 'C-':0,
                                    'D+':0, 'D':0, 'D-':0, 'F':0,} #key = letter grade : value = grade value

    def __init__(self, cwid: str, name: str, major: str, required: Set[str], elective: Set[str]) -> None:
        '''To represent a single student'''

        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._completed_courses: Dict[str, str] = dict() #key = course name : value = letter grade
        self._gpa: str = ''
        self._required_courses_remaining: Set[str] = required
        self._elective_courses_remaining: Set[str] = elective

    def add_completed_course(self, course_name: str, letter_grade: str) -> None:
        '''Adds a completed course and its grade'''

        if letter_grade not in Student._letter_grade_values:
            raise ValueError(f'Grade {letter_grade}, being entered for {course_name} is not a valid grade.')
        else:
            self._completed_courses[course_name] = letter_grade.upper()

            if letter_grade.upper() not in Student._failing_grades:
                if course_name in self._required_courses_remaining:
                    self._required_courses_remaining.remove(course_name)
                
                if course_name in self._elective_courses_remaining:
                    self._elective_courses_remaining = set()

    def calculate_gpa(self) -> None:
        '''Calculates a students GPA'''

        sum_of_grade_values: float = sum([Student._letter_grade_values[letter_grade] for letter_grade in self._completed_courses.values()])

        try:
            self._gpa += f'{sum_of_grade_values/len(self._completed_courses):.2f}'
        except ZeroDivisionError:
            self._gpa: str = '0.0'

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
        
        self._target_directory = target_directory
        try:
            os.chdir(self._target_directory)
        except FileNotFoundError as file_not_found:
            print(file_not_found)

        self._student_repository: Dict[str, Student] = dict() #key = CWID : value = an instacne of class Student
        self._instructor_repository: Dict[str, Instructor] = dict() #key = CWID: value = an instance of class Instructor
        self._majors_repository: DefaultDict[str, DefaultDict[str, List[str]]] = defaultdict(lambda: defaultdict(list)) #key = major : value = {'R': List, 'E': List}

        self.try_files()
        self.calculate_gpa()

    def try_files(self) -> str:
        '''Reads the necessary data file need to populate the students, instructors, and majors repositories'''

        try:
            self.read_majors_file()
            self.read_students_file()
            self.read_instructors_file()
            self.read_grades_file()
        except FileNotFoundError as error:
            print(error)

    def read_majors_file(self) -> None:
        '''Reads the majors file, updates the majors repository, and sends major, flag, course info to Class Student to update/populate the
            remaining and elective courses that each student has'''

        majors_file_path: str = os.path.join(self._target_directory, 'majors.txt')

        for major, flag, course in file_reader(majors_file_path, 3, '\t', header = True):
            if flag == 'R': # R = Required
                self._majors_repository[major][flag].append(course)
            elif flag == 'E': # E = Electives
                self._majors_repository[major][flag].append(course)

    def read_students_file(self) -> None:
        '''Reads the students file and updates the student directory'''

        student_file_path: str = os.path.join(self._target_directory, 'students.txt')

        for cwid, name, major in file_reader(student_file_path, 3, '\t', header = True):
            self._student_repository[cwid] = Student(cwid, name, major, set(self._majors_repository[major]['R']), set(self._majors_repository[major]['E']))
        
    def read_instructors_file(self) -> None:
        '''Reads the instructors file and updates the instructor repository'''

        instructor_file_path: str = os.path.join(self._target_directory, 'instructors.txt')

        for cwid, name, dept in file_reader(instructor_file_path, 3, '\t', header = True):
            self._instructor_repository[cwid] = Instructor(cwid, name, dept)
            
    def read_grades_file(self) -> None:
        '''Reads the grades file and sends Class Student and Class Instructor course and grade info
            to update the courses completed for students and the courses taught for instructors'''

        grades_file_path: str = os.path.join(self._target_directory, 'grades.txt')

        for student_cwid, course, grade, instructor_cwid in file_reader(grades_file_path, 4, '\t', header = True):
            if student_cwid not in self._student_repository:
                print(f'WARNING: Student CWID {student_cwid} has been identified as unknown. This CWID does not exist in the student repository.')
            elif instructor_cwid not in self._instructor_repository:
                print(f'WARNING: The Instructor CWID {instructor_cwid} has been identified as unkown. This CWID does not exist in the instructor repository.')
            else:
                self._student_repository[student_cwid].add_completed_course(course, grade)
                self._instructor_repository[instructor_cwid].add_course_taught(course)

    def calculate_gpa(self) -> None:
        '''Calls method calculate_gpa from Class Student for every student in the student repository in order to calculate
            their gpa'''

        for student in self._student_repository.values():
            student.calculate_gpa()
           
    def all_students_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all students'''

        all_students_pretty_table: PrettyTable = PrettyTable(field_names = Student.student_summary_header)
        
        for key, value in self._student_repository.items():
            all_students_pretty_table.add_row(self._student_repository[key].student_summary_row())

        return f'\nStudents Summary:\n{all_students_pretty_table}'

    def all_instructors_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all instructors'''

        all_instructors_pretty_table: PrettyTable = PrettyTable(field_names = Instructor.instructor_summary_header)

        for key, value in self._instructor_repository.items():
            for row in self._instructor_repository[key].instructor_summary_row():
                all_instructors_pretty_table.add_row(row)

        return f'\nInstructors Summary:\n{all_instructors_pretty_table}'

    def all_majors_summary(self) -> PrettyTable:
        '''Returns a prettytable summary of all majors'''

        all_majors_pretty_table: PrettyTable = PrettyTable(field_names = ['Major', 'Required Courses', 'Electives'])
        
        for key, value in self._majors_repository.items():
            all_majors_pretty_table.add_row([key, value['R'], value['E']]) 

        return f'\nMajors Summary:\n{all_majors_pretty_table}'

    def student_grades_table_db(self, db_path: str) -> PrettyTable:
        '''Retrieves data from SQLite database to create a new student summary table that contains:
            Student Name, CWID, Course, Grade, Instructor Name'''

        db: sqlite3.Connection = sqlite3.connect(db_path)
        query: str = '''select students.Name, students.CWID, grades.Course, grades.Grade, instructors.Name
                        from students join grades on students.CWID = grades.StudentCWID
                        join instructors on grades.InstructorCWID = instructors.CWID order by students.Name ASC;'''

        student_grades_summary_prettytable: PrettyTable = PrettyTable(field_names = ['Name', 'CWID', 'Course', 'Grade', 'Instructor'])

        for row in db.execute(query):
            student_grades_summary_prettytable.add_row(row)
        
        return f'\nStudent Grade Summary:\n{student_grades_summary_prettytable}'
                
def main() -> None:
    '''Generates and returns student and instructor summary tables for a given unviversity directory'''

    stevens: Repository = Repository(input('Please enter a directory for Stevens: '))
    colombia: Repository = Repository(input('Please enter a directory for Colombia: '))
    nyu: Repository = Repository(input('Please enter a directory for NYU: '))

    university_names: List[str] = ['stevens', 'colombia', 'nyu']
    university_repositories: List[Repository] = [stevens, colombia, nyu]

    for university_name, university_repository in zip(university_names, university_repositories):
        print(f'\nSummaries for {university_name.capitalize()}:')
        print(university_repository.all_majors_summary())
        print(university_repository.all_students_summary())
        print(university_repository.all_instructors_summary())
        print(university_repository.student_grades_table_db(DB_FILE))

# if __name__ == '__main__':
#     main()

x = Repository(os.getcwd())
print(x.all_majors_summary())
print(x.all_students_summary())
print(x.all_instructors_summary())
print(x.student_grades_table_db(DB_FILE))