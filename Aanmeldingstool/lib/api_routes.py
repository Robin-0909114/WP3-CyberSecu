# Accesible through Postman 

import sqlite3
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, Blueprint, session
from flask_cors import CORS
import pytz
from hashids import Hashids

students_api = Blueprint('students_api', __name__)
CORS(students_api, resources={r"/*": {"origins": "*"}})
hashids = Hashids(salt='your_secret_salt_value_here')
amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    
def connect_to_db():
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    return conn

def insert_student(student):
    inserted_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Students (Student_id, Student_name, Other_details, Username, Password, Studentnumber) 
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                    (student['Student_id'], student['Student_name'], student['Other_details'], 
                     student['Username'], student['Password'], student['Studentnumber']))
        conn.commit()
        inserted_student = get_student_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_student

def get_students():
    students = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students")
        rows = cur.fetchall()

        for i in rows:
            student = {}
            student["Student_id"] = i["Student_id"]
            student["Student_name"] = i["Student_name"]
            student["Other_details"] = i["Other_details"]
            student["Class_id"] = i["Class_id"]
            student["Username"] = i["Username"]
            student["Password"] = i["Password"]
            student["Studentnumber"] = i["Studentnumber"]
            students.append(student)
    except:
        students = []

    return students

def get_student_by_id(student_id):
    student = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students WHERE Student_id = ?", 
                    (student_id,))
        row = cur.fetchone()

        student["Student_id"] = row["Student_id"]
        student["Student_name"] = row["Student_name"]
        student["Other_details"] = row["Other_details"]
        student["Class_id"] = row["Class_id"]
        student["Username"] = row["Username"]
        student["Password"] = row["Password"]
        student["Studentnumber"] = row["Studentnumber"]
    except:
        student = {}

    return student

def update_student(student):
    updated_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Students SET Student_name = ?, Other_details = ?, Class_id = ?,Username = ?, Password = ?, Studentnumber = ?
                       WHERE Student_id = ?''',
                    (student["Student_name"], student["Other_details"], student["Class_id"], student["Username"], 
                     student["Password"], student["Studentnumber"], student["Student_id"],))
        conn.commit()
        updated_student = get_student_by_id(student["Student_id"])
    except:
        conn.rollback()
        updated_student = {}
    finally:
        conn.close()

    return updated_student

def delete_student(student_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Students WHERE Student_id = ?",     
                      (student_id,))
        conn.commit()
        message["status"] = "Student deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Student"
    finally:
        conn.close()

    return message

def insert_faculty(faculty):
    inserted_faculty = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Faculty (Faculty_id, Faculty_name, Faculty_email, Other_details, Username, Password) 
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                    (faculty['Faculty_id'], faculty['Faculty_name'], faculty['Faculty_email'], 
                     faculty['Other_details'], faculty['Username'], faculty['Password']))
        conn.commit()
        inserted_faculty = get_faculty_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_faculty

def get_faculties():
    faculties = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Faculty")
        rows = cur.fetchall()

        for i in rows:
            faculty = {}
            faculty["Faculty_id"] = i["Faculty_id"]
            faculty["Faculty_name"] = i["Faculty_name"]
            faculty["Faculty_email"] = i["Faculty_email"]
            faculty["Other_details"] = i["Other_details"]
            faculty["Username"] = i["Username"]
            faculty["Password"] = i["Password"]
            faculties.append(faculty)
    except:
        faculties = []

    return faculties

def get_faculty_by_id(faculty_id):
    faculty = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Faculty WHERE Faculty_id = ?", 
                    (faculty_id,))
        row = cur.fetchone()

        faculty["Faculty_id"] = row["Faculty_id"]
        faculty["Faculty_name"] = row["Faculty_name"]
        faculty["Faculty_email"] = row["Faculty_email"]
        faculty["Other_details"] = row["Other_details"]
        faculty["Username"] = row["Username"]
        faculty["Password"] = row["Password"]
    except:
        faculty = {}

    return faculty

def update_faculty(faculty):
    updated_faculty = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Faculty SET Faculty_name = ?, Faculty_email = ?, Other_details = ?, Username = ?, Password = ?
                       WHERE Faculty_id = ?''',
                    (faculty["Faculty_name"], faculty["Faculty_email"], faculty["Other_details"], 
                     faculty["Username"], faculty["Password"], faculty["Faculty_id"],))
        conn.commit()
        updated_faculty = get_faculty_by_id(faculty["Faculty_id"])
    except:
        conn.rollback()
        updated_faculty = {}
    finally:
        conn.close()

    return updated_faculty

