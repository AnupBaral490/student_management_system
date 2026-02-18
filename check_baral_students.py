#!/usr/bin/env python
"""
Script to check Baral teacher's assignments and students
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, TeacherProfile
from academic.models import TeacherSubjectAssignment, StudentEnrollment

print("=" * 80)
print("BARAL TEACHER DIAGNOSTIC")
print("=" * 80)

# Find Baral teacher
baral_users = User.objects.filter(username__icontains='baral')

if not baral_users.exists():
    print("\n❌ No user found with 'baral' in username")
    exit(1)

for user in baral_users:
    print(f"\nUser: {user.username} ({user.get_full_name()})")
    print(f"User Type: {user.user_type}")
    
    if user.user_type == 'teacher':
        try:
            teacher_profile = user.teacher_profile
            print(f"Teacher ID: {teacher_profile.id}")
            
            # Get teacher's assignments
            assignments = TeacherSubjectAssignment.objects.filter(
                teacher=teacher_profile
            ).select_related('subject', 'class_assigned', 'academic_year')
            
            print(f"\n📚 Teacher Assignments: {assignments.count()}")
            print("=" * 80)
            
            for assignment in assignments:
                print(f"\nAssignment ID: {assignment.id}")
                print(f"Subject: {assignment.subject.name}")
                print(f"Class: {assignment.class_assigned.name}")
                print(f"Class ID: {assignment.class_assigned.id}")
                print(f"Academic Year: {assignment.academic_year.year}")
                
                # Get students in this class
                enrollments = StudentEnrollment.objects.filter(
                    class_enrolled=assignment.class_assigned,
                    is_active=True
                ).select_related('student__user')
                
                print(f"\n👨‍🎓 Students Enrolled: {enrollments.count()}")
                
                if enrollments.exists():
                    for enrollment in enrollments:
                        student_name = enrollment.student.user.get_full_name()
                        if not student_name.strip():
                            student_name = enrollment.student.user.username
                        
                        print(f"  - {student_name} (ID: {enrollment.student.student_id})")
                        print(f"    First Name: '{enrollment.student.user.first_name}'")
                        print(f"    Last Name: '{enrollment.student.user.last_name}'")
                        print(f"    Username: '{enrollment.student.user.username}'")
                else:
                    print("  ⚠️  No students enrolled in this class!")
                
                print("-" * 80)
                
        except TeacherProfile.DoesNotExist:
            print("❌ Teacher profile not found for this user")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
