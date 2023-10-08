from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import datetime
import sqlite3
import socket
import hashlib

teacher = Blueprint('teacher', __name__)

@teacher.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if 'teacher_logged_in' in session:
        if request.method == 'POST':
            # Get form data
            class_name = request.form['class_name']
            date = request.form['date']
            time = request.form['time']
            location = request.form['location']
            
            # Insert class details into the database
            conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
            c = conn.cursor()
            c.execute('INSERT INTO clas (class_name, date, time, location) VALUES (?, ?, ?, ?)', (class_name, date, time, location))
            conn.commit()
            conn.close()
            
            return redirect(url_for('teacher_dashboard'))
            
        return render_template('teachers/create_class.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

@teacher.route('/view_classes')
def view_classes():
    if 'teacher_logged_in' in session:
        conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Schedule')
        classes = c.fetchall()
        conn.close()
        return render_template('teachers/view_classes2.html', classes=classes)
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

@teacher.route('/aanwezigheid', methods=['GET', 'POST'])
def attendance():
    if 'teacher_logged_in' in session:
        print(session)
        return render_template('teachers/aanwezigheid.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

def generate_hash(meeting_id):
    salt = "your_salt_here"  # Choose a salt for added security
    input_str = f"{meeting_id}{salt}"
    return hashlib.sha256(input_str.encode()).hexdigest()

@teacher.route('/meetings/<string:meeting_hash>')
def meeting(meeting_hash):
    
    conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Fetch the maximum meeting ID from the Meeting table
    c.execute('SELECT MAX(Meeting_id) FROM Meeting')
    max_meeting_id = c.fetchone()[0]
    meeting_id = None
    for potential_id in range(1, max_meeting_id + 1):  # Replace max_meeting_id with the maximum meeting ID in your database
        if generate_hash(potential_id) == meeting_hash:
            meeting_id = potential_id
            break

    if meeting_id is None:
        flash('Invalid meeting ID', 'danger')
        return redirect(url_for('login'))

    if 'teacher_logged_in' in session: 
        hostname = socket.gethostname()

        ip_address = socket.gethostbyname(hostname)
        ip_str = str(ip_address)
        

        # Connect to the database
        conn = sqlite3.connect('Aanmeldingstool/databases/attendence.db')
        c = conn.cursor()

        # Retrieve the meeting with the requested ID from the database
        c.execute('SELECT * FROM Meeting WHERE Meeting_id = ?', (meeting_id,))
        meeting = c.fetchone()
        print(meeting[10])

        # Retrieve the class name using the class_id from the meeting
        c.execute('SELECT classname FROM Class WHERE Class_id = ?', (meeting[10],))
        class_name = c.fetchone()[0]
        # Close the database connection
        
        c.execute('SELECT faculty_name FROM faculty WHERE faculty_email = ?', (session['username'],))
        name = c.fetchone()[0]
        conn.close()
        # Render the meeting template with the meeting data
        return render_template('teachers/meetings.html', meeting=meeting, ip_str=ip_str, meeting_id=meeting_id, class_name=class_name, name=name )
    else:
        flash('Log alstublieft eerst in', 'danger')
    return redirect(url_for('login'))

@teacher.route('/create_meeting')
def make_meeting():
    if 'teacher_logged_in' in session: 
        return render_template('teachers/create_meeting.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
    return redirect(url_for('login'))

@teacher.route('/teacher/upcoming_meetings')
def t_upcoming_meetings():
    if 'teacher_logged_in' in session: 
        return render_template('teachers/teacher_upcoming_meetings.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
    return redirect(url_for('login'))

@teacher.route('/teacher/all_meetings')
def t_all_meetings():
    if 'teacher_logged_in' in session: 
        return render_template('teachers/teacher_all_meetings.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
    return redirect(url_for('login'))