def delete_faculty(faculty_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Faculty WHERE Faculty_id = ?",     
                      (faculty_id,))
        conn.commit()
        message["status"] = "Faculty deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Faculty"
    finally:
        conn.close()

    return message

def insert_schedule(schedule):
    inserted_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO schedule (schedule_id, course_id, faculty_id, room_id, start_time, end_time, days) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (schedule['schedule_id'], schedule['course_id'], schedule['faculty_id'], 
                     schedule['room_id'], schedule['start_time'], schedule['end_time'], schedule['days']))
        conn.commit()
        inserted_schedule = get_schedule_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_schedule

def get_schedule():
    schedules = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Schedule")
        rows = cur.fetchall()

        
        for i in rows:
            schedule = {}
            schedule["schedule_id"] = i["schedule_id"]
            schedule["course_id"] = i["course_id"]
            schedule["faculty_id"] = i["faculty_id"]
            schedule["room_id"] = i["room_id"]
            schedule["start_time"] = i["start_time"]
            schedule["end_time"] = i["end_time"]
            schedule["days"] = i["days"]
            schedules.append(schedule)
    except:
        schedules = []

    return schedules

def get_schedule_by_id(schedule_id):
    schedule = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Schedule WHERE Schedule_id = ?", 
                    (schedule_id,))
        row = cur.fetchone()

        
        schedule["schedule_id"] = row["schedule_id"]
        schedule["course_id"] = row["course_id"]
        schedule["faculty_id"] = row["faculty_id"]
        schedule["room_id"] = row["room_id"]
        schedule["start_time"] = row["start_time"]
        schedule["end_time"] = row["end_time"]
        schedule["days"] = row["days"]
    except:
        schedule = {}

    return schedule

def update_schedule(schedule):
    updated_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Schedule SET course_id = ?, faculty_id = ?, room_id = ?, start_time = ?, end_time = ?, days = ?
                       WHERE Schedule_id = ?''',
                    (schedule["Course_id"], schedule["Faculty_id"], schedule["Room_id"], 
                     schedule["Start_time"], schedule["End_time"], schedule["Schedule_id"], schedule["Days"]))
        conn.commit()

        updated_schedule = get_schedule_by_id(schedule["Schedule_id"])
    except:
        conn.rollback()
        updated_schedule = {}
    finally:
        conn.close()

    return updated_schedule

def update_schedule_by_id(schedule_id, schedule):
    updated_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE schedule SET course_id = ?, faculty_id = ?, room_id = ?, start_time = ?, end_time = ?, days = ?
                       WHERE Schedule_id = ?''',
                    (schedule["course_id"], schedule["faculty_id"], schedule["room_id"], 
                     schedule["start_time"], schedule["end_time"], schedule["days"], schedule_id))
        conn.commit()
        updated_schedule = get_schedule_by_id(schedule_id)
    except:
        conn.rollback()
        updated_schedule = {}
    finally:
        conn.close()

    return updated_schedule

def delete_schedule(schedule_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Schedule WHERE Schedule_id = ?",     
                      (schedule_id,))
        conn.commit()
        message["status"] = "Schedule deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Schedule"
    finally:
        conn.close()

    return message


@students_api.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(get_students())

@students_api.route('/api/students/<student_id>', methods=['GET'])
def api_get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@students_api.route('/api/students/add', methods=['POST'])
def api_add_student():
    student = request.get_json()
    return jsonify(insert_student(student))

@students_api.route('/api/students/update', methods=['PUT'])
def api_update_student():
    student = request.get_json()
    return jsonify(update_student(student))

