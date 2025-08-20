Name: Nicolas Urrea
Date: 12/06/2024
Assignment: Assignment 6
Due Date: 12/06/2024
Steps to initialize and launch website: 
    1. Go to directory cd BakingContestApp
    2. Activate virtual environment: 
        python3 -m venv venv
        source venv/bin/activate.csh
    3. Install python packages 
        pip install flask
        pip install pycryptodome
    4. Initialize database and encryption
        python encryption.py
        python init_db.py
    5. Launch flask
        python app.py
    6. Go to website
        http://127.0.0.1:55556
    7. On CS WLAN
        http://linprog2.cs.fsu.edu:55556/
        (I tested this on my laptop on campus and it worked)

Steps to Login
    1. Login information for security level 1
        Username: PDiana
        Password: password1
    2. Login information for security level 2
        Username: TJones
        Password: password2
    3. Login information for security level 3
        Username: KarenWorks
        Password: password3

Website Status:
    Login Page:  Fully functional. Should validate using encrypted cerdentials, tested encryption of name, phone number, and password using SQLite. 
    Home Pages: Fully functional. Based on three different security levels
    Show My Contest Entry Results: Fully functional. Each user loaded with one contest entry at initialization
    Add Contest Entry page: Fully functional. Stores in Database and visible on contest results page.
    Add Contest User: Fully functional. Should have necessary encyrption when stored in database
    List Contested User: Fully functional. Displays decrypted information
    Encryption: The Name, PhNum, and LoginPassword fields are encrypted in the BakingContestPeople table using a cryptographic library (PyCryptodome). 


About this project: This project is a more developed Flask-based web application designed to manage a baking contest. It functions using the above described pages. 
Assumptions: The project assumes that user inputs are generally correct and properly validated, and that the database is pre-populated with contest result entries.
All work below was performed solely by Nicolas Urrea

