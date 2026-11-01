# 🏥 CarePulse — Smart Healthcare & Medicine Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite3">
  <img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20ES6-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="Frontend">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 📌 Overview

**CarePulse** is a personal full-stack healthcare web application engineered to address real-world everyday medical challenges. It bridges the gap between patient adherence, prescription organization, and emergency preparedness.

Built using an asynchronous **Flask (Python)** backend and a zero-configuration **SQLite3** relational database, CarePulse delivers a responsive, medical-grade user experience without external third-party frontend dependencies.

---

## 🚨 Problems CarePulse Solves

| Challenge | Real-World Danger | CarePulse Solution |
| :--- | :--- | :--- |
| **Expired Medicines** | Consuming degraded drugs can cause toxicity or treatment failure. | **Automated Expiry Engine:** Dynamic date calculation with visual status badges (🟢 Safe, 🟡 Expiring within 30 days, 🔴 Expired). |
| **Missed Dosages** | Skipping prescriptions delays patient recovery and causes complications. | **Daily Timetable Checklist:** Morning, Afternoon, and Night routine tracking with one-click AJAX toggles and automatic day-reset. |
| **Missed Checkups** | Overlooking specialist consultations and routine medical tests. | **Appointment Scheduler:** Intelligent countdown timers (*Today!*, *Tomorrow*, *In X days*) and checkup history tracking. |
| **Emergency Incidents** | Paramedics lack quick access to patient blood type, allergies, and contacts. | **Printable Emergency ID:** A standardized digital medical ID card optimized for wallet printing and one-click contact dialing. |

---

## ✨ Key Features & Modules

### 1. 💊 Smart Medicine Cabinet & Expiry Tracker
* **Real-time Expiry Computation:** Compares expiration dates against `date.today()` on every load.
* **Color-Coded Status Tags:**
  - 🟢 **Safe:** Active medicine with more than 30 days of shelf life.
  - 🟡 **Expiring Soon:** Warning triggered when 30 days or fewer remain.
  - 🔴 **Expired:** Immediate alert badge notifying the user to discard the drug.
* **Instant Filtering:** Real-time client-side search by medicine name, brand/manufacturer, or clinical category.
* **Stock & Dosage Management:** Track unit quantities and dosage instructions.

### 2. ⏰ Daily Medication Schedule & Routine
* **Structured Time Slots:** Segregated into **Morning**, **Afternoon**, and **Night** dosings.
* **Meal Relations:** Specify when to take medicine (*Before Meal / Empty Stomach*, *After Meal*, *With Food*).
* **Asynchronous AJAX Check-Off:** Toggle doses as "Taken" instantly without full page reloads via the Fetch API.
* **Automated Daily Reset:** Detects date transitions and resets doses to pending for the new day.

### 3. 🩺 Doctor Appointments & Checkup Manager
* **Consultation Booking:** Record doctor name, medical specialty, clinic/hospital address, and consultation reasons.
* **Automated Countdowns:** Dynamic relative timing indicators:
  - 🔔 **Today!** — Urgent alert for visits scheduled for today.
  - 🟢 **Tomorrow / In X days** — Proactive reminders.
  - ⏳ **Past Visits** — Keeps an archive of previous consultations.
* **Status Toggles:** Mark visits as *Completed* or reopen them with a single click.

### 4. 🚨 Digital Emergency Medical ID Card
* **Critical Health Demographics:** Prominently displays Blood Group, Age, Gender, and Known Drug Allergies (e.g., Penicillin, Sulfa).
* **Direct Calling:** Click-to-call links (`tel:`) for family emergency contacts and primary physicians.
* **Print-Optimized Layout:** Built with print media queries (`window.print()`) to generate a wallet-sized physical emergency card.

---

## 🏛️ System Architecture

CarePulse follows the **Model-View-Controller (MVC)** architectural design pattern:

