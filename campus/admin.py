from django.contrib import admin
from .models import Block, Classroom, Department, Faculty, Course, Student

admin.site.register(Block)
admin.site.register(Classroom)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Student)

admin.site.site_header = "LPU Campus Management System"
admin.site.site_title = "LPU CMS Admin"
admin.site.index_title = "Welcome to LPU CMS Administration"
