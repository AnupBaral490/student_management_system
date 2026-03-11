from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, time
from accounts.models import TeacherProfile
from academic.models import TeacherSubjectAssignment, AcademicYear
from attendance.models import TeacherAttendance, AttendanceSession
import random

class Command(BaseCommand):
    help = 'Test the enhanced teacher attendance functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date to create test data for (YYYY-MM-DD format)',
            default=timezone.now().date().strftime('%Y-%m-%d')
        )

    def handle(self, *args, **options):
        test_date_str = options['date']
        try:
            test_date = datetime.strptime(test_date_str, '%Y-%m-%d').date()
        except ValueError:
            self.stdout.write(
                self.style.ERROR(f'Invalid date format: {test_date_str}. Use YYYY-MM-DD format.')
            )
            return

        self.stdout.write(f'Creating test data for date: {test_date}')

        # Get all teachers
        teachers = TeacherProfile.objects.all()
        if not teachers.exists():
            self.stdout.write(
                self.style.ERROR('No teachers found. Please create some teachers first.')
            )
            return

        # Get current academic year
        try:
            academic_year = AcademicYear.objects.get(is_current=True)
        except AcademicYear.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('No current academic year found. Please create one first.')
            )
            return

        created_attendance = 0
        created_sessions = 0

        for teacher in teachers:
            # Create teacher attendance record
            attendance, created = TeacherAttendance.objects.get_or_create(
                teacher=teacher,
                date=test_date,
                defaults={
                    'status': random.choice(['present', 'absent', 'late', 'half_day']),
                    'check_in_time': time(random.randint(8, 10), random.randint(0, 59)),
                    'check_out_time': time(random.randint(15, 17), random.randint(0, 59)),
                    'is_auto_marked': random.choice([True, False]),
                    'remarks': f'Test attendance for {teacher.user.get_full_name()}'
                }
            )
            
            if created:
                attendance.calculate_hours()
                attendance.save()
                created_attendance += 1

            # Get teacher's subject assignments
            subject_assignments = TeacherSubjectAssignment.objects.filter(
                teacher=teacher,
                academic_year=academic_year
            )

            # Create attendance sessions for each subject assignment
            for assignment in subject_assignments:
                session, session_created = AttendanceSession.objects.get_or_create(
                    teacher_assignment=assignment,
                    date=test_date,
                    start_time=time(random.randint(9, 15), 0),
                    defaults={
                        'end_time': time(random.randint(10, 16), 0),
                        'topic_covered': f'Test topic for {assignment.subject.name}',
                        'is_completed': random.choice([True, False]),
                        'notes': f'Test session for {assignment.subject.name} - {assignment.class_assigned}'
                    }
                )
                
                if session_created:
                    created_sessions += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_attendance} teacher attendance records '
                f'and {created_sessions} attendance sessions for {test_date}'
            )
        )

        # Display summary
        self.stdout.write('\n--- Summary ---')
        total_teachers = teachers.count()
        present_teachers = TeacherAttendance.objects.filter(
            date=test_date, 
            status__in=['present', 'late']
        ).count()
        
        self.stdout.write(f'Total teachers: {total_teachers}')
        self.stdout.write(f'Present teachers: {present_teachers}')
        self.stdout.write(f'Attendance rate: {(present_teachers/total_teachers*100):.1f}%')
        
        # Show sample enhanced data
        self.stdout.write('\n--- Sample Enhanced Data ---')
        sample_attendance = TeacherAttendance.objects.filter(date=test_date).first()
        if sample_attendance:
            subject_assignments = TeacherSubjectAssignment.objects.filter(
                teacher=sample_attendance.teacher
            ).select_related('subject', 'class_assigned')
            
            attendance_sessions = AttendanceSession.objects.filter(
                teacher_assignment__teacher=sample_attendance.teacher,
                date=test_date
            ).select_related('teacher_assignment__subject')
            
            self.stdout.write(f'Teacher: {sample_attendance.teacher.user.get_full_name()}')
            self.stdout.write(f'Status: {sample_attendance.get_status_display()}')
            self.stdout.write(f'Check-in: {sample_attendance.check_in_time}')
            self.stdout.write(f'Total Hours: {sample_attendance.total_hours}')
            self.stdout.write(f'Subjects Assigned: {subject_assignments.count()}')
            self.stdout.write(f'Sessions Today: {attendance_sessions.count()}')
            self.stdout.write(f'Completed Sessions: {attendance_sessions.filter(is_completed=True).count()}')
            
            if subject_assignments.exists():
                self.stdout.write('Subject Assignments:')
                for assignment in subject_assignments:
                    self.stdout.write(f'  - {assignment.subject.name} ({assignment.class_assigned})')