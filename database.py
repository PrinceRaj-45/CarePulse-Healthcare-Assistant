"""
Database Management Module for CarePulse Healthcare Assistant
Uses SQLite (embedded, zero-configuration SQL database)
"""

import os
import sqlite3
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carepulse.db")


def get_db_connection():
    """Returns a SQLite connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Medicines Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand_or_mfg TEXT,
            dosage TEXT,
            category TEXT,
            expiry_date TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Appointments Table (Doctor Visits & Checkups)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT NOT NULL,
            specialty TEXT,
            hospital_clinic TEXT,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Vitals History Table (Preserved)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            systolic INTEGER,
            diastolic INTEGER,
            blood_sugar REAL,
            sugar_type TEXT,
            heart_rate INTEGER,
            weight REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Daily Medication Schedule Routine Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medication_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            dosage TEXT,
            time_slot TEXT NOT NULL,  -- Morning, Afternoon, Night
            meal_relation TEXT,       -- Before Meal, After Meal, With Meal
            days TEXT DEFAULT 'Daily',
            is_taken_today INTEGER DEFAULT 0,
            last_taken_date TEXT
        )
    """)

    # 4. Emergency Profile Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_profile (
            id INTEGER PRIMARY KEY,
            patient_name TEXT,
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            allergies TEXT,
            chronic_conditions TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            emergency_contact_relation TEXT,
            doctor_name TEXT,
            doctor_phone TEXT,
            hospital_preference TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------------------------------
# MEDICINES QUERIES & EXPIRY CALCULATION
# -----------------------------------------------------------------
def calculate_expiry_status(expiry_date_str):
    """
    Calculates whether a medicine is:
    - 'expired' (Today > expiry_date)
    - 'expiring_soon' (Within 30 days)
    - 'safe' (> 30 days remaining)
    """
    try:
        exp_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        today = date.today()
        days_left = (exp_date - today).days

        if days_left < 0:
            return "expired", days_left, f"Expired {abs(days_left)} days ago"
        elif days_left <= 30:
            return "expiring_soon", days_left, f"Expiring in {days_left} days"
        else:
            return "safe", days_left, f"{days_left} days remaining"
    except Exception:
        return "unknown", 0, "Invalid Date"


def get_all_medicines(search_query="", filter_status="all"):
    """Fetches all medicines with real-time calculated expiry statuses."""
    conn = get_db_connection()
    query = "SELECT * FROM medicines WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE ? OR category LIKE ? OR brand_or_mfg LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY expiry_date ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    medicines = []
    for r in rows:
        med = dict(r)
        status, days_left, status_text = calculate_expiry_status(med["expiry_date"])
        med["status"] = status
        med["days_left"] = days_left
        med["status_text"] = status_text

        if filter_status == "all" or med["status"] == filter_status:
            medicines.append(med)

    return medicines


def get_medicine_stats():
    """Summary metrics for the dashboard."""
    all_meds = get_all_medicines()
    total = len(all_meds)
    expired = sum(1 for m in all_meds if m["status"] == "expired")
    expiring_soon = sum(1 for m in all_meds if m["status"] == "expiring_soon")
    safe = sum(1 for m in all_meds if m["status"] == "safe")
    low_stock = sum(1 for m in all_meds if m.get("quantity", 0) <= 2)

    return {
        "total": total,
        "expired": expired,
        "expiring_soon": expiring_soon,
        "safe": safe,
        "low_stock": low_stock
    }


def add_medicine(name, brand, dosage, category, expiry_date, quantity, notes):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO medicines (name, brand_or_mfg, dosage, category, expiry_date, quantity, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, brand, dosage, category, expiry_date, quantity, notes))
    conn.commit()
    conn.close()


