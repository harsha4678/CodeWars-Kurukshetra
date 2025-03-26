from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Secret key for session management
app.secret_key = "my_super_secret_key_123"

# Database file
DATABASE = 'pregnancy.db'

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Makes fetching data easier
    return conn

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, phone, password) VALUES (?, ?, ?)", (name, phone, password))
        conn.commit()
        conn.close()
        
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE phone=? AND password=?", (phone, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!")
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['name'])

# Upload Health Record
@app.route('/upload_record', methods=['GET', 'POST'])
def upload_record():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO health_records (user_id, file_name) VALUES (?, ?)", (session['user_id'], filename))
            conn.commit()
            conn.close()
            
            flash("File uploaded successfully!")
            return redirect(url_for('records'))
    return render_template('upload_record.html')

# View Records
@app.route('/records')
def records():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM health_records WHERE user_id=?", (session['user_id'],))
    records = cur.fetchall()
    conn.close()

    return render_template('records.html', records=records)

# Symptom Checker
@app.route('/symptom_checker', methods=['GET', 'POST'])
def symptom_checker():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    advice = None
    if request.method == 'POST':
        symptom = request.form['symptom']
        advice = "Drink plenty of water and rest."

        if 'nausea' in symptom.lower():
            advice = "Eat small frequent meals, avoid spicy foods."
        elif 'headache' in symptom.lower():
            advice = "Stay hydrated and avoid stress."

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO symptoms (user_id, symptom, advice) VALUES (?, ?, ?)", (session['user_id'], symptom, advice))
        conn.commit()
        conn.close()
    
    return render_template('symptom_checker.html', advice=advice)

# Diet Plan Route
@app.route('/diet_plan')
def diet_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    sample_diet = {
        "Breakfast": "Oats with fruits and milk",
        "Lunch": "Rice, Dal, Vegetables, Curd",
        "Dinner": "Whole wheat roti, Green leafy curry, Soup"
    }

    return render_template('diet_plan.html', diet=sample_diet)

# Book Appointment
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        doctor_name = request.form['doctor']
        date = request.form['date']
        time = request.form['time']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO appointments (user_id, doctor_name, date, time) VALUES (?, ?, ?, ?)", (session['user_id'], doctor_name, date, time))
        conn.commit()
        conn.close()
        
        flash("Appointment booked successfully!")
        return redirect(url_for('appointments'))
    
    return render_template('book_appointment.html')

# View Appointments
@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments WHERE user_id=?", (session['user_id'],))
    appointments = cur.fetchall()
    conn.close()
    
    return render_template('appointments.html', appointments=appointments)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
