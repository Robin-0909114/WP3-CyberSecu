from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import datetime
import sqlite3
import socket

admin = Blueprint('admin', __name__)

conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db', check_same_thread=False)
c = conn.cursor()


# Route to display all students in a HTML table
@admin.route('/admin/students', methods=['GET'])
def admin_students():
    if 'admin_logged_in' in session:
        c.execute("SELECT * FROM Students")
        students = c.fetchall()
        return render_template('admin/admin_students.html', students=students)
    else:
        return redirect(url_for('index'))



@admin.route('/admin/students/add', methods=['GET'])
def add_student_form():
    if 'admin_logged_in' in session:
        return render_template('admin/admin_add_students.html')
    else:
        return redirect(url_for('index'))

# Route to add a new student
@admin.route('/admin/students/add', methods=['POST'])
def add_student():
    if 'admin_logged_in' in session:
        student_name = request.form['student_name']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']
        student_number = request.form['student_number']
        class_id = request.form['class_id']

        c.execute("INSERT INTO students (student_name, other_details, username, password, studentnumber, class_id) VALUES (?, ?, ?, ?, ?, ?)",
                (student_name, other_details, username, password, student_number, class_id))
        conn.commit()

        return admin_students()
    else:
        return redirect(url_for('index'))

# Route to update an existing student
@admin.route('/admin/students/update', methods=['POST'])
def update_student():
    if 'admin_logged_in' in session:
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']
        student_number = request.form['student_number']
        class_id = request.form['class_id']

        c.execute("UPDATE students SET student_name = ?, other_details = ?, username = ?, password = ?, student_number = ?, class_id = ? WHERE student_id = ?",
                (student_name, other_details, username, password, student_number, class_id, student_id))
        conn.commit()

        return admin_students()
    else:
        return redirect(url_for('index'))

@admin.route('/admin/students/update/<int:student_id>', methods=['GET', 'POST'])
def update_student_per_id(student_id=None):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            student_name = request.form['student_name']
            other_details = request.form['other_details']
            username = request.form['username']
            password = request.form['password']
            student_number = request.form['student_number']
            class_id = request.form['class_id']

            c.execute("UPDATE students SET student_name = ?, other_details = ?, username = ?, password = ?, studentnumber = ?, class_id = ? WHERE student_id = ?",
                    (student_name, other_details, username, password, student_number, class_id, student_id))
            conn.commit()

            return admin_students()
        else:
            c.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
            student = c.fetchone()
            return render_template('admin/admin_update_students.html', student=student)
    else:
        return redirect(url_for('index'))

# Route to delete a student
@admin.route('/admin/students/delete', methods=['POST'])
def delete_student():
    if 'admin_logged_in' in session:
        student_id = request.form['student_id']

        c.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()

        return admin_students()
    else:
        return redirect(url_for('index'))

# Route to display all faculties in an HTML table
@admin.route('/admin/faculties', methods=['GET'])
def admin_faculties():
    if 'admin_logged_in' in session:
        c.execute("SELECT * FROM Faculty")
        faculties = c.fetchall()
        return render_template('admin/admin_faculties.html', faculties=faculties)
    else:
        return redirect(url_for('index'))

@admin.route('/admin/faculties/add', methods=['GET'])
def add_faculty_form():
    if 'admin_logged_in' in session:
        return render_template('admin_add_faculties.html')
    else:
        return redirect(url_for('index'))

# Route to add a new faculty
@admin.route('/admin/faculties/add', methods=['POST'])
def add_faculty():
    if 'admin_logged_in' in session:
        faculty_name = request.form['faculty_name']
        faculty_email = request.form['faculty_email']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']

        c.execute("INSERT INTO faculty (faculty_name, faculty_email, other_details, username, password) VALUES (?, ?, ?, ?, ?)",
                (faculty_name, faculty_email, other_details, username, password))
        conn.commit()

        return admin_faculties()
    else:
        return redirect(url_for('index'))