def delete_medicine(med_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()


# -----------------------------------------------------------------
# DOCTOR APPOINTMENTS QUERIES
# -----------------------------------------------------------------
def add_appointment(doctor_name, specialty, hospital_clinic, appointment_date, appointment_time, reason):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO appointments (doctor_name, specialty, hospital_clinic, appointment_date, appointment_time, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Upcoming')
    """, (doctor_name, specialty, hospital_clinic, appointment_date, appointment_time, reason))
    conn.commit()
    conn.close()


def get_all_appointments(filter_status="all"):
    """Fetches all appointments with dynamic timing status (Today, Upcoming, Passed)."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM appointments ORDER BY appointment_date ASC, appointment_time ASC").fetchall()
    conn.close()

    today = date.today()
    appointments = []

    for r in rows:
        appt = dict(r)
        try:
            appt_date = datetime.strptime(appt["appointment_date"], "%Y-%m-%d").date()
            delta = (appt_date - today).days

            if appt["status"] == "Completed":
                appt["computed_status"] = "Completed"
                appt["timing_text"] = "Completed"
            elif delta < 0:
                appt["computed_status"] = "Passed"
                appt["timing_text"] = f"Passed {abs(delta)} day{'s' if abs(delta) > 1 else ''} ago"
            elif delta == 0:
                appt["computed_status"] = "Today"
                appt["timing_text"] = "Today!"
            elif delta == 1:
                appt["computed_status"] = "Upcoming"
                appt["timing_text"] = "Tomorrow"
            else:
                appt["computed_status"] = "Upcoming"
                appt["timing_text"] = f"In {delta} days"
        except Exception:
            appt["computed_status"] = appt["status"]
            appt["timing_text"] = appt["status"]

        if filter_status == "all" or appt["computed_status"].lower() == filter_status.lower():
            appointments.append(appt)

    return appointments


def get_upcoming_appointments(limit=4):
    """Fetches immediate upcoming doctor visits for the dashboard."""
    all_appts = get_all_appointments(filter_status="all")
    # Priority: Today and Upcoming first
    active_appts = [a for a in all_appts if a["computed_status"] in ("Today", "Upcoming")]
    return active_appts[:limit]


def toggle_appointment_status(app_id):
    """Toggles appointment between Upcoming and Completed."""
    conn = get_db_connection()
    current = conn.execute("SELECT status FROM appointments WHERE id = ?", (app_id,)).fetchone()
    if current:
        new_status = "Upcoming" if current["status"] == "Completed" else "Completed"
        conn.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, app_id))
        conn.commit()
    conn.close()


