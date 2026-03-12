from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime, time
from .models import TeacherAttendance, TeacherActivityLog

class TeacherAttendanceMiddleware(MiddlewareMixin):
    """
    Middleware to automatically track teacher attendance based on their real-time activity
    """
    
    def process_request(self, request):
        # Only track authenticated users who are teachers
        if not request.user.is_authenticated:
            return None
        
        if request.user.user_type != 'teacher':
            return None
        
        if not hasattr(request.user, 'teacher_profile'):
            return None
        
        teacher = request.user.teacher_profile
        today = timezone.now().date()
        current_time = timezone.now()
        current_time_only = current_time.time()
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Get or create today's attendance record
        attendance, created = TeacherAttendance.objects.get_or_create(
            teacher=teacher,
            date=today,
            defaults={
                'check_in_time': current_time_only,
                'ip_address': ip_address,
                'is_auto_marked': True,
                'status': 'present'  # Will be recalculated
            }
        )
        
        # If this is the first activity of the day, set real check-in time
        if created:
            attendance.check_in_time = current_time_only
            attendance.first_activity_time = current_time
            self._log_activity(request, teacher, ip_address, is_first_activity=True)
        else:
            # Update last activity time
            attendance.last_activity_time = current_time
            self._log_activity(request, teacher, ip_address, is_first_activity=False)
        
        # Always update check-out time with current activity (last activity = check out)
        attendance.check_out_time = current_time_only
        attendance.calculate_hours()
        attendance.determine_status()
        attendance.save()
        
        return None
    
    def _log_activity(self, request, teacher, ip_address, is_first_activity=False):
        """Log specific teacher activities with real-time tracking"""
        path = request.path
        method = request.method
        
        # Determine activity type based on URL pattern
        activity_type = 'other'
        description = ''
        
        if 'login' in path or 'accounts/login' in path:
            activity_type = 'login'
            description = 'Teacher logged in to system'
        elif 'logout' in path:
            activity_type = 'logout'
            description = 'Teacher logged out from system'
        elif ('attendance/mark' in path or 'attendance/save' in path or 
              'save_attendance_ajax' in path) and method == 'POST':
            activity_type = 'mark_attendance'
            description = 'Marked student attendance'
            # This is a significant activity - update teacher attendance status
            self._update_teacher_attendance_status(teacher)
        elif 'assignment' in path and method == 'POST':
            activity_type = 'create_assignment'
            description = 'Created/updated assignment'
        elif 'exam' in path or 'result' in path:
            activity_type = 'grade_exam'
            description = 'Graded exam/entered results'
        elif 'message' in path and method == 'POST':
            activity_type = 'send_message'
            description = 'Sent message'
        elif 'report' in path:
            activity_type = 'view_report'
            description = 'Viewed reports'
        elif 'dashboard' in path:
            activity_type = 'dashboard_access'
            description = 'Accessed dashboard'
        elif method == 'GET' and any(x in path for x in ['academic', 'attendance', 'accounts']):
            activity_type = 'system_navigation'
            description = f'Navigated to {path}'
        
        # Mark first activity of the day specially
        if is_first_activity:
            if activity_type == 'other':
                activity_type = 'first_login'
                description = f'First system access of the day - {path}'
            else:
                description = f'FIRST ACTIVITY: {description}'
        
        # Log all activities to track real-time usage
        TeacherActivityLog.objects.create(
            teacher=teacher,
            activity_type=activity_type,
            description=description,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )
    
    def _update_teacher_attendance_status(self, teacher):
        """Update teacher attendance status when they perform significant activities"""
        today = timezone.now().date()
        
        try:
            attendance = TeacherAttendance.objects.get(teacher=teacher, date=today)
            # Recalculate status based on real activities
            attendance.determine_status()
            attendance.save()
        except TeacherAttendance.DoesNotExist:
            # This shouldn't happen as attendance is created in process_request
            pass
