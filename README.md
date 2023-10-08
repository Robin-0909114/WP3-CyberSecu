# English, scroll down for Dutch

# Introduction
This Attendance Tool is a web-based application designed for keeping track of student attendance in classes, meetings, and events. The tool allows teachers and Study career coaches to easily manage attendance records, track students' participation and engagement.

# Prerequisites
```
Python 3.x
Flask
Flask-Cors
datetime
sqlite3
socket
requests
hashids
icalendar
hashlib
```
# Installation

To install the application, follow these steps:

1. Clone the repository to your local machine:
```
git clone https://github.com/Rac-Software-Development/werkplaats-3-rest-mironi
```

2. Navigate to the repository directory
```
cd werkplaats-3-rest-mironi
```

3. Create and activate virtual environment:
```
python -m venv venv
.\venv\scripts\activate
```

5. Install the necessary dependencies:
```
pip install -r requirements.txt
```

6. Run the application:
```
python app.py
```
# Usage
The Attendance Tool has dedicated routes for both teachers and students. Teachers can manage attendance records, track student participation and engagement, while students can participate in meetings and events.

1. Login
    Go to the login screen of the Attendance Tool.
    Choose whether you are a student or a teacher.

    If you are a student, select "Student" and enter your student number and password.
    If you are a teacher, select "Teacher" and enter your email address and password.

    Click on the "Log in" button.

    If you have entered your details correctly, you will be redirected to your dashboard page. If you encounter any problems logging in, please contact the administrator of the Attendance Tool.

2. Creating a meeting (Teacher)
    To create a meeting, click on the "Sidebar" tab in the navigation menu and select "Creëer een meeting"
    Enter the all the necessary requirements.
    Click the "Create" button to create the Meeting.
    Note that all meetings are created with a start time, the meeting will only be open for students 10 minutes prior the given start time. 

3. Participate in a meeting(Student)
    To participate in a meeting, the student is required to sign in via the route indicated by the teacher's QR-code.
    Once signed in, the student can mark themselves as "Present" or "Absent" and provide additional details such as a response to the meeting question or the reason for their absence. It is important to note that failure to check in or out will result in the student being automatically marked as absent when the meeting concludes.
# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Credits
```
Milan Kreukniet
Robin Winkels
```

# Dutch

# Introductie
Deze Aanwezigheidstool is een webgebaseerde applicatie ontworpen om de aanwezigheid van studenten bij te houden in lessen, meetings en evenementen. De tool maakt het voor docenten en studieloopbaancoaches gemakkelijk om aanwezigheidsrecords te beheren en de deelname en betrokkenheid van studenten bij te houden.

# Vereisten
Controleer voordat u begint of de volgende vereisten zijn geïnstalleerd:
```
Python 3.x
Flask
Flask-Cors
datetime
sqlite3
socket
requests
hashids
icalendar
hashlib
```

# Installatie

Volg deze stappen om de applicatie te installeren:

1. Kloon de repository naar uw lokale computer:
```
git clone https://github.com/Rac-Software-Development/werkplaats-3-rest-mironi
```

2. Navigeer naar de repository-directory
```
cd werkplaats-3-rest-mironi
```

3. Creëer en activeer de virtuele omgeving:
```
python -m venv venv
.\venv\scripts\activate
```

5. Installeer de benodigde onderdelen:
```
pip install -r requirements.txt
```

6. Start de applicatie:
```
python app.py
```

# Gebruikershandleiding

De Attendance Tool heeft toegewijde routes voor zowel docenten als studenten. Docenten kunnen aanwezigheidsregistraties beheren, studentenparticipatie bijhouden en betrokkenheid monitoren, terwijl studenten kunnen deelnemen aan meetings en evenementen.

1. Login

    Ga naar het inlogscherm van de Attendance Tool.
    Kies of je een student of een docent bent.

    Ben je student, kies dan voor "Student" en vul je studentnummer en wachtwoord in.
    Als u een docent bent, selecteert u "Docent" en voert u uw e-mailadres en wachtwoord in.

    Klik op de knop "Inloggen".

    Als u uw gegevens correct heeft ingevuld, wordt u doorgestuurd naar uw dashboardpagina. Mocht je problemen ondervinden bij het inloggen, neem dan contact op met de beheerder van de Attendance Tool.

2. Het aanmaken van een meeting (Docent)
    Om een meeting aan te maken, klik op het "Sidebar" tabblad in het navigatiemenu en selecteer "Creëer een meeting".
    Voer alle benodigde informatie in.
    Klik op de knop "Creëer" om de meeting aan te maken.
    Houd er rekening mee dat alle meetings een starttijd hebben en dat de meeting pas 10 minuten voor aanvang open zal zijn voor studenten.

3. Deelnemen aan een meeting(Student)

    Om deel te nemen aan een meeting moet de student zich aanmelden via de route aangegeven in de QR-code van de docent. Eenmaal aangemeld, kan de student zichzelf aanmerken als "Aanwezig" of "Afwezig" en extra details verstrekken, zoals een reactie op de vraag van de meeting of de reden voor hun afwezigheid. Het is belangrijk op te merken dat als de student zich niet aan- of afmeldt, deze automatisch als afwezig wordt gemarkeerd wanneer de meeting eindigt.

# License
Dit project is gelicentieerd onder de MIT-licentie - zie het LICENSE-bestand voor details.

# Credits
```
Milan Kreukniet
Robin Winkels
```