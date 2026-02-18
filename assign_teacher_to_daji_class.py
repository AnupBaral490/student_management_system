"""
Script to assign teacher Baral to Daji's class subjects
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, StudentProfile, TeacherProfile
from academic.models import TeacherSubjectAssignment, Subject, Class

print("\n" + "="*70)
print("ASSIGNING TEACHER TO DAJI'S CLASS")
print("="*70)

# Get Daji's enrollment
child = StudentProfile.objects.get(student_id='212')
enrollment = child.get_current_enrollment()

if not enrollment:
    print("\n✗ Daji is not enrolled in any class")
    exit()

print(f"\n✓ Daji's Class: {enrollment.class_enrolled}")

# Get teacher Baral
try:
    baral_user = User.objects.get(username='baral')
    baral_teacher = baral_user.teacher_profile
    print(f"✓ Found teacher: {baral_user.get_full_name()} ({baral_teacher.employee_id})")
except:
    print("\n✗ Teacher 'baral' not found or doesn't have a teacher profile")
    exit()

# Get subjects for Daji's class
subjects = Subject.objects.filter(
    course=enrollment.class_enrolled.course,
    year=enrollment.class_enrolled.year,
    semester=enrollment.class_enrolled.semester
)

print(f"\n✓ Subjects in this class: {subjects.count()}")

# Assign teacher to each subject
created_count = 0
existing_count = 0

for subject in subjects:
    assignment, created = TeacherSubjectAssignment.objects.get_or_create(
        teacher=baral_teacher,
        subject=subject,
        class_assigned=enrollment.class_enrolled,
        defaults={
            'academic_year': enrollment.class_enrolled.academic_year
        }
    )
    
    if created:
        print(f"  ✓ Created assignment: {subject.name}")
        created_count += 1
    else:
        print(f"  - Already assigned: {subject.name}")
        existing_count += 1

print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"New assignments created: {created_count}")
print(f"Existing assignments: {existing_count}")
print(f"Total assignments: {created_count + existing_count}")
print(f"\n✓ Teacher Baral is now assigned to teach all subjects in Daji's class!")
print(f"{'='*70}\n")
