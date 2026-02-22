"""
Run this once after migrations to set up the database with sample data.
Usage: python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from django.contrib.auth.models import User
from campus.models import Block, Classroom, Department, Faculty, Course, Student

print("🚀 Setting up LPU Campus Management System...")

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@lpu.in', 'admin123')
    print("✅ Admin user created: username=admin, password=admin123")

# Departments
depts = [
    ('Computer Science & Engineering', 'CSE'),
    ('Electronics & Communication', 'ECE'),
    ('Mechanical Engineering', 'ME'),
    ('Business Administration', 'MBA'),
]
dept_objs = []
for name, code in depts:
    d, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
    dept_objs.append(d)
print(f"✅ {len(dept_objs)} Departments created")

# Blocks
blocks_data = [
    ('Block A - Engineering', 'Main engineering block', 4),
    ('Block B - Sciences', 'Science and research block', 3),
    ('Block C - Management', 'Management and commerce block', 5),
    ('Block D - Computing', 'Computer labs and IT block', 4),
]
block_objs = []
for name, desc, floors in blocks_data:
    b, _ = Block.objects.get_or_create(name=name, defaults={'description': desc, 'total_floors': floors})
    block_objs.append(b)
print(f"✅ {len(block_objs)} Blocks created")

# Classrooms
rooms = [
    (block_objs[0], 'A101', 1, 60, 'lecture'),
    (block_objs[0], 'A102', 1, 40, 'tutorial'),
    (block_objs[0], 'A201', 2, 80, 'lecture'),
    (block_objs[1], 'B101', 1, 30, 'lab'),
    (block_objs[1], 'B201', 2, 50, 'seminar'),
    (block_objs[2], 'C101', 1, 100, 'lecture'),
    (block_objs[3], 'D101', 1, 45, 'lab'),
    (block_objs[3], 'D102', 1, 45, 'lab'),
]
room_objs = []
for block, num, floor, cap, rtype in rooms:
    r, _ = Classroom.objects.get_or_create(
        block=block, room_number=num,
        defaults={'floor': floor, 'capacity': cap, 'room_type': rtype}
    )
    room_objs.append(r)
print(f"✅ {len(room_objs)} Classrooms created")

# Faculty
faculty_data = [
    ('Dr. Rajesh Kumar', 'EMP001', dept_objs[0], 'rajesh@lpu.in', 'Professor', 20),
    ('Prof. Priya Singh', 'EMP002', dept_objs[0], 'priya@lpu.in', 'Associate Professor', 18),
    ('Dr. Amit Sharma', 'EMP003', dept_objs[1], 'amit@lpu.in', 'Assistant Professor', 18),
    ('Prof. Neha Gupta', 'EMP004', dept_objs[2], 'neha@lpu.in', 'Assistant Professor', 16),
    ('Dr. Vikram Bose', 'EMP005', dept_objs[3], 'vikram@lpu.in', 'Professor', 20),
]
faculty_objs = []
for name, eid, dept, email, desig, workload in faculty_data:
    f, _ = Faculty.objects.get_or_create(
        employee_id=eid,
        defaults={'name': name, 'department': dept, 'email': email,
                  'designation': desig, 'max_workload_hours': workload}
    )
    faculty_objs.append(f)
print(f"✅ {len(faculty_objs)} Faculty created")

# Courses
courses_data = [
    ('Data Structures & Algorithms', 'CSE301', dept_objs[0], faculty_objs[0], room_objs[0], 4, '3', 55, 60),
    ('Operating Systems', 'CSE401', dept_objs[0], faculty_objs[1], room_objs[2], 3, '4', 48, 80),
    ('Digital Electronics', 'ECE201', dept_objs[1], faculty_objs[2], room_objs[3], 3, '2', 28, 45),
    ('Marketing Management', 'MBA101', dept_objs[3], faculty_objs[3], room_objs[5], 3, '1', 90, 100),
    ('Database Systems', 'CSE501', dept_objs[0], faculty_objs[4], room_objs[6], 4, '5', 40, 45),
    ('Computer Networks', 'CSE601', dept_objs[0], faculty_objs[0], room_objs[1], 3, '6', 35, 40),
]
for cname, code, dept, fac, room, credits, sem, enrolled, maxs in courses_data:
    Course.objects.get_or_create(
        code=code,
        defaults={'name': cname, 'department': dept, 'faculty': fac, 'classroom': room,
                  'credit_hours': credits, 'semester': sem,
                  'enrolled_students': enrolled, 'max_students': maxs}
    )
print(f"✅ {len(courses_data)} Courses created")

# Students
students_data = [
    ('Arjun Verma', '12108001', dept_objs[0], 'arjun@student.lpu.in', '5', 8.4),
    ('Sneha Patel', '12108002', dept_objs[0], 'sneha@student.lpu.in', '5', 9.1),
    ('Rohan Das', '12108003', dept_objs[1], 'rohan@student.lpu.in', '3', 7.8),
    ('Priti Jain', '12108004', dept_objs[3], 'priti@student.lpu.in', '1', 8.0),
    ('Karan Singh', '12108005', dept_objs[0], 'karan@student.lpu.in', '7', 7.2),
    ('Meera Nair', '12108006', dept_objs[2], 'meera@student.lpu.in', '2', 8.9),
]
for sname, reg, dept, email, sem, cgpa in students_data:
    Student.objects.get_or_create(
        registration_number=reg,
        defaults={'name': sname, 'department': dept, 'email': email,
                  'semester': sem, 'cgpa': cgpa}
    )
print(f"✅ {len(students_data)} Students created")

print("\n🎉 Setup complete!")
print("   👉 Run: python manage.py runserver")
print("   👉 Open: http://127.0.0.1:8000")
print("   👉 Login: admin / admin123")
