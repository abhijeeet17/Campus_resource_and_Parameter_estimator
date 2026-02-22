from django.db import models
from django.contrib.auth.models import User


class Block(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_floors = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_capacity(self):
        return sum(c.capacity for c in self.classroom_set.all())

    def total_classrooms(self):
        return self.classroom_set.count()


class Classroom(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField(default=0)
    capacity = models.IntegerField(default=30)
    room_type = models.CharField(max_length=50, choices=[
        ('lecture', 'Lecture Hall'),
        ('lab', 'Computer Lab'),
        ('seminar', 'Seminar Room'),
        ('tutorial', 'Tutorial Room'),
    ], default='lecture')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.block.name} - Room {self.room_number}"

    def utilization_percent(self):
        enrollments = self.course_set.aggregate(
            total=models.Sum('enrolled_students'))['total'] or 0
        if self.capacity > 0:
            return min(round((enrollments / self.capacity) * 100, 1), 100)
        return 0


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    designation = models.CharField(max_length=100, default='Assistant Professor')
    max_workload_hours = models.IntegerField(default=18)

    def __str__(self):
        return self.name

    def current_workload(self):
        return sum(c.credit_hours for c in self.course_set.all())

    def workload_percent(self):
        if self.max_workload_hours > 0:
            return min(round((self.current_workload() / self.max_workload_hours) * 100, 1), 100)
        return 0


class Course(models.Model):
    SEMESTER_CHOICES = [(str(i), f'Semester {i}') for i in range(1, 9)]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    credit_hours = models.IntegerField(default=3)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES, default='1')
    enrolled_students = models.IntegerField(default=0)
    max_students = models.IntegerField(default=60)
    schedule = models.CharField(max_length=200, blank=True, help_text="e.g. Mon/Wed 9:00-10:30")

    def __str__(self):
        return f"{self.code} - {self.name}"

    def enrollment_percent(self):
        if self.max_students > 0:
            return min(round((self.enrolled_students / self.max_students) * 100, 1), 100)
        return 0


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    semester = models.CharField(max_length=2, choices=Course.SEMESTER_CHOICES, default='1')
    courses = models.ManyToManyField(Course, blank=True)
    cgpa = models.FloatField(default=0.0)
    date_of_admission = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} - {self.name}"
