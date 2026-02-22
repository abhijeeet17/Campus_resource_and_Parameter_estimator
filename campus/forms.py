from django import forms
from .models import Block, Classroom, Department, Faculty, Course, Student


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


class BlockForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Block
        fields = ['name', 'description', 'total_floors']


class ClassroomForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['block', 'room_number', 'floor', 'capacity', 'room_type', 'is_available']


class DepartmentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']


class FacultyForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'employee_id', 'department', 'email', 'phone', 'designation', 'max_workload_hours']


class CourseForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'faculty', 'classroom',
                  'credit_hours', 'semester', 'enrolled_students', 'max_students', 'schedule']


class StudentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration_number', 'department', 'email',
                  'phone', 'semester', 'cgpa']
