"""
Direct test of parent dashboard logic
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, ParentProfile
from academic.models import StudentEnrollment, Subject, Assignment
from attendance.models import AttendanceRecord
from notifications.models import Notification
from examination.models import Examination, ExamResult
from datetime import timedelta
from django.utils import timezone as django_timezone

print("\n" + "="*70)
print("DIRECT TEST OF PARENT DASHBOARD LOGIC")
print("="*70)

try:
    # Get parent user
    parent_user = User.objects.get(username='dajikopita')
    print(f"\n✓ Found parent: {parent_user.username}")
    
    # Get parent profile
    parent_profile = parent_user.parent_profile
    print(f"✓ Found parent profile")
    
    # Get children
    children_profiles = parent_profile.children.all()
    print(f"✓ Children profiles count: {children_profiles.count()}")
    
    # Prepare children data
    children_data = []
    upcoming_events = []
    
    for child in children_profiles:
        print(f"\n--- Processing child: {child.user.get_full_name()} ---")
        
        # Get enrollment
        enrollment = None
        try:
            enrollment = child.get_current_enrollment()
            print(f"  ✓ Enrollment: {enrollment}")
        except Exception as e:
            print(f"  ✗ Enrollment error: {e}")
        
        # Get attendance
        attendance_percentage = 0
        total_sessions = 0
        present_sessions = 0
        try:
            attendance_records = AttendanceRecord.objects.filter(student=child)
            total_sessions = attendance_records.count()
            present_sessions = attendance_records.filter(status__in=['present', 'late']).count()
            attendance_percentage = (present_sessions / total_sessions * 100) if total_sessions > 0 else 0
            print(f"  ✓ Attendance: {attendance_percentage:.2f}% ({present_sessions}/{total_sessions})")
        except Exception as e:
            print(f"  ✗ Attendance error: {e}")
        
        # Get subjects
        subjects_with_grades = []
        gpa = 0.0
        
        if enrollment:
            try:
                subjects = Subject.objects.filter(
                    course=enrollment.class_enrolled.course,
                    year=enrollment.class_enrolled.year,
                    semester=enrollment.class_enrolled.semester
                )
                print(f"  ✓ Subjects: {subjects.count()}")
                
                for subject in subjects:
                    subjects_with_grades.append({
                        'name': subject.name,
                        'grade': None,
                        'percentage': 0
                    })
                    
            except Exception as e:
                print(f"  ✗ Subjects error: {e}")
        
        # Create child info
        child_info = {
            'profile': child,
            'user': child.user,
            'enrollment': enrollment,
            'attendance_percentage': round(attendance_percentage, 2),
            'gpa': round(gpa, 2),
            'total_sessions': total_sessions,
            'present_sessions': present_sessions,
            'subjects': subjects_with_grades
        }
        children_data.append(child_info)
        print(f"  ✓ Child info added to children_data")
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULTS")
    print(f"{'='*70}")
    print(f"Children Data Count: {len(children_data)}")
    
    if len(children_data) > 0:
        print("\n✓✓✓ SUCCESS! Children data is populated ✓✓✓")
        for idx, child_info in enumerate(children_data, 1):
            print(f"\nChild #{idx}:")
            print(f"  Name: {child_info['user'].get_full_name()}")
            print(f"  Student ID: {child_info['profile'].student_id}")
            print(f"  Enrollment: {child_info['enrollment']}")
            print(f"  Attendance: {child_info['attendance_percentage']}%")
            print(f"  Subjects: {len(child_info['subjects'])}")
            print(f"  GPA: {child_info['gpa']}")
    else:
        print("\n✗✗✗ FAILED! Children data is empty ✗✗✗")
    
    # Get notifications
    try:
        child_user_ids = [child.user.id for child in children_profiles]
        recent_notifications = Notification.objects.filter(
            recipients__in=child_user_ids
        ).order_by('-created_at').distinct()[:5] if child_user_ids else []
        print(f"\n✓ Notifications: {recent_notifications.count()}")
    except Exception as e:
        print(f"\n✗ Notifications error: {e}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"\n✗ MAIN ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
