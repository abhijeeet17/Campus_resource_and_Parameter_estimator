from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.http import JsonResponse
from .models import Block, Classroom, Department, Faculty, Course, Student
from .forms import (BlockForm, ClassroomForm, DepartmentForm, FacultyForm,
                    CourseForm, StudentForm)


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'campus/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_blocks = Block.objects.count()
    total_classrooms = Classroom.objects.count()
    total_faculty = Faculty.objects.count()
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()

    # Capacity utilization per block
    blocks = Block.objects.all()
    block_data = []
    for block in blocks:
        classrooms = block.classroom_set.count()
        capacity = block.total_capacity()
        enrolled = block.classroom_set.aggregate(
            total=Sum('course__enrolled_students'))['total'] or 0
        util = round((enrolled / capacity * 100), 1) if capacity > 0 else 0
        block_data.append({
            'name': block.name,
            'classrooms': classrooms,
            'capacity': capacity,
            'utilization': util
        })

    # Faculty workload
    faculty_workload = []
    for f in Faculty.objects.all():
        faculty_workload.append({
            'name': f.name,
            'current': f.current_workload(),
            'max': f.max_workload_hours,
            'percent': f.workload_percent()
        })

    # Recent students
    recent_students = Student.objects.order_by('-date_of_admission')[:5]

    # Course enrollment stats
    courses = Course.objects.all()
    avg_enrollment = courses.aggregate(avg=Avg('enrolled_students'))['avg'] or 0

    context = {
        'total_blocks': total_blocks,
        'total_classrooms': total_classrooms,
        'total_faculty': total_faculty,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'block_data': block_data,
        'faculty_workload': faculty_workload,
        'recent_students': recent_students,
        'avg_enrollment': round(avg_enrollment, 1),
    }
    return render(request, 'campus/dashboard.html', context)


# ─── BLOCKS ──────────────────────────────────────────────────────────────────

@login_required
def block_list(request):
    blocks = Block.objects.all()
    return render(request, 'campus/block_list.html', {'blocks': blocks})

@login_required
def block_add(request):
    form = BlockForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Block added successfully!')
        return redirect('block_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Block', 'back_url': 'block_list'})

@login_required
def block_edit(request, pk):
    block = get_object_or_404(Block, pk=pk)
    form = BlockForm(request.POST or None, instance=block)
    if form.is_valid():
        form.save()
        messages.success(request, 'Block updated!')
        return redirect('block_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Block', 'back_url': 'block_list'})

@login_required
def block_delete(request, pk):
    block = get_object_or_404(Block, pk=pk)
    if request.method == 'POST':
        block.delete()
        messages.success(request, 'Block deleted.')
        return redirect('block_list')
    return render(request, 'campus/confirm_delete.html', {'obj': block, 'back_url': 'block_list'})


# ─── CLASSROOMS ──────────────────────────────────────────────────────────────

@login_required
def classroom_list(request):
    classrooms = Classroom.objects.select_related('block').all()
    return render(request, 'campus/classroom_list.html', {'classrooms': classrooms})

@login_required
def classroom_add(request):
    form = ClassroomForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Classroom added!')
        return redirect('classroom_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Classroom', 'back_url': 'classroom_list'})

@login_required
def classroom_edit(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    form = ClassroomForm(request.POST or None, instance=classroom)
    if form.is_valid():
        form.save()
        messages.success(request, 'Classroom updated!')
        return redirect('classroom_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Classroom', 'back_url': 'classroom_list'})

@login_required
def classroom_delete(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        classroom.delete()
        messages.success(request, 'Classroom deleted.')
        return redirect('classroom_list')
    return render(request, 'campus/confirm_delete.html', {'obj': classroom, 'back_url': 'classroom_list'})


# ─── FACULTY ─────────────────────────────────────────────────────────────────

@login_required
def faculty_list(request):
    faculty = Faculty.objects.select_related('department').all()
    return render(request, 'campus/faculty_list.html', {'faculty': faculty})

@login_required
def faculty_add(request):
    form = FacultyForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Faculty member added!')
        return redirect('faculty_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Faculty', 'back_url': 'faculty_list'})

@login_required
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    form = FacultyForm(request.POST or None, instance=faculty)
    if form.is_valid():
        form.save()
        messages.success(request, 'Faculty updated!')
        return redirect('faculty_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Faculty', 'back_url': 'faculty_list'})