@students_api.route('/api/students/delete/<student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    return jsonify(delete_student(student_id))

@students_api.route('/api/faculties', methods=['GET'])
def api_get_faculties():
    return jsonify(get_faculties())

@students_api.route('/api/faculties/<faculty_id>', methods=['GET'])
def api_get_faculty(faculty_id):
    return jsonify(get_faculty_by_id(faculty_id))

@students_api.route('/api/faculties/add', methods=['POST'])
def api_add_faculty():
    faculty = request.get_json()
    return jsonify(insert_faculty(faculty))

@students_api.route('/api/faculties/update', methods=['PUT'])
def api_update_faculty():
    faculty = request.get_json()
    return jsonify(update_faculty(faculty))

@students_api.route('/api/faculties/delete/<faculty_id>', methods=['DELETE'])
def api_delete_faculty(faculty_id):
    return jsonify(delete_faculty(faculty_id))

@students_api.route('/api/schedule', methods=['GET'])
def api_get_schedule():
    return jsonify(get_schedule())

@students_api.route('/api/schedule/<schedule_id>', methods=['GET'])
def api_get_schedule_by_id(schedule_id):
    return jsonify(get_schedule_by_id(schedule_id))

@students_api.route('/api/schedule/add', methods=['POST'])
def api_add_schedule():
    schedule = request.get_json()
    return jsonify(insert_schedule(schedule))

@students_api.route('/api/schedule/update', methods=['PUT'])
def api_update_schedule():
    schedule = request.get_json()
    return jsonify(update_schedule(schedule))

@students_api.route('/api/schedule/update/<schedule_id>', methods=['PUT'])
def api_update_by_id_schedule(schedule_id):
    schedule = request.get_json()
    return jsonify(update_schedule_by_id(schedule_id, schedule))

@students_api.route('/api/schedule/delete/<schedule_id>', methods=['DELETE'])
def api_delete_schedule(schedule_id):
    return jsonify(delete_schedule(schedule_id))


@students_api.route('/api/checkin/<int:student>/<int:meeting>', methods=['POST'])
def api_checkin(student, meeting):
    data = request.json
    student = str(student).zfill(7)
    attendance_date = datetime.now().strftime('%Y-%m-%d')
    attendance_time = datetime.now().strftime('%H:%M:%S')
    status = data.get('status')
    question = data.get('question')
    answer = data.get('answer')
    reason = data.get('reason')

    # Check if the student exists
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()
    student_query = c.execute('SELECT * FROM Students WHERE Studentnumber LIKE ? OR Studentnumber LIKE ?', (f'{str(student)}%', f'0{str(student)}%'))
    student_data = student_query.fetchone()
    if not student_data:
        conn.close()
        return jsonify({'error': f'Student {student} niet gevonden'}), 404

    meeting_query = c.execute('SELECT * FROM Meeting WHERE Meeting_id = ? AND Meeting_date = ?', (meeting, attendance_date))
    meeting_data = meeting_query.fetchone()
    

    if not meeting_data:
        conn.close()
        return jsonify({'error': f'Meeting {meeting} voor vandaag is niet gevonden'}), 404

    if meeting_data[11] != 'open' and meeting_data[11] != 'closed':
        conn.close()
        return jsonify({'error': f'Meeting {meeting} is niet open of gesloten'}), 403

    if meeting_data[11] == 'closed':
        conn.close()
        print(meeting_data[11])
        return jsonify({'error': f'Check-in voor meeting {meeting} is gesloten'}), 403
    
     # Extract the meeting time from the database
    meeting_time = meeting_data[3] 
    current_time = datetime.now(amsterdam_tz).strftime('%H:%M')

    # Check if the current time is between 10 minutes before and 20 minutes after the meeting time
    checkin_open = datetime.strptime(current_time, '%H:%M') >= datetime.strptime(meeting_time, '%H:%M') - timedelta(minutes=10) \
                and datetime.strptime(current_time, '%H:%M') <= datetime.strptime(meeting_time, '%H:%M') + timedelta(minutes=20)

    if checkin_open:
        # Check if student is already checked in
        attendance_query = c.execute('SELECT * FROM Attendance WHERE Studentnumber LIKE ? AND Meeting_id = ?', (str(student), meeting))
        attendance_data = attendance_query.fetchone()
        if attendance_data:
            conn.close()
            return jsonify({'error': f'Student {student} is al ingecheckt voor meeting {meeting}'}), 400

        # Add the attendance record
        c.execute('INSERT INTO Attendance (Student_id, Studentnumber, Meeting_id, Attendance_date, Attendance_time, Status, Question, Answer, Reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (student_data[0], student, meeting, attendance_date, attendance_time, status, question, answer, reason,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Student {student} is succesvol ingecheckt voor meeting {meeting}'}), 200
    else:
        conn.close()
        return jsonify({'error': f'Check-in voor meeting {meeting} is nog niet geopend'}), 403



