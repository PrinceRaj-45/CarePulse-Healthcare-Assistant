"""
Seed Initial Realistic Demo Data for CarePulse Healthcare System
"""

from datetime import date, timedelta
from database import init_db, get_db_connection, save_emergency_profile

def seed_all_data():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing demo data to avoid duplicates
    cursor.execute("DELETE FROM medicines")
    cursor.execute("DELETE FROM appointments")
    cursor.execute("DELETE FROM vitals")
    cursor.execute("DELETE FROM medication_schedule")
    cursor.execute("DELETE FROM emergency_profile")

    today = date.today()

    # 1. Seed Medicines (Expired, Expiring Soon, Safe, and Low Stock)
    medicines = [
        # Expired (shows red warning badge)
        ("Paracetamol 650", "Dolo-650 (Micro Labs)", "650 mg", "Fever & Pain", (today - timedelta(days=14)).strftime("%Y-%m-%d"), 6, "Take when fever > 100°F"),
        ("Amoxicillin Capsules", "Novamox (Cipla)", "500 mg", "Antibiotic", (today - timedelta(days=45)).strftime("%Y-%m-%d"), 4, "Course finished last month"),
        
        # Expiring Soon (shows yellow warning badge)
        ("Cetirizine Tablets", "Cetzine (Glaxo)", "10 mg", "Allergy & Cold", (today + timedelta(days=12)).strftime("%Y-%m-%d"), 10, "For seasonal allergy/sneezing"),
        ("Cough Relief Syrup", "Benadryl DR (J&J)", "100 ml", "Cough & Cold", (today + timedelta(days=22)).strftime("%Y-%m-%d"), 1, "Low stock bottle"),

        # Safe to Use (shows green badge)
        ("Metformin SR", "Glycomet (USV)", "500 mg", "Diabetes", (today + timedelta(days=240)).strftime("%Y-%m-%d"), 2, "Daily morning & night - Low stock!"),
        ("Telmisartan 40", "Telma-40 (Glenmark)", "40 mg", "Hypertension (BP)", (today + timedelta(days=320)).strftime("%Y-%m-%d"), 28, "Daily post breakfast for Blood Pressure"),
        ("Pantoprazole Gastro", "Pan-40 (Alkem)", "40 mg", "Antacid / Acidity", (today + timedelta(days=180)).strftime("%Y-%m-%d"), 15, "Empty stomach in morning"),
        ("Vitamin D3 Calcirol", "Cadila Healthcare", "60,000 IU", "Vitamins & Calcium", (today + timedelta(days=450)).strftime("%Y-%m-%d"), 8, "Once weekly on Sundays"),
        ("Multivitamin Complex", "Becodex Forte", "1 Capsule", "Supplements", (today + timedelta(days=300)).strftime("%Y-%m-%d"), 30, "Immunity booster")
    ]

    cursor.executemany("""
        INSERT INTO medicines (name, brand_or_mfg, dosage, category, expiry_date, quantity, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, medicines)

    # 2. Seed Doctor Appointments
    appointments = [
        ("Dr. Ananya Sen", "Cardiologist", "City Care Hospital, Sector 14", (today + timedelta(days=3)).strftime("%Y-%m-%d"), "11:00", "Routine 3-month blood pressure and ECG review", "Upcoming"),
        ("Dr. Rajesh Mehta", "Dentist", "Smile Dental Clinic", (today + timedelta(days=9)).strftime("%Y-%m-%d"), "17:30", "Semi-annual dental scaling and cleaning", "Upcoming"),
        ("Dr. Sunita Rao", "Eye Specialist", "Vision Care Center", (today - timedelta(days=5)).strftime("%Y-%m-%d"), "10:15", "Annual vision checkup and new glasses prescription", "Completed")
    ]

    cursor.executemany("""
        INSERT INTO appointments (doctor_name, specialty, hospital_clinic, appointment_date, appointment_time, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, appointments)

    # 3. Seed Medication Schedule Routine
    routine = [
        ("Pantoprazole 40", "1 Tablet", "Morning", "Before Meal (Empty Stomach)", "Daily"),
        ("Telmisartan 40", "1 Tablet", "Morning", "After Breakfast", "Daily"),
        ("Metformin 500", "1 Tablet", "Morning", "With Breakfast", "Daily"),
        ("Multivitamin Complex", "1 Capsule", "Afternoon", "After Lunch", "Daily"),
        ("Metformin 500", "1 Tablet", "Night", "After Dinner", "Daily"),
        ("Atorvastatin 10", "1 Tablet", "Night", "Before Bedtime", "Daily")
    ]

    cursor.executemany("""
        INSERT INTO medication_schedule (medicine_name, dosage, time_slot, meal_relation, days)
        VALUES (?, ?, ?, ?, ?)
    """, routine)

    conn.commit()
    conn.close()

    # 4. Seed Emergency Profile
    save_emergency_profile({
        "patient_name": "Ramesh Kumar Sharma",
        "age": 56,
        "gender": "Male",
        "blood_group": "B+",
        "allergies": "Penicillin (Causes Rashes), Sulfa Antibiotics",
        "chronic_conditions": "Hypertension (High BP) since 2019, Mild Type-2 Diabetes",
        "emergency_contact_name": "Vikram Sharma (Son)",
        "emergency_contact_phone": "+91 98765 43210",
        "emergency_contact_relation": "Son",
        "doctor_name": "Dr. Ananya Sen (Cardiologist & General Physician)",
        "doctor_phone": "+91 91234 56789",
        "hospital_preference": "City Care Multispeciality Hospital, Sector 14"
    })

    print("CarePulse database seeded successfully!")

if __name__ == "__main__":
    seed_all_data()
