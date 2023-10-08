The entities that can be identified are:

* Students
* Faculty
* Attendance
* Meeting
* Class

The attributes associated with each entity are:

**Students:**

* student_id
* student_name
* other_details
* Username
* Password
* Studentnumber
* class_id

**Faculty:**

* faculty_id
* faculty_name
* faculty_email
* other_details
* Username
* Password

**Attendance:**

* attendance_id
* enrollment_id
* attendance_date
* attendance_time
* status
* Studentnumber
* Question
* Answer
* Reason
* Student_id
* Meeting_id
* class_id

**Meeting:**

* Meeting_id
* Meeting_title
* Meeting_date
* Meeting_time
* Meeting_duration
* Meeting_location
* Meeting_description
* Created_by
* Created_at
* Updated_at,
* class_id
* meeting_status
* Question

**Class:**

* class_id
* classname

**Courses:**

* course_id
* course_name
* other_details

Relationships:


Each STUDENT can be associated with one and only one CLASS.

Each CLASS may have one or more STUDENTS.

Each STUDENT can have one or more ATTENDANCE records.

Each ATTENDANCE record must be associated with one and only one STUDENT.

Each ATTENDANCE record must be associated with one and only one MEETING.

Each MEETING can have one or more ATTENDANCE records.

Each ATTENDANCE record must be associated with one and only one CLASS.

Each CLASS can have one or more ATTENDANCE records.

Each MEETING must be created by one and only one FACULTY member.

Each FACULTY member can create one or more MEETINGS.

Each MEETING can be associated with one and only one CLASS.

Each CLASS may have one or more MEETINGS.

Each STUDENT can attend one or more MEETINGS.

Each MEETING can have one or more STUDENTS.