@students_api.route('/api/questions/random', methods=['GET'])
def get_random_question():
    questions = ['Wat is de hoofdstad van Frankrijk?', 'Hoe heet Adriaan zijn compagnon?"', 'Wat is de hoogste berg ter wereld?', 'Wat is de hoofstad van Nederland?']
    question = random.choice(questions)
    return jsonify({'question': question})

@students_api.route('/api/attendance/v2', methods=['GET'])
def get_attendance_v2():
    # Get the meeting_id from the query parameters
    meeting_id = request.args.get('meeting_id')

    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    cursor = conn.cursor()

    # Retrieve attendance records from the database for the current meeting_id
    cursor.execute('SELECT Students.student_name, Students.studentnumber, Attendance.Attendance_date, Attendance.Attendance_time, Attendance.Status, Attendance.Meeting_id, Students.class_id FROM Students INNER JOIN Attendance ON Students.Student_id=Attendance.Student_id WHERE Attendance.Meeting_id = ?', (meeting_id,))
    rows = cursor.fetchall()

    # Convert the records into a list of dictionaries
    attendance = []
    for row in rows:
        attendance.append({
            'student_name': row[0],
            'studentnumber': row[1],
            'date': row[2],
            'time': row[3],
            'status': row[4],
            'Meeting_id':row[5],
            'class_id': row[6]
        })
    conn.close()

    return jsonify({'attendance': attendance})

@students_api.route('/api/average_attendance', methods=['GET'])
def get_average_attendance():
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    cursor = conn.cursor()

    # Retrieve attendance records from the database
    cursor.execute('SELECT Attendance.Meeting_id, Attendance.Status, Students.class_id FROM Students INNER JOIN Attendance ON Students.Student_id=Attendance.Student_id WHERE Attendance.Meeting_id IN (SELECT DISTINCT Meeting_id FROM Attendance ORDER BY Attendance_date DESC LIMIT 10)')
    rows = cursor.fetchall()

    # Calculate attendance counts by meeting_id and class_id
    meeting_attendance = {}  # dictionary to store attendance counts by meeting_id
    class_sizes = {}  # dictionary to store class sizes by class_id
    for row in rows:
        status = row[1]
        meeting_id = row[0]
        class_id = row[2]
        
        # Update attendance count for this meeting_id
        if meeting_id in meeting_attendance:
            meeting_attendance[meeting_id]['total'] += 1
            if status == 'Aanwezig':
                meeting_attendance[meeting_id]['attended'] += 1
        else:
            meeting_attendance[meeting_id] = {
                'total': 1,
                'attended': 1 if status == 'Aanwezig' else 0
            }
        
        # Update class size for this class_id
        if class_id in class_sizes:
            class_sizes[class_id] += 1
        else:
            class_sizes[class_id] = 1
    
    # Calculate average attendance by meeting_id
    average_attendance = {}
    for meeting_id, counts in meeting_attendance.items():
        total_attendance = counts['total']
        attended_attendance = counts['attended']
        average_attendance[meeting_id] = attended_attendance / total_attendance
    
    # Get class sizes
    cursor = conn.cursor()
    cursor.execute('SELECT class_id, COUNT(*) FROM Students GROUP BY class_id')
    rows = cursor.fetchall()
    for row in rows:
        class_id = row[0]
        size = row[1]
        class_sizes[class_id] = size
    
    conn.close()
    
    # Convert dictionaries to arrays for use by Charts.JS
    meeting_data = []
    for meeting_id, avg_attendance in average_attendance.items():
        meeting_data.append({
            'meeting_id': meeting_id,
            'avg_attendance': avg_attendance
        })
    
    class_data = []
    for class_id, size in class_sizes.items():
        class_data.append({
            'class_id': class_id,
            'size': size
        })
    
    return jsonify({
        'meeting_data': meeting_data,
        'class_data': class_data
    })


