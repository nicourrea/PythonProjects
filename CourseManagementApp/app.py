# Name: Nicolas Urrea
# FSUID: <nu22c>
# Due Date: 06/20/2025
# The program in this file is the individual work of Nicolas Urrea

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/addCourse", methods=["GET"])
def show_add_course_form():
    return render_template("addCourse.html")

@app.route("/addCourse", methods=["POST"])
def add_course():
    conn = None  
    try:
        conn = sqlite3.connect('courseData.db')
        cursor = conn.cursor()
        
        # Get form data
        course_title = request.form["course_title"]
        course_department = request.form["course_department"]
        semester = request.form["semester"]
        enrollment = int(request.form["enrollment"])
        
        instructor_id = request.form["instructor_id"]
        instructor_name = request.form["instructor_name"]
        instructor_department = request.form["instructor_department"]
        job_title = request.form["job_title"]
        
        # Generate CourseID from first 5 letters of title + semester
        course_id = course_title[:5] + semester

        # Insert instructor into Employees
        cursor.execute("""
            INSERT INTO Employees (EmployeeID, Name, Department, JobTitle, Salary)
            VALUES (?, ?, ?, ?, ?)
        """, (instructor_id, instructor_name, instructor_department, job_title, 65000.0))

        # Insert course into Courses
        cursor.execute("""
            INSERT INTO Courses (CourseID, Title, Department, Semester, InstructorID, Enrollment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (course_id, course_title, course_department, semester, instructor_id, enrollment))

        conn.commit()
        return redirect('/')
    
    except Exception as e:
        if conn:
            conn.rollback()
        return f"An error occurred: {e}"
    
    finally:
        if conn:
            conn.close()

@app.route('/getCourses', methods=['GET'])
def show_get_courses_form():
    return render_template("getCourses.html")

@app.route('/getCourses', methods=['POST'])
def get_courses():
    conn = None
    try:
        conn = sqlite3.connect('courseData.db')
        cursor = conn.cursor()

        instructor_name = request.form['instructor_name']

        # Get EmployeeID for the instructor
        cursor.execute("SELECT EmployeeID FROM Employees WHERE Name = ?", (instructor_name,))
        row = cursor.fetchone()
        
        if not row:
            return f"No instructor found with name: {instructor_name}"

        instructor_id = row[0]

        # Fetch all courses by this instructor
        cursor.execute("""
            SELECT CourseID, Title, Department, Enrollment
            FROM Courses
            WHERE InstructorID = ?
        """, (instructor_id,))

        courses = cursor.fetchall()

        return render_template('listByInstructor.html', instructor_name=instructor_name, courses=courses)

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if conn:
            conn.close()

@app.route('/getDept', methods=['GET'])
def show_get_dept_form():
    return render_template("getDept.html")

@app.route('/getDept', methods=['POST'])
def get_dept():
    conn = None
    try:
        conn = sqlite3.connect('courseData.db')
        cursor = conn.cursor()

        dept = request.form['department']

        cursor.execute("""
            SELECT Title, AVG(Enrollment) as avg_enroll
            FROM Courses
            WHERE Department = ?
            GROUP BY Title
            ORDER BY avg_enroll DESC, Title ASC
            LIMIT 5;
        """, (dept,))

        results = cursor.fetchall()

        return render_template('top5dept.html', department=dept, results=results)

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)