```
┌────────────────────────────────────────────────────────┐
│                   Browser / Client                     │
│   (HTML5 Semantic Layout, Responsive CSS3, Modern ES6)  │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP GET / POST (AJAX / JSON)
                           ▼
┌────────────────────────────────────────────────────────┐
│               Flask Web Server (app.py)                │
│    - Route Handlers & REST API Endpoints               │
│    - Input Validation & Flash Messaging                │
│    - Jinja2 Template Rendering Engine                  │
└──────────────────────────┬─────────────────────────────┘
                           │ Python Function Calls
                           ▼
┌────────────────────────────────────────────────────────┐
│            Data Layer (database.py)                    │
│    - SQLite3 Embedded Database Engine (carepulse.db)   │
│    - Expiry & Countdown Date Arithmetic               │
│    - Parameterized SQL Queries (Anti-SQLi)             │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Backend** | Python 3.12+ | Core programming logic and date arithmetic |
| **Framework** | Flask 3.x | Lightweight, high-performance WSGI web application framework |
| **Database** | SQLite3 | Embedded, zero-configuration relational database engine |
| **Frontend UI** | HTML5 & CSS3 | Responsive layouts using Flexbox, CSS Grid, and custom medical design system |
| **Client Scripting** | JavaScript (ES6) | Asynchronous Fetch API, dynamic DOM manipulation, and search filtering |

---

## 📁 Directory Structure

```
CarePulse-Healthcare-Assistant/
├── app.py                     # Main Flask Application Server & Route Controllers
├── database.py                # Database connection, schemas, and SQL queries
├── seed_data.py               # Pre-populates realistic clinical and appointment data
├── view_db.py                 # Command-line database inspector utility
├── carepulse.db               # SQLite database file
├── run_website.bat            # 1-click Windows execution launcher
├── PROJECT_GUIDE.md           # Technical documentation and Viva Q&A
├── README.md                  # Comprehensive project documentation
├── .gitignore                 # Excludes cache and virtual environment files
│
├── static/
│   ├── css/
│   │   └── style.css          # Master stylesheet (Clean medical theme, responsive)
│   └── js/
│       └── main.js            # Frontend interactivity, AJAX toggles & toasts
│
└── templates/
    ├── base.html              # Shared base template with navigation & flash toasts
    ├── index.html             # Unified dashboard overview & critical warnings
    ├── medicines.html         # Medicine cabinet manager & expiry monitor
    ├── appointments.html      # Doctor appointment scheduler & visit history
    ├── routine.html           # Daily medication timetable
    └── emergency.html         # Printable Emergency Medical ID card
```

---

## 🗄️ Database Schema Design

The relational database (`carepulse.db`) consists of 4 primary tables:

1. **`medicines`**
   - `id` (INTEGER, Primary Key, Auto-increment)
   - `name` (TEXT, Drug trade or chemical name)
   - `brand_or_mfg` (TEXT, Pharmaceutical company)
   - `dosage` (TEXT, e.g., 500 mg, 10 ml)
   - `category` (TEXT, e.g., Antibiotic, Diabetes, Supplement)
   - `expiry_date` (TEXT, ISO format YYYY-MM-DD)
   - `quantity` (INTEGER, Unit stock count)
   - `notes` (TEXT, Usage guidelines or precautions)

2. **`appointments`**
   - `id` (INTEGER, Primary Key, Auto-increment)
   - `doctor_name` (TEXT, Physician name)
   - `specialty` (TEXT, Department / field of medicine)
   - `hospital_clinic` (TEXT, Facility location)
   - `appointment_date` (TEXT, YYYY-MM-DD)
   - `appointment_time` (TEXT, HH:MM)
   - `reason` (TEXT, Clinical symptoms or purpose)
   - `status` (TEXT, 'Upcoming' or 'Completed')

3. **`medication_schedule`**
   - `id` (INTEGER, Primary Key, Auto-increment)
   - `medicine_name` (TEXT)
   - `dosage` (TEXT)
   - `time_slot` (TEXT, 'Morning', 'Afternoon', 'Night')
   - `meal_relation` (TEXT, 'Before Meal', 'After Meal', 'With Food')
   - `days` (TEXT, Frequency)
   - `is_taken_today` (INTEGER, 0 for Pending, 1 for Taken)
   - `last_taken_date` (TEXT, YYYY-MM-DD)

4. **`emergency_profile`**
   - `id` (INTEGER, Primary Key)
   - `patient_name`, `age`, `gender`, `blood_group`
   - `allergies`, `chronic_conditions`
   - `emergency_contact_name`, `emergency_contact_phone`, `emergency_contact_relation`
   - `doctor_name`, `doctor_phone`, `hospital_preference`

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher installed on your system.
- Git installed.

### 2. Clone the Repository
```bash
git clone https://github.com/PrinceRaj-45/CarePulse-Healthcare-Assistant.git
cd CarePulse-Healthcare-Assistant
```

### 3. Install Dependencies
```bash
pip install flask
```

### 4. (Optional) Re-seed Demo Data
If you want to reset realistic demo medicines and appointments:
```bash
python seed_data.py
```

### 5. Run the Application
```bash
python app.py
```
*(On Windows, you can alternatively double-click `run_website.bat`)*

### 6. Access the Dashboard
Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🔍 Database Inspection Utility

You can inspect all SQLite tables and records directly inside your terminal without installing database viewers:
```bash
python view_db.py
```

---

## 👨‍💻 Author

**Prince Raj**  
- GitHub: [@PrinceRaj-45](https://github.com/PrinceRaj-45)
- Project Repository: [CarePulse-Healthcare-Assistant](https://github.com/PrinceRaj-45/CarePulse-Healthcare-Assistant)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and adapt it for learning and academic projects.
