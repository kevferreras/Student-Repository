'''This file uses the Student Repository database to retrive data and display a completed summary table on a web page'''

from flask import Flask, render_template
from typing import List, Dict, Any
import sqlite3

DB_FILE: str = r'C:\Users\Kevin\Documents\SSW810 - Software Dev Tools & Techniques\student_repository_database.sqlite'

app: Flask = Flask(__name__)

@app.route('/completed')
def completed_courses() -> str:
    '''Retrieves student data from the Student Repository database, converts the data into a list of dictionaries, 
    and passes it to the student_courses.html template for display on a web page'''

    db: sqlite3.Connection = sqlite3.connect(DB_FILE)

    query: str = '''select students.Name, students.CWID, grades.Course, grades.Grade, instructors.Name
                        from students join grades on students.CWID = grades.StudentCWID
                        join instructors on grades.InstructorCWID = instructors.CWID order by students.Name ASC;'''

    data: List[Dict[str, str]] = [{'Name': name, 'CWID': cwid, 'Course': course, 'Grade': grade, 'Instructor': instructor}      
                                    for name, cwid, course, grade, instructor in db.execute(query)]

    db.close()

    return render_template('student_courses.html',
                            title = 'Stevens Repository',
                            table_title = 'Student Summary',
                            students = data)
    
app.run(debug= True)