# Route to update an existing faculty
@admin.route('/admin/faculties/update', methods=['POST'])
def update_faculty():
    if 'admin_logged_in' in session:
        faculty_id = request.form['faculty_id']
        faculty_name = request.form['faculty_name']
        faculty_email = request.form['faculty_email']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']

        c.execute("UPDATE faculty SET faculty_name = ?, faculty_email = ?, other_details = ?, username = ?, password = ? WHERE faculty_id = ?",
                (faculty_name, faculty_email, other_details, username, password, faculty_id))
        conn.commit()

        return admin_faculties()
    else:
        return redirect(url_for('index'))

@admin.route('/admin/faculties/update/<int:faculty_id>', methods=['GET', 'POST'])
def update_faculty_per_id(faculty_id=None):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            faculty_name = request.form['faculty_name']
            faculty_email = request.form['faculty_email']
            other_details = request.form['other_details']
            username = request.form['username']
            password = request.form['password']

            c.execute("UPDATE faculty SET faculty_name = ?, faculty_email = ?, other_details = ?, username = ?, password = ? WHERE faculty_id = ?",
                    (faculty_name, faculty_email, other_details, username, password, faculty_id))
            conn.commit()

            return admin_faculties()
        else:
            c.execute("SELECT * FROM Faculty WHERE faculty_id = ?", (faculty_id,))
            faculty = c.fetchone()
            return render_template('admin/admin_update_faculties.html', faculty=faculty)
    else:
        return redirect(url_for('index'))

# Route to delete a faculty
@admin.route('/admin/faculties/delete', methods=['POST'])
def delete_faculty():
    if 'admin_logged_in' in session:
        faculty_id = request.form['faculty_id']

        c.execute("DELETE FROM faculty WHERE faculty_id = ?", (faculty_id,))
        conn.commit()

        return admin_faculties()
    else:
        return redirect(url_for('index'))

@admin.route('/admin/meetings', methods=['GET'])
def admin_meetings():
    if 'admin_logged_in' in session:
        c.execute("SELECT * FROM Meeting")
        meetings = c.fetchall()
        return render_template('admin/admin_meetings.html', meetings=meetings)
    else:
        return redirect(url_for('index'))


@admin.route('/admin/meetings/add', methods=['GET'])
def add_meeting_form():
    if 'admin_logged_in' in session:
        return render_template('admin/admin_add_meetings.html')
    else:
        return redirect(url_for('index'))