@students_api.route('/api/attendance', methods=['GET'])
def get_attendance():
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    cursor = conn.cursor()

    # Retrieve attendance records from the database
    cursor.execute('SELECT Students.student_name, Students.studentnumber, Attendance.Attendance_date, Attendance.Attendance_time, Attendance.Status, Attendance.Meeting_id, Students.class_id, Attendance.question, Attendance.answer, Attendance.reason FROM Students INNER JOIN Attendance ON Students.Student_id=Attendance.Student_id')
    rows = cursor.fetchall()

    # Convert the records into a list of dictionaries
    attendance = []
    for row in rows:
        attendance.append({
            'student_name': row[0],
            'studentnumber': row[1],
            'date': row[2],
            'time': row[3],
            'status': row[4],
            'Meeting_id': row[5],
            'class_id': row[6],
            'question': row[7],
            'answer': row[8],
            'reason': row[9]
        })
    conn.close()

    return jsonify({'attendance': attendance})


@students_api.route('/api/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Delete the attendance record with the given attendance_id
    c.execute('DELETE FROM Attendance WHERE Attendance_id = ?', (attendance_id,))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': f'Attendance record with id {attendance_id} deleted successfully.'})

@students_api.route('/api/attendance/all', methods=['DELETE'])
def delete_all_attendance():
    # Get the range of attendance IDs to delete from the request body
    data = request.json
    start_id = data.get('start_id')
    end_id = data.get('end_id')
    
    if not start_id or not end_id:
        return jsonify({'error': 'Start and end IDs not provided in request body.'}), 400

    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Delete the attendance records with the given range of IDs
    c.execute('DELETE FROM Attendance WHERE Attendance_id >= ? AND Attendance_id <= ?', (start_id, end_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': f'Attendance records with IDs between {start_id} and {end_id} deleted successfully.'})


@students_api.route('/api/create_meeting', methods=['POST'])
def create_meeting():
    if 'teacher_logged_in' in session:
        print(session)
        # Parse the request data
        data = request.json
        meeting_title = data.get('title')
        meeting_date = data.get('date')
        meeting_time = data.get('time')
        meeting_duration = data.get('duration')
        meeting_location = data.get('location')
        meeting_description = data.get('description')
        meeting_question = data.get('question')
        created_by = data.get('created_by')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        class_id = data.get('class_id')
        

        # Connect to the database
        conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
        c = conn.cursor()

        # Add the new meeting to the database
        c.execute('INSERT INTO Meeting (Meeting_title, Meeting_date, Meeting_time, Meeting_duration, Meeting_location, Meeting_description, Class_id, meeting_status, Question) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                        (meeting_title, meeting_date, meeting_time, meeting_duration, meeting_location, meeting_description, class_id, 'open', meeting_question))

        # Retrieve the ID of the newly created meeting
        meeting_id = c.lastrowid

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Return the meeting ID in the response
        return jsonify({'message': 'Meeting created successfully.', 'meeting_id': meeting_id})

@students_api.route('/api/close-meeting/<int:meeting>', methods=['POST'])
def api_close_meeting(meeting):
    # Check if the meeting exists
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()
    attendance_date = datetime.now().strftime('%Y-%m-%d')
    attendance_time = datetime.now().strftime('%H:%M:%S')
    meeting_query = c.execute('SELECT * FROM Meeting WHERE Meeting_id = ?', (meeting,))
    meeting_data = meeting_query.fetchone()
    if not meeting_data:
        conn.close()
        return jsonify({'error': f'Meeting {meeting} not found'}), 404
        # Check-in has closed, get list of all students who have not checked in and are not already marked as absent
    attendance_query = c.execute('SELECT * FROM Attendance WHERE Meeting_id = ?', (meeting,))
    attendance_data = attendance_query.fetchall()
    attendance_students = set(row[1] for row in attendance_data if row[5] != 'Afwezig')
    students_query = c.execute('SELECT * FROM Students WHERE Class_id = ?', (meeting_data[10],))
    students_data = students_query.fetchall()
    
    for student_data in students_data:
        if student_data[5] not in attendance_students:
            # Check if the student is already marked as absent or present
            existing_query = c.execute('SELECT * FROM Attendance WHERE Meeting_id = ? AND Studentnumber = ?', (meeting, student_data[5],))
            existing_data = existing_query.fetchone()
            if not existing_data:
                # Insert new attendance record for this student with status set to 'afwezig'
                c.execute('INSERT INTO Attendance (Studentnumber, Student_id, Meeting_id, Attendance_date, Attendance_time, Status, Question, Answer, Reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (student_data[5], student_data[0], meeting, attendance_date, attendance_time, 'Afwezig', None, None, 'Niet in/uitgecheckt',))

        
    # Update the meeting status to 'closed'
    c.execute('UPDATE Meeting SET meeting_status = ? WHERE Meeting_id = ?', ('closed', meeting))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Meeting {meeting} closed'}), 200


#Delete meeting row
@students_api.route('/api/meetings/<int:meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Delete the meeting with the given meeting_id
    cursor.execute('DELETE FROM Meeting WHERE Meeting_id = ?', (meeting_id,))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': f'Meeting with id {meeting_id} deleted successfully.'})

@students_api.route('/api/meetings/delete_all', methods=['DELETE'])
def delete_all_meetings():
    # Get the range of attendance IDs to delete from the request body
    data = request.json
    start_id = data.get('start_id')
    end_id = data.get('end_id')
    
    if not start_id or not end_id:
        return jsonify({'error': 'Start and end IDs not provided in request body.'}), 400

    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Delete the attendance records with the given range of IDs
    c.execute('DELETE FROM Meeting WHERE Meeting_id >= ? AND Meeting_id <= ?', (start_id, end_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': f'Attendance records with IDs between {start_id} and {end_id} deleted successfully.'})

@students_api.route('/api/students/delete_all', methods=['DELETE'])
def delete_all_students():
    # Get the range of attendance IDs to delete from the request body
    data = request.json
    start_id = data.get('start_id')
    end_id = data.get('end_id')
    
    if not start_id or not end_id:
        return jsonify({'error': 'Start and end IDs not provided in request body.'}), 400

    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Delete the attendance records with the given range of IDs
    c.execute('DELETE FROM Students WHERE Student_id >= ? AND Student_id <= ?', (start_id, end_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': f'Attendance records with IDs between {start_id} and {end_id} deleted successfully.'})


@students_api.route('/api/students/insert', methods=['POST'])
def insert_students():
    
    students = request.get_json()
    if not students:
        return jsonify({'message': 'No data provided'}), 400

    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    for student in students:
        c.execute("INSERT INTO students (class_id, other_details, Studentnumber, Student_name, Username, Password) VALUES (?, ?, ?, ?, ?, ?)",
                       (student['class_id'], student['other_details'], student['Studentnumber'], student['Student_name'], student['Username'], student['Password']))
    conn.commit()
    return jsonify({'message': 'Students inserted successfully'}), 201

@students_api.route('/api/all_meetings', methods=['GET'])
def get_meetings():
    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Get all meetings
    c.execute('SELECT Meeting_id, Meeting_title, Meeting_date, Meeting_time, Meeting_duration, Meeting_location, Meeting_description FROM Meeting ORDER BY Meeting_date ASC, Meeting_time ASC')
    meetings = c.fetchall()

    # Close the database connection
    conn.close()

    # Return the meetings in the response
    return jsonify({'upcoming_meetings': meetings})


@students_api.route('/api/upcoming_meetings', methods=['GET'])
def get_upcoming_meetings():
    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Get the upcoming meetings
    c.execute('SELECT Meeting_id, Meeting_title, Meeting_date, Meeting_time, Meeting_duration, Meeting_location, Meeting_description FROM Meeting WHERE Meeting_date >= ? ORDER BY Meeting_date ASC, Meeting_time ASC',
              (datetime.now().strftime('%Y-%m-%d'),))
    meetings = c.fetchall()

    # Close the database connection
    conn.close()

    # Return the meetings in the response
    return jsonify({'upcoming_meetings': meetings})



def get_meetings():
    meetings = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Meeting")
        rows = cur.fetchall()

        for i in rows:
            meeting = {}
            meeting["Meeting_id"] = i["Meeting_id"]
            meeting["Meeting_title"] = i["Meeting_title"]
            meeting["Meeting_date"] = i["Meeting_date"]
            meeting["Meeting_time"] = i["Meeting_time"]
            meeting["Meeting_duration"] = i["Meeting_duration"]
            meeting["Meeting_location"] = i["Meeting_location"]
            meeting["Meeting_description"] = i["Meeting_description"]
            meeting["Created_by"] = i["Created_by"]
            meeting["Created_at"] = i["Created_at"]
            meeting["Updated_at"] = i["Updated_at"]
            meeting["class_id"] = i["class_id"]
            meetings.append(meeting)
    except:
        meetings = []

    return meetings

@students_api.route('/api/getmeetings', methods=['GET'])
def api_getmeetings():
    return jsonify(get_meetings())

# Admin API - Class
@students_api.route('/api/all_classes', methods=['GET'])
def get_all_classes():
    # Connect to the database
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Get all classes
    c.execute('SELECT class_id, classname FROM Class')
    klassen = c.fetchall()

    # Close the database connection
    conn.close()

    # Return the classes in the response
    return jsonify({'all_classes': klassen})

@students_api.route('/api/add_class', methods=['POST'])
def add_class():
    if 'admin_logged_in' in session:
        print(session)
        # Parse the request data
        data = request.json
        class_name = data.get('classname')
        
        # Connect to the database
        conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
        c = conn.cursor()

        # Add the new class to the database
        c.execute('INSERT INTO Class (classname) VALUES (?)', 
                        (class_name))

        # Retrieve the ID of the newly created meeting
        class_id = c.lastrowid

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Return the class ID in the response
        return jsonify({'message': 'Class created successfully.', 'class_id': class_id})

# def insert_class(klas):
#     inserted_class = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO Class (class_id, classname VALUES (?, ?)", (klas['class_id'], klas['classname']) )
#         conn.commit()
#         inserted_class = get_class_by_id(cur.lastrowid)
#     except:
#         conn().rollback()

#     finally:
#         conn.close()

#     return inserted_class

# def get_class():
#     klas = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM Class")
#         rows = cur.fetchall()

#         # convert row objects to dictionary
#         for i in rows:
#             klas = {}
#             klas["class_id"] = i["class_id"]
#             klas["classname"] = i["classname"]
#             klas.append(klas)

#     except:
#         klas = []

#     return klas


# def get_class_by_id(class_id):
#     klas = {}
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM Class WHERE class_id = ?", 
#                        (class_id,))
#         row = cur.fetchone()

#         # convert row object to dictionary
#         klas["class_id"] = row["class_id"]
#         klas["classname"] = row["classname"]
#     except:
#         klas = {}

#     return klas

# def update_class(klas):
#     updated_class = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         cur.execute("UPDATE Class SET classname = ? WHERE class_id =?",  
#                      (klas["classname"], klas["class_id"],))
#         conn.commit()
#         #return the user
#         updated_class = get_class_by_id(klas["class_id"])

#     except:
#         conn.rollback()
#         updated_class = {}
#     finally:
#         conn.close()

#     return updated_class

# def delete_class(class_id):
#     message = {}
#     try:
#         conn = connect_to_db()
#         conn.execute("DELETE from Class WHERE class_id = ?",     
#                       (class_id,))
#         conn.commit()
#         message["status"] = "User deleted successfully"
#     except:
#         conn.rollback()
#         message["status"] = "Cannot delete user"
#     finally:
#         conn.close()

#     return message

# @students_api.route('/api/class', methods=['GET'])
# def api_get_class():
#     return jsonify(get_class())

# @students_api.route('/api/class/<class_id>', methods=['GET'])
# def api_get_class(class_id):
#     return jsonify(get_class_by_id(class_id))

# @students_api.route('/api/class/add',  methods = ['POST'])
# def api_add_class():
#     klas = request.get_json()
#     return jsonify(insert_class(klas))

# @students_api.route('/api/class/update',  methods = ['PUT'])
# def api_update_class():
#     klas = request.get_json()
#     return jsonify(update_class(klas))

# @students_api.route('/api/class/delete/<class_id>',  methods = ['DELETE'])
# def api_delete_class(class_id):
#     return jsonify(delete_class(class_id))