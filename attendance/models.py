from django.db import models
from django.utils import timezone
from accounts.models import StudentProfile, TeacherProfile
from academic.models import Subject, Class, TeacherSubjectAssignment
from datetime import datetime, time

class AttendanceSession(models.Model):
    """Represents a single class session for attendance marking"""
    teacher_assignment = models.ForeignKey(TeacherSubjectAssignment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic_covered = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['teacher_assignment', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.teacher_assignment.subject.name} - {self.teacher_assignment.class_assigned} - {self.date}"

class AttendanceRecord(models.Model):
    ATTENDANCE_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    remarks = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'student']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.session} - {self.status}"

class AttendanceSummary(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    total_sessions = models.PositiveIntegerField(default=0)
    sessions_attended = models.PositiveIntegerField(default=0)
    sessions_late = models.PositiveIntegerField(default=0)
    sessions_excused = models.PositiveIntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ['student', 'subject', 'class_enrolled', 'month', 'year']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} - {self.month}/{self.year}"
    
    def calculate_percentage(self):
        if self.total_sessions > 0:
            # Count present, late, and excused as attended
            attended = self.sessions_attended + self.sessions_late + self.sessions_excused
            self.attendance_percentage = (attended / self.total_sessions) * 100
        else:
            self.attendance_percentage = 0.00
        return self.attendance_percentage


class TeacherAttendance(models.Model):
    """Daily attendance record for teachers"""
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    first_activity_time = models.DateTimeField(null=True, blank=True, help_text="Exact time of first activity")
    last_activity_time = models.DateTimeField(null=True, blank=True, help_text="Exact time of last activity")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_auto_marked = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['teacher', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.date} - {self.status}"
    
    def calculate_hours(self):
        """Calculate total hours worked based on real activity times or manual times"""
        if self.first_activity_time and self.last_activity_time:
            # Use real activity times for accurate calculation
            delta = self.last_activity_time - self.first_activity_time
            self.total_hours = round(delta.total_seconds() / 3600, 2)
        elif self.check_in_time and self.check_out_time:
            # Fallback to manual times
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            delta = check_out - check_in
            self.total_hours = round(delta.total_seconds() / 3600, 2)
        return self.total_hours
    
    def determine_status(self):
        """Auto-determine status based on actual activities and real check-in time"""
        from academic.models import TeacherSubjectAssignment
        
        # Check if teacher has any subject assignments for today
        teacher_assignments = TeacherSubjectAssignment.objects.filter(teacher=self.teacher)
        
        # Check if teacher performed any real activities today
        has_real_activities = self.has_performed_duties()
        
        if not has_real_activities:
            # No real activities performed, mark as absent regardless of check-in
            self.status = 'absent'
            return self.status
        
        # Has real activities, determine based on first activity time
        actual_check_in_time = None
        
        if self.first_activity_time:
            # Use real first activity time
            actual_check_in_time = self.first_activity_time.time()
        elif self.check_in_time:
            # Fallback to manual check-in time
            actual_check_in_time = self.check_in_time
        
        if actual_check_in_time:
            school_start = time(9, 0)
            late_threshold = time(9, 30)
            
            if actual_check_in_time <= school_start:
                self.status = 'present'
            elif actual_check_in_time <= late_threshold:
                self.status = 'late'
            else:
                self.status = 'late'
            
            # Check for half day (less than 4 hours but has activities)
            if self.total_hours > 0 and self.total_hours < 4:
                self.status = 'half_day'
        else:
            # Has activities but no time recorded - mark as present
            self.status = 'present'
        
        return self.status
    
    def has_performed_duties(self):
        """Check if teacher has performed actual duties today"""
        # Check if teacher marked attendance for any of their subjects
        attendance_sessions = AttendanceSession.objects.filter(
            teacher_assignment__teacher=self.teacher,
            date=self.date,
            is_completed=True
        )
        
        if attendance_sessions.exists():
            return True
        
        # Check for other significant activities
        significant_activities = TeacherActivityLog.objects.filter(
            teacher=self.teacher,
            timestamp__date=self.date,
            activity_type__in=['mark_attendance', 'create_assignment', 'grade_exam']
        )
        
        return significant_activities.exists()
    
    def get_duties_performed(self):
        """Get list of duties performed today"""
        duties = []
        
        # Check attendance sessions
        attendance_sessions = AttendanceSession.objects.filter(
            teacher_assignment__teacher=self.teacher,
            date=self.date,
            is_completed=True
        ).select_related('teacher_assignment__subject', 'teacher_assignment__class_assigned')
        
        for session in attendance_sessions:
            duties.append({
                'type': 'attendance',
                'description': f"Marked attendance for {session.teacher_assignment.subject.name} - {session.teacher_assignment.class_assigned.name}",
                'time': session.created_at.time() if session.created_at else None
            })
        
        # Check other activities
        activities = TeacherActivityLog.objects.filter(
            teacher=self.teacher,
            timestamp__date=self.date,
            activity_type__in=['create_assignment', 'grade_exam', 'send_message']
        ).order_by('timestamp')
        
        for activity in activities:
            duties.append({
                'type': activity.activity_type,
                'description': activity.description,
                'time': activity.timestamp.time()
            })
        
        return duties
    
    def get_subjects_not_attended(self):
        """Get list of subjects teacher was supposed to attend but didn't"""
        from academic.models import TeacherSubjectAssignment
        
        # Get all teacher's assignments
        all_assignments = TeacherSubjectAssignment.objects.filter(
            teacher=self.teacher
        ).select_related('subject', 'class_assigned')
        
        # Get assignments where attendance was marked
        attended_assignments = AttendanceSession.objects.filter(
            teacher_assignment__teacher=self.teacher,
            date=self.date,
            is_completed=True
        ).values_list('teacher_assignment_id', flat=True)
        
        # Find assignments not attended
        not_attended = []
        for assignment in all_assignments:
            if assignment.id not in attended_assignments:
                not_attended.append({
                    'subject': assignment.subject.name,
                    'class': assignment.class_assigned.name,
                    'assignment_id': assignment.id
                })
        
        return not_attended


class TeacherActivityLog(models.Model):
    """Log of teacher activities for attendance tracking"""
    ACTIVITY_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('first_login', 'First Login'),
        ('mark_attendance', 'Mark Student Attendance'),
        ('create_assignment', 'Create Assignment'),
        ('grade_exam', 'Grade Exam'),
        ('send_message', 'Send Message'),
        ('view_report', 'View Report'),
        ('dashboard_access', 'Dashboard Access'),
        ('system_navigation', 'System Navigation'),
        ('other', 'Other Activity'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['teacher', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.activity_type} - {self.timestamp}"


class TeacherLeave(models.Model):
    """Leave requests and approvals for teachers"""
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('earned', 'Earned Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    admin_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.leave_type} - {self.start_date} to {self.end_date}"
    
    @property
    def total_days(self):
        """Calculate total leave days"""
        return (self.end_date - self.start_date).days + 1