# Route to add a new meeting
@admin.route('/admin/meetings/add', methods=['POST'])
def add_meeting():
    if 'admin_logged_in' in session:
        meeting_title = request.form['meeting_title']
        meeting_date = request.form['meeting_date']
        meeting_time = request.form['meeting_time']
        meeting_duration = request.form['meeting_duration']
        meeting_location = request.form['meeting_location']
        meeting_description = request.form['meeting_description']
        class_id = request.form['class_id']
        meeting_status = request.form['meeting_status']
        question = request.form['question']

        c.execute("INSERT INTO Meeting (meeting_title, meeting_date, meeting_time, meeting_duration, meeting_location, meeting_description, class_id, meeting_status, question) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (meeting_title, meeting_date, meeting_time, meeting_duration, meeting_location, meeting_description, class_id, meeting_status, question))
        conn.commit()

        return admin_meetings()
    else:
        return redirect(url_for('index'))

# Route to update an existing meeting
@admin.route('/admin/meetings/update', methods=['POST'])
def update_meeting():
    if 'admin_logged_in' in session:
        meeting_id = request.form['meeting_id']
        meeting_title = request.form['meeting_title']
        meeting_date = request.form['meeting_date']
        meeting_time = request.form['meeting_time']
        meeting_duration = request.form['meeting_duration']
        meeting_location = request.form['meeting_location']
        meeting_description = request.form['meeting_description']
        created_by = request.form['created_by']
        created_at = request.form['created_at']
        updated_at = request.form['updated_at']
        class_id = request.form['class_id']
        meeting_status = request.form['meeting_status']
        question = request.form['question']

        c.execute("UPDATE Meeting SET meeting_title = ?, meeting_date = ?, meeting_time = ?, meeting_duration = ?, meeting_location = ?, meeting_description = ?, created_by = ?, created_at = ?, updated_at = ?, class_id = ?, meeting_status = ?, question = ? WHERE meeting_id = ?",
                (meeting_title, meeting_date, meeting_time, meeting_duration, meeting_location, meeting_description, created_by, created_at, updated_at, class_id, meeting_status, question, meeting_id))
        conn.commit()

        return admin_meetings()
    else:
        return redirect(url_for('index'))

# Route to update a specific meeting
@admin.route('/admin/meetings/update/<int:meeting_id>', methods=['GET', 'POST'])
def update_meeting_per_id(meeting_id=None):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            meeting_title = request.form['meeting_title']
            meeting_date = request.form['meeting_date']
            meeting_time = request.form['meeting_time']
            meeting_duration = request.form['meeting_duration']
            meeting_location = request.form['meeting_location']
            meeting_description = request.form['meeting_description']
            class_id = request.form['class_id']
            meeting_status = request.form['meeting_status']
            question = request.form['question']

            c.execute("UPDATE Meeting SET meeting_title = ?, meeting_date = ?, meeting_time = ?, meeting_duration = ?, meeting_location = ?, meeting_description = ?, class_id = ?, meeting_status = ?, question = ?, updated_at = datetime('now') WHERE meeting_id = ?",
                    (meeting_title, meeting_date, meeting_time, meeting_duration, meeting_location, meeting_description, class_id, meeting_status, question, meeting_id))
            conn.commit()

            return admin_meetings()
        else:
            c.execute("SELECT * FROM Meeting WHERE meeting_id = ?", (meeting_id,))
            meeting = c.fetchone()
            return render_template('admin/admin_update_meetings.html', meeting=meeting)
    else:
        return redirect(url_for('index'))
    
@admin.route('/admin/meetings/delete', methods=['POST'])
def delete_meeting():
    if 'admin_logged_in' in session:
        meeting_id = request.form['meeting_id']

        c.execute("DELETE FROM meeting WHERE meeting_id = ?", (meeting_id,))
        conn.commit()

        return admin_meetings()
    else:
        return redirect(url_for('index'))
    
# Route to see all classes
@admin.route('/admin/classes', methods=['GET'])
def admin_classes():
    if 'admin_logged_in' in session:
        c.execute("SELECT * FROM Class")
        classes = c.fetchall()
        return render_template('admin/admin_classes.html', classes=classes)
    else:
        return redirect(url_for('index'))

@admin.route('/admin/classes/add', methods=['GET'])
def add_class_form():
    if 'admin_logged_in' in session:
        return render_template('admin/admin_add_class.html')
    else:
        return redirect(url_for('index'))

# Route to add a new class
@admin.route('/admin/classes/add', methods=['POST'])
def add_class():
    if 'admin_logged_in' in session:
        class_name = request.form['class_name']

        c.execute("INSERT INTO Class (classname) VALUES (?)",
                (class_name,))
        conn.commit()

        return admin_classes()
    else:
        return redirect(url_for('index'))

# Route to update an existing student
@admin.route('/admin/classes/update', methods=['POST'])
def update_class():
    if 'admin_logged_in' in session:
        class_id = request.form['class_id']
        class_name = request.form['class_name']

        c.execute("UPDATE Class SET classname = ? WHERE class_id = ?",
                (class_name, class_id))
        conn.commit()

        return admin_classes()
    else:
        return redirect(url_for('index'))

# Route to update a class
@admin.route('/admin/classes/update/<int:class_id>', methods=['GET', 'POST'])
def update_classes_per_id(class_id=None):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            class_name = request.form['class_name']

            c.execute("UPDATE Class SET classname = ? WHERE class_id = ?",
                    (class_name, class_id))
            conn.commit()

            return admin_classes()
        else:
            c.execute("SELECT * FROM Class WHERE class_id = ?", (class_id,))
            classes = c.fetchone()
            return render_template('admin/admin_update_class.html', classes=classes)
    else:
        return redirect(url_for('index'))

# Route to delete a class
@admin.route('/admin/classes/delete', methods=['POST'])
def delete_class():
    if 'admin_logged_in' in session:  
        class_id = request.form['class_id']

        c.execute("DELETE FROM Class WHERE class_id = ?", (class_id,))
        conn.commit()

        return admin_classes()
    else:
        return redirect(url_for('index'))
    

# Route to see all attendance
@admin.route('/admin/attendance', methods=['GET'])
def admin_attendance():
    if 'admin_logged_in' in session:
        c.execute("SELECT * FROM Attendance")
        attendances = c.fetchall()
        return render_template('admin/admin_attendance.html', attendances=attendances)
    else:
        return redirect(url_for('index'))

@admin.route('/admin/attendance/add', methods=['GET'])
def add_attendance_form():
    if 'admin_logged_in' in session:
        return render_template('admin/admin_add_attendance.html')
    else:
        return redirect(url_for('index'))

# Route to add a new class
@admin.route('/admin/attendance/add', methods=['POST'])
def add_attendance():
    if 'admin_logged_in' in session:
        attendance_date = request.form['attendance_date']
        attendance_time = request.form['attendance_time']
        status = request.form['status']
        student_number = request.form['student_number']
        question = request.form['question']
        answer = request.form['answer']
        reason = request.form['reason']
        student_id = request.form['student_id']
        meeting_id = request.form['meeting_id']
        class_id = request.form['class_id']

        c.execute("INSERT INTO Attendance (attendance_date, attendance_time, status, Studentnumber, Question, Answer, Reason, student_id, meeting_id, class_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (attendance_date, attendance_time, status, student_number, question, answer, reason, student_id, meeting_id, class_id,))
        conn.commit()

        return admin_attendance()
    else:
        return redirect(url_for('index'))

# Route to update an existing attendance
@admin.route('/admin/attendance/update', methods=['POST'])
def update_attendance():
    if 'admin_logged_in' in session:
        attendance_id = request.form['attendance_id']
        attendance_date = request.form['attendance_date']
        attendance_time = request.form['attendance_time']
        status = request.form['status']
        student_number = request.form['student_number']
        question = request.form['question']
        answer = request.form['answer']
        reason = request.form['reason']
        student_id = request.form['student_id']
        meeting_id = request.form['meeting_id']
        class_id = request.form['class_id']

        c.execute("UPDATE Attendance SET attendance_date = ?, attendance_time = ?, status = ?, Studentnumber = ?, Question = ?, Answer = ?, Reason = ?, student_id = ?, meeting_id = ?, class_id = ? WHERE attendance_id = ?",
            (attendance_date, attendance_time, status, student_number, question, answer, reason, student_id, meeting_id, class_id, attendance_id))
        conn.commit()

        return admin_attendance()
    else:
        return redirect(url_for('index'))

# Route to update attendance
@admin.route('/admin/attendance/update/<int:attendance_id>', methods=['GET', 'POST'])
def update_attendance_per_id(attendance_id=None):
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            attendance_date = request.form['attendance_date']
            attendance_time = request.form['attendance_time']
            status = request.form['status']
            student_number = request.form['student_number']
            question = request.form['question']
            answer = request.form['answer']
            reason = request.form['reason']
            student_id = request.form['student_id']
            meeting_id = request.form['meeting_id']
            class_id = request.form['class_id']

            c.execute("UPDATE Attendance SET attendance_date = ?, attendance_time = ?, status = ?, Studentnumber = ?, Question = ?, Answer = ?, Reason = ?, student_id = ?, meeting_id = ?, class_id = ? WHERE attendance_id = ?",
                    (attendance_date, attendance_time, status, student_number, question, answer, reason, student_id, meeting_id, class_id, attendance_id))
            conn.commit()

            return admin_attendance()
        else:
            c.execute("SELECT * FROM Attendance WHERE attendance_id = ?", (attendance_id,))
            attendances = c.fetchone()
            return render_template('admin/admin_update_attendance.html', attendances=attendances)
    else:
        return redirect(url_for('index'))

# Route to delete a attendance
@admin.route('/admin/attendance/delete', methods=['POST'])
def delete_attendance():
    if 'admin_logged_in' in session:  
        attendance_id = request.form['attendance_id']

        c.execute("DELETE FROM attendance WHERE attendance_id = ?", (attendance_id,))
        conn.commit()

        return admin_attendance()
    else:
        return redirect(url_for('index'))