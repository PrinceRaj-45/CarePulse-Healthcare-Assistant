# 🏥 CarePulse: Smart Healthcare & Medicine Assistant

**Project Type:** Full-Stack Healthcare Web Application  
**Technologies:** Python 3.12, Flask, SQLite3, HTML5, Vanilla CSS3, JavaScript, Chart.js  
**Project Location:** `C:\healthcare_project`

---

## 📌 Executive Summary
**CarePulse** is a personal healthcare web application engineered to solve real-world everyday medical problems:
1. **Preventing Accidental Consumption of Expired Drugs:** Color-coded automated expiry tracking (🟢 Safe, 🟡 Expiring within 30 days, 🔴 Expired).
2. **Preventing Missed Dosages:** Structured Morning, Afternoon, and Night timetable with one-click "Mark as Taken" tracking.
3. **Doctor Appointments & Checkup Tracking:** Schedule and manage doctor visits, dental checkups, and consultations with dynamic countdowns (Today, Tomorrow, In X days).
4. **Emergency First-Responder Preparedness:** A digital, printable Emergency Medical ID Card displaying Blood Group, Allergies, and Emergency Contacts.

---

## 🏗️ System Architecture & Technology Stack

| Layer | Technology | Key Responsibility in Project |
| :--- | :--- | :--- |
| **Backend Framework** | **Python (Flask)** | Route handlers, business logic, expiry & appointment countdowns, template rendering |
| **Database** | **SQLite3** | Zero-configuration local SQL database (`carepulse.db`) with relational tables for medicines, appointments, routine, and emergency profile |
| **Frontend UI** | **HTML5 & Vanilla CSS3** | Modern medical UI, responsive card grids, badges, glassmorphic header, and modal forms |
| **Client Interactivity** | **JavaScript (ES6)** | Real-time search filtering, auto-dismissing flash alerts, and AJAX dosage toggle |

---

## 📁 Project Structure

```
C:\python mini project\
│
├── app.py                     # Main Flask Application Server
├── database.py                # SQLite database management and queries
├── seed_data.py               # Pre-populates realistic initial medicines, appointments, and profile
├── view_db.py                 # Terminal Database Inspector script
├── carepulse.db               # SQLite database file
├── PROJECT_GUIDE.md           # Complete project documentation & Viva Q&A
│
├── static/
│   ├── css/
│   │   └── style.css          # Master stylesheet (Clean medical theme, responsive)
│   └── js/
│       └── main.js            # Frontend interactive logic & AJAX toggles
│
└── templates/
    ├── base.html              # Base navigation, flash alerts, and layout
    ├── index.html             # Dashboard overview & urgent alerts
    ├── medicines.html         # Medicine cabinet manager & expiry tracker
    ├── appointments.html      # Doctor appointment scheduler & checkup manager
    ├── routine.html           # Daily dosage timetable
    └── emergency.html         # Digital Emergency Medical ID Card
```

---

## 🚀 How to Run the Website

### Method 1: Using Command Prompt (CMD)
1. Open Command Prompt (`Win + R`, type `cmd`, press Enter).
2. Type:
   ```bash
   cd C:\healthcare_project
   python app.py
   ```
3. Open your browser (Chrome, Edge) and go to:
   👉 **`http://127.0.0.1:5000`**

---

## 🎓 Top 10 Viva Questions & Model Answers

### Q1: What real-world problem does CarePulse solve?
**Answer:** It prevents the health hazards of taking expired drugs by automatically calculating expiry status, eliminates missed prescriptions through a daily routine checklist, organizes doctor appointments and checkup schedules with automated countdowns, and provides emergency medical info like allergies and blood group to paramedics.

### Q2: Why did you choose SQLite over other databases like MySQL or MongoDB?
**Answer:** SQLite is serverless, lightweight, requires zero installation, and is natively built into Python. It stores data locally in a single file (`carepulse.db`), making the web application self-contained, portable, and fast.

### Q3: How is the expiry status calculated in the backend?
**Answer:** In `database.py`, we parse the medicine's expiry date using Python's `datetime.strptime()` and subtract today's date (`date.today()`). If `days_left < 0`, it is flagged as **Expired** (🔴); if `0 <= days_left <= 30`, it is marked as **Expiring Soon** (🟡); otherwise, it is **Safe** (🟢).

### Q4: How does the Doctor Appointment Scheduler determine upcoming visits?
**Answer:** In `database.py`, the appointment date is parsed and compared against `date.today()`. If the visit date is today, it displays 'Today!'; if it's tomorrow, it shows 'Tomorrow'; if future, it calculates the remaining days (e.g., 'In 4 days'); and if past, it tags it as 'Passed'. Users can also toggle visits as 'Completed'.

### Q5: How does the "Mark as Taken" button work without refreshing the page?
**Answer:** It uses modern JavaScript `fetch()` (AJAX) to send an asynchronous POST request to `/routine/toggle/<id>`. The backend flips the `is_taken_today` flag in SQLite, and the frontend dynamically updates the button style and strikethrough text instantly.

### Q6: What is Flask and why was it chosen?
**Answer:** Flask is a micro web framework for Python. It provides routing, request handling, and Jinja2 template rendering without unnecessary overhead, making it ideal for high-performance modular web applications.

### Q7: How does the application handle data validation?
**Answer:** On the client side, HTML5 attributes like `required`, `type="date"`, and `min`/`max` enforce valid input. On the server side, Python checks ensure critical fields (such as medicine name and expiry date) are not empty before inserting into SQLite.

### Q8: What happens when the day changes for the daily routine?
**Answer:** The system checks `last_taken_date`. If the current date does not match the recorded date, the application automatically resets the dosage status to pending (`is_taken_today = 0`) for the new day.

### Q9: Can this application run on a mobile device?
**Answer:** Yes! The CSS is built using responsive media queries, CSS Grid, and Flexbox. Any device connected to the local network can access the dashboard by navigating to the host machine's IP address on port 5000.

### Q10: How can this project be scaled further in the future?
**Answer:** Future enhancements can include:
- WhatsApp / SMS dosage reminders using Twilio API.
- OCR barcode / prescription scanner using OpenCV to auto-fill medicine details.
- Telemedicine video consultation link for doctors.
