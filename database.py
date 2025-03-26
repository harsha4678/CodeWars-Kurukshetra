import sqlite3

# Connect to the database (creates pregnancy.db if not exists)
conn = sqlite3.connect('pregnancy.db')
cur = conn.cursor()

# Create users table
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    password TEXT
)
''')

# Create health_records table (fixed foreign key syntax)
cur.execute('''
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_name TEXT,
    file_path TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Create symptoms table
cur.execute('''
CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symptom TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    advice TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Create exercises table
cur.execute('''
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    reps TEXT NOT NULL
)
''')

# Create pregnancy_records table
cur.execute('''
CREATE TABLE IF NOT EXISTS pregnancy_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_type TEXT NOT NULL,
    input_date TEXT NOT NULL,
    cycle_length INTEGER DEFAULT 28,
    embryo_age INTEGER DEFAULT 0,
    calculated_due_date TEXT NOT NULL
)
''')

# Create appointments table
cur.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    hospital_name TEXT,
    specialization TEXT,
    date TEXT,
    time TEXT,
    status TEXT DEFAULT 'Pending',
    reminder_sent INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Create pregnancy profile table
cur.execute('''
CREATE TABLE IF NOT EXISTS pregnancy_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    due_date TEXT,
    last_menstrual_period TEXT,
    previous_pregnancies INTEGER,
    live_births INTEGER,
    miscarriages INTEGER,
    current_week INTEGER,
    doctor_name TEXT,
    doctor_contact TEXT,
    hospital_name TEXT,
    hospital_contact TEXT,
    blood_type TEXT,
    allergies TEXT,
    medications TEXT,
    pre_existing_conditions TEXT,
    weight REAL,
    height REAL,
    diet TEXT,
    exercise TEXT,
    smoking_status TEXT,
    alcohol_consumption TEXT,
    caffeine_intake TEXT,
    stress_levels TEXT,
    emotional_wellbeing TEXT,
    partner_name TEXT,
    partner_contact TEXT,
    emergency_contact TEXT,
    birth_preferences TEXT,
    additional_notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Create user preferences table
cur.execute('''
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INTEGER PRIMARY KEY,
    dark_mode BOOLEAN DEFAULT FALSE,
    theme_color TEXT DEFAULT 'blue',
    show_nsfw BOOLEAN DEFAULT FALSE,
    language TEXT DEFAULT 'en',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Commit and close connection
conn.commit()
conn.close()

print("Database initialized successfully.")