@login_required
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty deleted.')
        return redirect('faculty_list')
    return render(request, 'campus/confirm_delete.html', {'obj': faculty, 'back_url': 'faculty_list'})


# ─── COURSES ─────────────────────────────────────────────────────────────────

@login_required
def course_list(request):
    courses = Course.objects.select_related('department', 'faculty', 'classroom').all()
    return render(request, 'campus/course_list.html', {'courses': courses})

@login_required
def course_add(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course added!')
        return redirect('course_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Course', 'back_url': 'course_list'})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course updated!')
        return redirect('course_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Course', 'back_url': 'course_list'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('course_list')
    return render(request, 'campus/confirm_delete.html', {'obj': course, 'back_url': 'course_list'})


# ─── STUDENTS ────────────────────────────────────────────────────────────────

@login_required
def student_list(request):
    students = Student.objects.select_related('department').all()
    return render(request, 'campus/student_list.html', {'students': students})

@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student added!')
        return redirect('student_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Student', 'back_url': 'student_list'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated!')
        return redirect('student_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Student', 'back_url': 'student_list'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'campus/confirm_delete.html', {'obj': student, 'back_url': 'student_list'})


# ─── DEPARTMENTS ─────────────────────────────────────────────────────────────

@login_required
def department_list(request):
    departments = Department.objects.annotate(
        faculty_count=Count('faculty'),
        course_count=Count('course'),
        student_count=Count('student')
    )
    return render(request, 'campus/department_list.html', {'departments': departments})

@login_required
def department_add(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Department added!')
        return redirect('department_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Add Department', 'back_url': 'department_list'})

@login_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if form.is_valid():
        form.save()
        messages.success(request, 'Department updated!')
        return redirect('department_list')
    return render(request, 'campus/form.html', {'form': form, 'title': 'Edit Department', 'back_url': 'department_list'})

@login_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, 'Department deleted.')
        return redirect('department_list')
    return render(request, 'campus/confirm_delete.html', {'obj': dept, 'back_url': 'department_list'})


# ─── AI INSIGHTS (API) ────────────────────────────────────────────────────────

@login_required
def ai_insights(request):
    insights = []

    # Overloaded faculty
    for f in Faculty.objects.all():
        if f.workload_percent() > 90:
            insights.append({
                'type': 'warning',
                'icon': '⚠️',
                'message': f"Faculty {f.name} is overloaded at {f.workload_percent()}% workload ({f.current_workload()}/{f.max_workload_hours} hrs)."
            })

    # Underutilized classrooms
    for c in Classroom.objects.all():
        if c.utilization_percent() < 30 and c.course_set.count() > 0:
            insights.append({
                'type': 'info',
                'icon': '💡',
                'message': f"Classroom {c} is underutilized at {c.utilization_percent()}% capacity."
            })

    # Overenrolled courses
    for course in Course.objects.all():
        if course.enrollment_percent() > 90:
            insights.append({
                'type': 'danger',
                'icon': '🔴',
                'message': f"Course {course.code} is {course.enrollment_percent()}% full ({course.enrolled_students}/{course.max_students} students)."
            })

    # Departments with no faculty
    for dept in Department.objects.all():
        if dept.faculty_set.count() == 0:
            insights.append({
                'type': 'warning',
                'icon': '👥',
                'message': f"Department '{dept.name}' has no faculty assigned."
            })

    if not insights:
        insights.append({
            'type': 'success',
            'icon': '✅',
            'message': 'All campus resources are balanced and running optimally!'
        })

    return render(request, 'campus/ai_insights.html', {'insights': insights})


# ─── ANALYTICS API ────────────────────────────────────────────────────────────

@login_required
def analytics_data(request):
    # Block utilization for charts
    blocks = Block.objects.all()
    block_labels = [b.name for b in blocks]
    block_capacity = [b.total_capacity() for b in blocks]

    # Faculty workload for charts
    faculty = Faculty.objects.all()
    faculty_labels = [f.name for f in faculty]
    faculty_workload = [f.current_workload() for f in faculty]

    # Course enrollment
    courses = Course.objects.all()[:8]
    course_labels = [c.code for c in courses]
    course_enrolled = [c.enrolled_students for c in courses]
    course_max = [c.max_students for c in courses]

    return JsonResponse({
        'blocks': {'labels': block_labels, 'capacity': block_capacity},
        'faculty': {'labels': faculty_labels, 'workload': faculty_workload},
        'courses': {'labels': course_labels, 'enrolled': course_enrolled, 'max': course_max},
    })
