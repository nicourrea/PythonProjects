# Name: Nicolas Urrea
# FSUID: <nu22c>
# Due Date: 06/20/2025
# The program in this file is the individual work of Nicolas Urrea

import sqlite3

def createTables():
    conn = sqlite3.connect("courseData.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID TEXT PRIMARY KEY,
            Name TEXT,
            Department TEXT,
            JobTitle TEXT,
            Salary FLOAT
        );
    """);
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Courses (
        CourseID TEXT PRIMARY KEY,
        Title TEXT,
        Department TEXT,
        Semester TEXT,
        InstructorID TEXT,
        Enrollment INTEGER,
        FOREIGN KEY (InstructorID) REFERENCES Employees(EmployeeID)
        );
    """)
    
    conn.commit()
    conn.close()
   
if __name__ == "__main__":
    createTables()