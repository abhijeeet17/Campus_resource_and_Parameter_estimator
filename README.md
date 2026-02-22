# 🏫 LPU Smart Campus Management System
**Django-based AI-Enabled Web Application**

---

## 📋 Project Overview
A full-featured campus management system built with Django for Lovely Professional University. It manages blocks, classrooms, departments, faculty, courses, and students — with AI-powered insights on resource utilization and workload distribution.

---

## ⚙️ Setup Instructions (VSCode)

### Step 1 — Open in VSCode
Open the `campus_management` folder in VSCode.

### Step 2 — Create Virtual Environment
Open the **VSCode Terminal** (`Ctrl + backtick`) and run:
```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Load Sample Data
```bash
python setup_data.py
```

### Step 7 — Start the Server
```bash
python manage.py runserver
```

### Step 8 — Open in Browser
Visit: **http://127.0.0.1:8000**

**Login credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🗂️ Project Structure
```
campus_management/
├── campus_project/         # Django project settings
│   ├── settings.py
│   └── urls.py
├── campus/                 # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin config
│   └── templates/campus/  # HTML templates
├── manage.py
├── setup_data.py           # Sample data loader
└── requirements.txt
```

---

## ✨ Features
- 📊 **Dashboard** — Stats, charts, utilization overview
- 🏢 **Campus Blocks** — Manage university buildings
- 🚪 **Classrooms** — Track capacity and availability
- 👨‍🏫 **Faculty** — Workload management with progress bars
- 📚 **Courses** — Enrollment tracking
- 👩‍🎓 **Students** — CGPA and semester tracking
- 🏛️ **Departments** — Overview with faculty/course/student counts
- 🤖 **AI Insights** — Smart alerts on overloaded faculty, full courses, etc.
- 🔐 **Authentication** — Login/logout system

---

## 🛠️ Technologies Used
- **Backend:** Django 4.2, SQLite
- **Frontend:** Bootstrap 5, Chart.js, Bootstrap Icons
- **Language:** Python 3.x
# Campus_management_system
