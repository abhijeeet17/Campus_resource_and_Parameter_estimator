from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Blocks
    path('blocks/', views.block_list, name='block_list'),
    path('blocks/add/', views.block_add, name='block_add'),
    path('blocks/edit/<int:pk>/', views.block_edit, name='block_edit'),
    path('blocks/delete/<int:pk>/', views.block_delete, name='block_delete'),

    # Classrooms
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('classrooms/add/', views.classroom_add, name='classroom_add'),
    path('classrooms/edit/<int:pk>/', views.classroom_edit, name='classroom_edit'),
    path('classrooms/delete/<int:pk>/', views.classroom_delete, name='classroom_delete'),

    # Faculty
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/edit/<int:pk>/', views.faculty_edit, name='faculty_edit'),
    path('faculty/delete/<int:pk>/', views.faculty_delete, name='faculty_delete'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:pk>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),

    # AI & Analytics
    path('ai-insights/', views.ai_insights, name='ai_insights'),
    path('api/analytics/', views.analytics_data, name='analytics_data'),
]
