#!/usr/bin/env python
"""
Test script to verify teacher class sections display correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, TeacherProfile
from academic.models import TeacherSubjectAssignment, StudentEnrollment

def test_teacher_classes():
    print("=" * 80)
    print("TESTING TEACHER CLASS SECTIONS")
    print("=" * 80)
    
    # Find a teacher (let's use baral as example)
    try:
        teacher_user = User.objects.get(username='baral')
        teacher_profile = teacher_user.teacher_profile
        
        print(f"\nTeacher: {teacher_user.get_full_name() or teacher_user.username}")
        print(f"Employee ID: {teacher_profile.employee_id}")
        print("-" * 80)
        
        # Get teacher's assignments
        teacher_assignments = TeacherSubjectAssignment.objects.filter(
            teacher=teacher_profile
        ).select_related('subject', 'class_assigned')
        
        print(f"\nTotal Classes Assigned: {teacher_assignments.count()}")
        print("-" * 80)
        
        for idx, assignment in enumerate(teacher_assignments, 1):
            print(f"\n{idx}. CLASS SECTION:")
            print(f"   Subject: {assignment.subject.name}")
            print(f"   Class: {assignment.class_assigned.name}")
            print(f"   Section: {assignment.class_assigned.section}")
            
            # Get student count
            student_count = StudentEnrollment.objects.filter(
                class_enrolled=assignment.class_assigned,
                is_active=True
            ).count()
            
            print(f"   Students Enrolled: {student_count}")
            
            # List students
            if student_count > 0:
                students = StudentEnrollment.objects.filter(
                    class_enrolled=assignment.class_assigned,
                    is_active=True
                ).select_related('student__user')
                
                print(f"   Student List:")
                for student_enrollment in students:
                    student_name = student_enrollment.student.user.get_full_name() or student_enrollment.student.user.username
                    print(f"     - {student_name} ({student_enrollment.student.student_id})")
            
            print(f"   ---")
        
        print("\n" + "=" * 80)
        print("DASHBOARD DISPLAY PREVIEW")
        print("=" * 80)
        
        for assignment in teacher_assignments:
            print(f"\n┌─────────────────────────────────────────┐")
            print(f"│ {assignment.subject.name:^39} │")
            print(f"│ {assignment.class_assigned.name:^39} │")
            print(f"├─────────────────────────────────────────┤")
            
            student_count = StudentEnrollment.objects.filter(
                class_enrolled=assignment.class_assigned,
                is_active=True
            ).count()
            
            print(f"│ 👥 {student_count} Students                          │")
            print(f"├─────────────────────────────────────────┤")
            print(f"│ [View Students]                         │")
            print(f"│ [Mark Attendance]                       │")
            print(f"│ [Create Assignment]                     │")
            print(f"│ [Enter Grades]                          │")
            print(f"└─────────────────────────────────────────┘")
        
    except User.DoesNotExist:
        print("\nTeacher 'baral' not found. Checking all teachers...")
        
        teachers = TeacherProfile.objects.all().select_related('user')
        print(f"\nTotal Teachers: {teachers.count()}")
        
        for teacher in teachers:
            print(f"\n- {teacher.user.get_full_name() or teacher.user.username} ({teacher.user.username})")
            assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher).count()
            print(f"  Classes: {assignments}")

if __name__ == '__main__':
    test_teacher_classes()
