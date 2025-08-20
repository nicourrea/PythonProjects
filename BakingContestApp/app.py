from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from encryption import encrypt, decrypt  # Import encryption functions from encryption.py

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('contest.db')
    conn.row_factory = sqlite3.Row  # Allows access by column name
    return conn

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM BakingContestPeople WHERE UserId = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        username = decrypt(user['Name'])  # Decrypt the Name
        security_level = user['SecurityLevel']
        return render_template('home.html', username=username, security_level=security_level)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encrypt input for comparison
        encrypted_username = encrypt(username)
        encrypted_password = encrypt(password)

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM BakingContestPeople WHERE Name = ? AND LoginPassword = ?", 
            (encrypted_username, encrypted_password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['UserId']
            return redirect(url_for('home'))
        else:
            error = "Invalid username and/or password!"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/list')
def list_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM BakingContestPeople").fetchall()
    conn.close()

    # Decrypt sensitive fields before passing to the template
    decrypted_users = [
        {
            "UserId": user["UserId"],
            "Name": decrypt(user["Name"]),
            "Age": user["Age"],
            "PhNum": decrypt(user["PhNum"]),
            "SecurityLevel": user["SecurityLevel"],
            "LoginPassword": decrypt(user["LoginPassword"]),
        }
        for user in users
    ]

    return render_template('list_users.html', users=decrypted_users)

@app.route('/contestResults')
def contest_results():
    conn = get_db_connection()
    entries = conn.execute("SELECT * FROM BakingContestEntry").fetchall()
    conn.close()

    if not entries:
        msg = "No contest entries found!"
        return render_template('contest_results.html', entries=[], msg=msg)

    return render_template('contest_results.html', entries=entries)

@app.route('/addrec')
def add_rec():
    msg = request.args.get('msg', 'No message provided')
    return render_template('result.html', msg=msg)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        security_level = request.form['security_level']
        login_password = request.form['login_password']

        errors = []
        if not name.strip():
            errors.append("You cannot enter an empty name")
        if not phone_number.strip():
            errors.append("You cannot enter an empty phone number")
        if not age.isdigit() or not (0 < int(age) < 121):
            errors.append("The Age must be a whole number between 0 and 121")
        if not security_level.isdigit() or not (1 <= int(security_level) <= 3):
            errors.append("The Security Level must be a numeric value between 1 and 3")
        if not login_password.strip():
            errors.append("You cannot enter an empty password")

        if errors:
            return redirect(url_for('add_rec', msg="<br>".join(errors)))

        # Encrypt sensitive fields
        encrypted_name = encrypt(name)
        encrypted_phone_number = encrypt(phone_number)
        encrypted_login_password = encrypt(login_password)

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO BakingContestPeople (Name, Age, PhNum, SecurityLevel, LoginPassword) VALUES (?, ?, ?, ?, ?)",
            (encrypted_name, age, encrypted_phone_number, security_level, encrypted_login_password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('add_rec', msg="Record successfully added!"))
    return render_template('add_user.html')

@app.route('/myContestResults')
def my_contest_results():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    entries = conn.execute("SELECT * FROM BakingContestEntry WHERE UserId = ?", (user_id,)).fetchall()
    conn.close()
    return render_template('my_contest_results.html', entries=entries)

@app.route('/enterEntry', methods=['GET', 'POST'])
def enter_entry():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name_of_baking_item = request.form['name_of_baking_item']
        num_excellent_votes = request.form['num_excellent_votes']
        num_ok_votes = request.form['num_ok_votes']
        num_bad_votes = request.form['num_bad_votes']

        errors = []
        if not name_of_baking_item.strip():
            errors.append("Name of Baking Item cannot be empty or contain only spaces.")
        if not num_excellent_votes.isdigit() or int(num_excellent_votes) < 0:
            errors.append("Number of Excellent Votes must be a non-negative integer.")
        if not num_ok_votes.isdigit() or int(num_ok_votes) < 0:
            errors.append("Number of OK Votes must be a non-negative integer.")
        if not num_bad_votes.isdigit() or int(num_bad_votes) < 0:
            errors.append("Number of Bad Votes must be a non-negative integer.")

        if errors:
            return render_template('result.html', msg="<br>".join(errors))

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO BakingContestEntry (UserId, NameOfBakingItem, NumExcellentVotes, NumOkVotes, NumBadVotes)
            VALUES (?, ?, ?, ?, ?)
        """, (session['user_id'], name_of_baking_item, num_excellent_votes, num_ok_votes, num_bad_votes))
        conn.commit()
        conn.close()

        return render_template('result.html', msg="Contest entry successfully added!")
    
    return render_template('enter_entry.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=55556)

