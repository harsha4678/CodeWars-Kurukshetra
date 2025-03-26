from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3
import os
from werkzeug.utils import secure_filename
from hospital_utils import get_hospitals

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
    conn.row_factory = sqlite3.Row
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
        if 'file' not in request.files:
            flash("No file part in request.")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("No file selected.")
            return redirect(request.url)

        filename = f"user_{session['user_id']}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO health_records (user_id, file_name, file_path)
            VALUES (?, ?, ?)
        ''', (session['user_id'], filename, filepath))
        conn.commit()
        conn.close()

        flash("File uploaded successfully!")
        return redirect(url_for('records'))

    return render_template('upload_record.html')

# View Records (with download link)
@app.route('/records')
def records():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT file_name, upload_date 
        FROM health_records 
        WHERE user_id=?
    ''', (session['user_id'],))
    records = cur.fetchall()
    conn.close()

    return render_template('records.html', records=records)

# Download File Route
@app.route('/download/<filename>')
def download_file(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT file_path 
        FROM health_records 
        WHERE user_id=? AND file_name=?
    ''', (session['user_id'], filename))
    record = cur.fetchone()
    conn.close()

    if record and os.path.exists(record['file_path']):
        return send_file(record['file_path'], as_attachment=True)
    else:
        flash("File not found or unauthorized.")
        return redirect(url_for('records'))

# Symptom Checker Route (corrected)
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
        cur.execute("INSERT INTO symptoms (user_id, symptom, advice) VALUES (?, ?, ?)", 
                    (session['user_id'], symptom, advice))
        conn.commit()
        conn.close()

    return render_template('symptom_checker.html', advice=advice)

# Diet Plan Route
@app.route('/diet_plan', methods=['GET', 'POST'])
def diet_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Predefined options
    trimesters = ['First Trimester', 'Second Trimester', 'Third Trimester']
    health_conditions = ['None', 'Gestational Diabetes', 'Hypertension', 'Anemia', 'Nausea', 'Constipation']
    diets = ['Vegetarian', 'Vegan', 'Non-Vegetarian']
    cultures = ['Indian', 'Mediterranean', 'Western', 'Asian']

    # Default selected values
    selected_trimester = None
    selected_condition = None
    selected_diet = None
    selected_culture = None
    selected_plan = None

    if request.method == 'POST':
        selected_trimester = request.form['trimester']
        selected_condition = request.form['condition']
        selected_diet = request.form['diet']
        selected_culture = request.form['culture']

        # Generate diet plan based on inputs
        selected_plan = generate_diet_plan(selected_trimester, selected_condition, selected_diet, selected_culture)

    return render_template(
        'diet_plan.html',
        trimesters=trimesters,
        health_conditions=health_conditions,
        diets=diets,
        cultures=cultures,
        selected_plan=selected_plan,
        selected_trimester=selected_trimester,
        selected_condition=selected_condition,
        selected_diet=selected_diet,
        selected_culture=selected_culture
    )

def generate_diet_plan(trimester, condition, diet_type, culture):
    # 🌱 Start with trimester-specific meals (base diet)
    diet = {}

    if trimester == "First Trimester":
        diet = {
            "Breakfast": "Whole grain toast with avocado & boiled egg",
            "Snack": "Ginger tea with crackers",
            "Lunch": "Vegetable soup with whole grain bread",
            "Evening Snack": "Fruit salad with almonds",
            "Dinner": "Light khichdi with mint chutney",
        }
    elif trimester == "Second Trimester":
        diet = {
            "Breakfast": "Oats with chia seeds, banana, and walnuts",
            "Snack": "Greek yogurt with berries",
            "Lunch": "Grilled chicken with quinoa and spinach salad",
            "Evening Snack": "Boiled egg with flaxseed",
            "Dinner": "Palak paneer with brown rice",
        }
    elif trimester == "Third Trimester":
        diet = {
            "Breakfast": "Ragi porridge with dates & almonds",
            "Snack": "Milk with dry fruits",
            "Lunch": "Lentil curry with spinach and brown rice",
            "Evening Snack": "Sesame laddoo with coconut water",
            "Dinner": "Stuffed paratha with vegetable soup",
        }

    # 💉 Layer: Health Condition Adjustments
    if condition == "Gestational Diabetes":
        diet.update({
            "Breakfast": "Oats with chia, flaxseed & cinnamon (low GI)",
            "Snack": "Roasted chickpeas and cucumber sticks",
            "Lunch": "Grilled chicken with quinoa and leafy greens (low GI)",
            "Evening Snack": "Nuts, seeds, and berries (low sugar)",
        })
    elif condition == "Hypertension":
        diet.update({
            "Breakfast": "Banana smoothie with flaxseed",
            "Snack": "Watermelon salad with mint",
            "Lunch": "Grilled salmon with sweet potato & spinach",
            "Evening Snack": "Yogurt with flaxseed",
        })
    elif condition == "Anemia":
        diet.update({
            "Breakfast": "Beetroot and carrot smoothie",
            "Snack": "Dates stuffed with almonds",
            "Lunch": "Spinach dal with brown rice",
            "Evening Snack": "Pomegranate juice",
        })
    elif condition == "Nausea":
        diet.update({
            "Breakfast": "Dry toast with ginger lemon tea",
            "Snack": "Crackers with nut butter",
            "Lunch": "Light vegetable broth with rice crackers",
        })
    elif condition == "Constipation":
        diet.update({
            "Breakfast": "Flaxseed oatmeal with prunes",
            "Snack": "Papaya cubes with lemon",
            "Lunch": "Palak curry with brown rice",
            "Evening Snack": "Chia pudding with mango",
        })

    # 🌿 Layer: Dietary Preference (only apply if needed)
    if diet_type == "Vegetarian":
        diet.update({
            "Lunch": "Palak paneer with quinoa",
            "Dinner": "Rajma curry with brown rice & salad",
        })
    elif diet_type == "Vegan":
        diet.update({
            "Lunch": "Chickpea quinoa salad",
            "Dinner": "Tofu stir fry with millet",
        })
    elif diet_type == "Non-Vegetarian":
        diet.update({
            "Lunch": "Chicken curry with brown rice",
            "Dinner": "Grilled fish with roasted vegetables",
        })

    # 🌎 Layer: Cultural Customization
    if culture == "Indian":
        diet.update({
            "Breakfast": "Poha with peanuts & curry leaves",
            "Lunch": "Dal tadka with roti and vegetable sabzi",
            "Dinner": "Aloo methi with curd and roti",
        })
    elif culture == "Mediterranean":
        diet.update({
            "Breakfast": "Greek yogurt with figs, walnuts & honey",
            "Lunch": "Falafel bowl with hummus & tabbouleh",
            "Dinner": "Grilled eggplant with tahini sauce and couscous",
        })
    elif culture == "Western":
        diet.update({
            "Breakfast": "Scrambled eggs with avocado toast",
            "Lunch": "Chicken Caesar salad",
            "Dinner": "Baked salmon with quinoa and vegetables",
        })
    elif culture == "Asian":
        diet.update({
            "Breakfast": "Rice porridge with vegetables",
            "Lunch": "Stir-fried tofu with vegetables & rice",
            "Dinner": "Miso soup with vegetable sushi (cooked options)",
        })

    # 💧 Final touch: Hydration (always same)
    diet["Hydration"] = "At least 10 glasses of water, including coconut water & herbal teas."

    return diet


# Book Appointment


@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    specializations = [
        "General Physical", "Neurologist", "Dermatologist", "Cardiologist",
        "Orthopedist", "Pediatrician", "Gynecologist", "Psychiatrist",
        "Dentist", "Oncologist", "Endocrinologist", "Ophthalmologist",
        "Urologist", "Gastroenterologist", "Pulmonologist", "ENT",
        "Rheumatologist", "Radiologist", "Nephrologist", "Allergist", "Surgeon"
    ]

    hospitals = []

    if request.method == 'POST':
        specialization = request.form['specialization']
        location = request.form['location']

        # Fetch real hospitals
        result = get_hospitals(location=location, specialization=specialization)
        hospitals = result.get('hospitals', [])
        if 'error' in result:
            flash(result['error'])

        if 'confirm' in request.form:
            hospital_name = request.form['hospital_name']
            date = request.form['date']
            time = request.form['time']

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO appointments (user_id, hospital_name, specialization, date, time)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], hospital_name, specialization, date, time))
            conn.commit()
            conn.close()

            flash(f"Appointment booked at {hospital_name} on {date} at {time}.")
            return redirect(url_for('appointments'))

    return render_template('book_appointment.html', specializations=specializations, hospitals=hospitals)

# View Appointments
@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, hospital_name, specialization, date, time, status 
        FROM appointments 
        WHERE user_id=?
    ''', (session['user_id'],))
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
