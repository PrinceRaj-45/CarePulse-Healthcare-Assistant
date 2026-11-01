"""
CarePulse: Smart Personal Healthcare & Medicine Assistant
Flask Web Application Server
"""

import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

import database as db

app = Flask(__name__)
app.secret_key = "carepulse-healthcare-super-secret-key-2026"

# Ensure tables exist on startup
db.init_db()


# -------------------------------------------------------------
# 1. DASHBOARD ROUTE
# -------------------------------------------------------------
@app.route("/")
def dashboard():
    stats = db.get_medicine_stats()
    routine = db.get_routine_schedule()
    upcoming_appointments = db.get_upcoming_appointments(limit=4)
    
    # Critical medicine alerts (Expired and Expiring within 30 days)
    all_meds = db.get_all_medicines()
    urgent_alerts = [m for m in all_meds if m["status"] in ("expired", "expiring_soon")][:5]
    
    emergency_profile = db.get_emergency_profile()

    return render_template(
        "index.html",
        stats=stats,
        routine=routine,
        upcoming_appointments=upcoming_appointments,
        urgent_alerts=urgent_alerts,
        emergency_profile=emergency_profile,
        today_date=date.today().strftime("%A, %d %B %Y")
    )


# -------------------------------------------------------------
# 2. MEDICINE CABINET ROUTES
# -------------------------------------------------------------
@app.route("/medicines")
def medicines():
    search = request.args.get("search", "").strip()
    filter_status = request.args.get("status", "all")
    
    meds = db.get_all_medicines(search_query=search, filter_status=filter_status)
    stats = db.get_medicine_stats()

    return render_template(
        "medicines.html",
        medicines=meds,
        stats=stats,
        search=search,
        filter_status=filter_status
    )


@app.route("/medicines/add", methods=["POST"])
def add_medicine_route():
    name = request.form.get("name", "").strip()
    brand = request.form.get("brand_or_mfg", "").strip()
    dosage = request.form.get("dosage", "").strip()
    category = request.form.get("category", "General").strip()
    expiry_date = request.form.get("expiry_date", "").strip()
    quantity = int(request.form.get("quantity", 1) or 1)
    notes = request.form.get("notes", "").strip()

    if not name or not expiry_date:
        flash("Please enter both medicine name and expiry date.", "danger")
        return redirect(url_for("medicines"))

    db.add_medicine(name, brand, dosage, category, expiry_date, quantity, notes)
    flash(f"Medicine '{name}' successfully added to cabinet!", "success")
    return redirect(url_for("medicines"))


@app.route("/medicines/delete/<int:med_id>", methods=["POST"])
def delete_medicine_route(med_id):
    db.delete_medicine(med_id)
    flash("Medicine removed from cabinet.", "info")
    return redirect(url_for("medicines"))


# -------------------------------------------------------------
# 3. DOCTOR APPOINTMENTS ROUTES
# -------------------------------------------------------------
@app.route("/appointments")
def appointments():
    filter_status = request.args.get("status", "all")
    appts = db.get_all_appointments(filter_status=filter_status)
    today_str = date.today().strftime("%Y-%m-%d")

    return render_template(
        "appointments.html",
        appointments=appts,
        filter_status=filter_status,
        today_date=today_str
    )


@app.route("/appointments/add", methods=["POST"])
def add_appointment_route():
    doctor_name = request.form.get("doctor_name", "").strip()
    specialty = request.form.get("specialty", "General Physician").strip()
    hospital_clinic = request.form.get("hospital_clinic", "").strip()
    appointment_date = request.form.get("appointment_date", "").strip()
    appointment_time = request.form.get("appointment_time", "").strip()
    reason = request.form.get("reason", "").strip()

    if not doctor_name or not appointment_date:
        flash("Please provide doctor name and appointment date.", "danger")
        return redirect(url_for("appointments"))

    db.add_appointment(doctor_name, specialty, hospital_clinic, appointment_date, appointment_time, reason)
    flash(f"Appointment with {doctor_name} scheduled successfully!", "success")
    return redirect(url_for("appointments"))


@app.route("/appointments/toggle/<int:app_id>", methods=["POST"])
def toggle_appointment_route(app_id):
    db.toggle_appointment_status(app_id)
    flash("Appointment status updated.", "info")
    return redirect(request.referrer or url_for("appointments"))


@app.route("/appointments/delete/<int:app_id>", methods=["POST"])
def delete_appointment_route(app_id):
    db.delete_appointment(app_id)
    flash("Appointment removed from schedule.", "info")
    return redirect(request.referrer or url_for("appointments"))


@app.route("/vitals")
def vitals():
    """Redirect legacy vitals route to appointments."""
    return redirect(url_for("appointments"))


# -------------------------------------------------------------
# 4. MEDICATION ROUTINE SCHEDULE
# -------------------------------------------------------------
@app.route("/routine")
def routine():
    grouped_schedule = db.get_routine_schedule()
    return render_template("routine.html", schedule=grouped_schedule)


@app.route("/routine/toggle/<int:item_id>", methods=["POST"])
def toggle_routine_item(item_id):
    db.toggle_schedule_taken(item_id)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True})
    return redirect(request.referrer or url_for("routine"))


@app.route("/routine/add", methods=["POST"])
def add_routine_item():
    medicine_name = request.form.get("medicine_name", "").strip()
    dosage = request.form.get("dosage", "").strip()
    time_slot = request.form.get("time_slot", "Morning")
    meal_relation = request.form.get("meal_relation", "After Meal")
    days = request.form.get("days", "Daily")

    if medicine_name:
        db.add_schedule_item(medicine_name, dosage, time_slot, meal_relation, days)
        flash(f"'{medicine_name}' added to {time_slot} routine!", "success")
    return redirect(url_for("routine"))


@app.route("/routine/delete/<int:item_id>", methods=["POST"])
def delete_routine_item(item_id):
    db.delete_schedule_item(item_id)
    flash("Medicine removed from daily routine.", "info")
    return redirect(url_for("routine"))


# -------------------------------------------------------------
# 5. EMERGENCY PROFILE
# -------------------------------------------------------------
@app.route("/emergency")
def emergency():
    profile = db.get_emergency_profile()
    return render_template("emergency.html", profile=profile)


@app.route("/emergency/update", methods=["POST"])
def update_emergency():
    data = {
        "patient_name": request.form.get("patient_name", "").strip(),
        "age": int(request.form.get("age", 0) or 0),
        "gender": request.form.get("gender", ""),
        "blood_group": request.form.get("blood_group", ""),
        "allergies": request.form.get("allergies", "").strip(),
        "chronic_conditions": request.form.get("chronic_conditions", "").strip(),
        "emergency_contact_name": request.form.get("emergency_contact_name", "").strip(),
        "emergency_contact_phone": request.form.get("emergency_contact_phone", "").strip(),
        "emergency_contact_relation": request.form.get("emergency_contact_relation", "").strip(),
        "doctor_name": request.form.get("doctor_name", "").strip(),
        "doctor_phone": request.form.get("doctor_phone", "").strip(),
        "hospital_preference": request.form.get("hospital_preference", "").strip()
    }
    db.save_emergency_profile(data)
    flash("Emergency Medical Profile updated successfully!", "success")
    return redirect(url_for("emergency"))


if __name__ == "__main__":
    print("==================================================")
    print(" CarePulse Healthcare Assistant is running!")
    print(" Open your browser at: http://127.0.0.1:5000")
    print("==================================================")
    app.run(debug=True, port=5000)