def delete_appointment(app_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM appointments WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


# -----------------------------------------------------------------
# VITALS QUERIES
# -----------------------------------------------------------------
def add_vital(v_date, v_time, systolic, diastolic, blood_sugar, sugar_type, heart_rate, weight, notes):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO vitals (date, time, systolic, diastolic, blood_sugar, sugar_type, heart_rate, weight, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (v_date, v_time, systolic, diastolic, blood_sugar, sugar_type, heart_rate, weight, notes))
    conn.commit()
    conn.close()


def get_all_vitals(limit=30):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM vitals ORDER BY date DESC, time DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_vitals_chart_data():
    """Returns chronological vitals formatted for Chart.js rendering."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM vitals ORDER BY date ASC, time ASC LIMIT 15").fetchall()
    conn.close()

    labels = []
    systolic_data = []
    diastolic_data = []
    sugar_data = []
    pulse_data = []

    for r in rows:
        labels.append(f"{r['date'][5:]} ({r['time']})")
        systolic_data.append(r["systolic"] if r["systolic"] else None)
        diastolic_data.append(r["diastolic"] if r["diastolic"] else None)
        sugar_data.append(r["blood_sugar"] if r["blood_sugar"] else None)
        pulse_data.append(r["heart_rate"] if r["heart_rate"] else None)

    return {
        "labels": labels,
        "systolic": systolic_data,
        "diastolic": diastolic_data,
        "blood_sugar": sugar_data,
        "heart_rate": pulse_data
    }


def delete_vital(v_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM vitals WHERE id = ?", (v_id,))
    conn.commit()
    conn.close()


# -----------------------------------------------------------------
# MEDICATION ROUTINE SCHEDULE
# -----------------------------------------------------------------
def get_routine_schedule():
    conn = get_db_connection()
    today_str = date.today().strftime("%Y-%m-%d")

    # If day changed, reset is_taken_today
    conn.execute("""
        UPDATE medication_schedule 
        SET is_taken_today = 0 
        WHERE last_taken_date IS NOT NULL AND last_taken_date != ?
    """, (today_str,))
    conn.commit()

    rows = conn.execute("SELECT * FROM medication_schedule ORDER BY time_slot, medicine_name").fetchall()
    conn.close()

    grouped = {"Morning": [], "Afternoon": [], "Night": []}
    for r in rows:
        item = dict(r)
        slot = item.get("time_slot", "Morning")
        if slot in grouped:
            grouped[slot].append(item)
        else:
            grouped["Morning"].append(item)

    return grouped


def toggle_schedule_taken(item_id):
    conn = get_db_connection()
    row = conn.execute("SELECT is_taken_today FROM medication_schedule WHERE id = ?", (item_id,)).fetchone()
    if row:
        new_val = 0 if row["is_taken_today"] == 1 else 1
        today_str = date.today().strftime("%Y-%m-%d") if new_val == 1 else None
        conn.execute("UPDATE medication_schedule SET is_taken_today = ?, last_taken_date = ? WHERE id = ?", (new_val, today_str, item_id))
        conn.commit()
    conn.close()


def add_schedule_item(medicine_name, dosage, time_slot, meal_relation, days):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO medication_schedule (medicine_name, dosage, time_slot, meal_relation, days)
        VALUES (?, ?, ?, ?, ?)
    """, (medicine_name, dosage, time_slot, meal_relation, days))
    conn.commit()
    conn.close()


def delete_schedule_item(item_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM medication_schedule WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# -----------------------------------------------------------------
# EMERGENCY PROFILE
# -----------------------------------------------------------------
def get_emergency_profile():
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM emergency_profile WHERE id = 1").fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "patient_name": "Demo Patient",
        "age": 52,
        "gender": "Male",
        "blood_group": "B+",
        "allergies": "Penicillin, Sulfa drugs",
        "chronic_conditions": "Hypertension (High BP), Type-2 Diabetes",
        "emergency_contact_name": "Amit Sharma",
        "emergency_contact_phone": "+91 98765 43210",
        "emergency_contact_relation": "Son",
        "doctor_name": "Dr. Rajesh Gupta (Cardiologist)",
        "doctor_phone": "+91 91234 56789",
        "hospital_preference": "Apollo Multispeciality Hospital"
    }


def save_emergency_profile(data):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO emergency_profile (id, patient_name, age, gender, blood_group, allergies, chronic_conditions,
                                       emergency_contact_name, emergency_contact_phone, emergency_contact_relation,
                                       doctor_name, doctor_phone, hospital_preference)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            patient_name=excluded.patient_name,
            age=excluded.age,
            gender=excluded.gender,
            blood_group=excluded.blood_group,
            allergies=excluded.allergies,
            chronic_conditions=excluded.chronic_conditions,
            emergency_contact_name=excluded.emergency_contact_name,
            emergency_contact_phone=excluded.emergency_contact_phone,
            emergency_contact_relation=excluded.emergency_contact_relation,
            doctor_name=excluded.doctor_name,
            doctor_phone=excluded.doctor_phone,
            hospital_preference=excluded.hospital_preference
    """, (
        data.get("patient_name"), data.get("age"), data.get("gender"), data.get("blood_group"),
        data.get("allergies"), data.get("chronic_conditions"),
        data.get("emergency_contact_name"), data.get("emergency_contact_phone"), data.get("emergency_contact_relation"),
        data.get("doctor_name"), data.get("doctor_phone"), data.get("hospital_preference")
    ))
    conn.commit()
    conn.close()
