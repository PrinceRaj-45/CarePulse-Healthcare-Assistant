# 🏥 CarePulse: Smart Healthcare & Medicine Assistant

**CarePulse** is a full-stack personal healthcare web application built with **Python (Flask)** and **SQLite3**, designed to simplify everyday medication management, appointment scheduling, and emergency preparedness.

---

## 🌟 Key Features

1. **💊 Medicine Cabinet & Expiry Tracker:**
   - Real-time color-coded alerts (🟢 Safe, 🟡 Expiring within 30 days, 🔴 Expired).
   - Quantity tracking and instant category/name search.

2. **⏰ Daily Medication Timetable:**
   - Morning, Afternoon, and Night routine slots.
   - One-click "Mark as Taken" tracking using asynchronous AJAX without page reloads.
   - Automated daily reset when a new day begins.

3. **🩺 Doctor Appointments & Checkup Manager:**
   - Schedule consultations, dental checkups, and routine tests.
   - Dynamic countdowns (*Today!*, *Tomorrow*, *In X days*, *Past Visits*).
   - One-click toggle between Upcoming and Completed visits.

4. **🚨 Printable Emergency Medical ID Card:**
   - Quick access to Blood Group, Drug Allergies, Chronic Conditions, and Emergency Contacts.
   - Integrated one-click print feature for physical wallet cards.

---

## 🏗️ Technology Stack

| Component | Technology Used |
| :--- | :--- |
| **Backend** | Python 3.12+, Flask Microframework |
| **Database** | SQLite3 (`carepulse.db`) |
| **Frontend** | HTML5, Vanilla CSS3 (Responsive Grid & Flexbox), Modern JavaScript (ES6) |
| **Architecture** | MVC (Model - View - Controller) |

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.8 or higher installed on your computer.
- Flask installed:
  ```bash
  pip install flask
  ```

### 2. Run the Application
In your terminal / Command Prompt:
```bash
python app.py
```
*(Or double-click `run_website.bat` on Windows)*

### 3. Open in Browser
Visit: 👉 **`http://127.0.0.1:5000`**

---

## 📂 Project Structure

```
├── app.py                     # Main Flask Application Server & Routes
├── database.py                # SQLite database management and queries
├── seed_data.py               # Pre-populates realistic demo medicines & appointments
├── view_db.py                 # Terminal Database Inspector script
├── carepulse.db               # SQLite database file
├── run_website.bat            # 1-click startup script for Windows
├── static/
│   ├── css/style.css          # Medical UI stylesheet (Responsive)
│   └── js/main.js             # Client interactivity & AJAX toggles
└── templates/
    ├── base.html              # Base layout & navigation
    ├── index.html             # Dashboard overview
    ├── medicines.html         # Medicine cabinet manager
    ├── appointments.html      # Doctor appointment scheduler
    ├── routine.html           # Daily routine timetable
    └── emergency.html         # Digital Emergency Medical ID Card
```

