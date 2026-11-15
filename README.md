# 🏥 MediCare — Hospital Management System

A full-featured, free Hospital Management System built with **Python (Flask)** + **SQLite**.  
No XAMPP, no MySQL, no cloud signup — runs 100% on your local machine.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## Screenshots

| Dashboard | Patients | Doctors |
|---|---|---|
| Stats, today's appointments, quick actions | Search, register, edit patients | Doctor cards with specialization |

---

## Features

| Module | What you can do |
|---|---|
| 📊 **Dashboard** | Live stats, today's appointments, quick action buttons |
| 👤 **Patients** | Register, search by name, edit, delete — blood group, age, address |
| 🩺 **Doctors** | Add doctors, set specialization, toggle availability |
| 📅 **Appointments** | Book, mark complete/cancel, delete appointments |
| 🏨 **Wards** | Track bed capacity with color-coded progress bars |

---

## Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| Backend | Python 3 + Flask 3 | Free |
| Database | SQLite (file-based) | Free (built into Python) |
| ORM | Flask-SQLAlchemy | Free |
| Frontend | Jinja2 + Plain CSS | Free |
| Font | Inter (Google Fonts) | Free |

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/hospital-mgmt.git
cd hospital-mgmt
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

> **Windows shortcut:** Just double-click `START.bat` — it does steps 4 and 5 automatically.

---

## Project Structure

```
hospital-mgmt/
├── app.py                      # Flask app — models + all routes
├── requirements.txt            # Python dependencies
├── START.bat                   # Windows one-click launcher
├── README.md
├── static/
│   └── css/
│       └── style.css           # All styling (sidebar, cards, tables)
└── templates/
    ├── base.html               # Shared layout (sidebar + topbar)
    ├── index.html              # Dashboard
    ├── patients.html           # Patient list
    ├── patient_form.html       # Register / edit patient
    ├── doctors.html            # Doctor grid
    ├── doctor_form.html        # Add / edit doctor
    ├── appointments.html       # Appointment list
    ├── appointment_form.html   # Book appointment
    ├── wards.html              # Ward grid with capacity bars
    └── ward_form.html          # Add / edit ward
```

> **Note:** The `instance/` folder (containing `hospital.db`) is excluded from Git via `.gitignore`.  
> The database is created automatically when you run the app for the first time.

---

## Demo Data

On first run, the app auto-seeds:
- 4 doctors (Cardiology, Neurology, Pediatrics, Orthopedics)
- 4 wards (General, ICU, Pediatric, Maternity)

---

## Requirements

- Python 3.8 or higher
- pip

```
flask==3.0.3
flask-sqlalchemy==3.1.1
```

---

## License

MIT License — free to use, modify, and distribute.
