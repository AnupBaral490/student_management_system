from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('mark/<int:session_id>/', views.mark_attendance_session, name='mark_attendance_session'),
    path('view/', views.view_attendance, name='view_attendance'),
    path('reports/', views.attendance_reports, name='attendance_reports'),
    # AJAX endpoints
    path('ajax/get-students/', views.get_students_for_assignment, name='get_students_ajax'),
    path('ajax/save-attendance/', views.save_attendance_ajax, name='save_attendance_ajax'),
]