#!/usr/bin/env python
"""
Script to fix Daji's enrollment to the correct class with assignments
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import StudentProfile
from academic.models import StudentEnrollment, Assignment

print("=" * 80)
print("FIXING DAJI'S ENROLLMENT")
print("=" * 80)

# Get Daji's student profile
daji = StudentProfile.objects.filter(student_id='212').first()

if not daji:
    print("ERROR: Could not find student with ID 212")
    exit(1)

print(f"\nStudent: {daji.user.get_full_name()} ({daji.student_id})")

# Get all enrollments for Daji
all_enrollments = StudentEnrollment.objects.filter(student=daji)

print(f"\nAll Enrollments (Active and Inactive):")
for enrollment in all_enrollments:
    status = "ACTIVE" if enrollment.is_active else "INACTIVE"
    
    # Check assignments for this class
    assignment_count = Assignment.objects.filter(
        class_assigned=enrollment.class_enrolled,
        is_active=True
    ).count()
    
    print(f"  [{status}] {enrollment.class_enrolled.name}")
    print(f"           Class ID: {enrollment.class_enrolled.id}")
    print(f"           Enrolled: {enrollment.enrollment_date}")
    print(f"           Assignments: {assignment_count}")
    print()

# The correct class is "BIM 7th Semester - Year 1, Sem 1 - A" (ID: 89)
correct_class_id = 89

print("=" * 80)
print("APPLYING FIX")
print("=" * 80)

# Deactivate all enrollments first
StudentEnrollment.objects.filter(student=daji).update(is_active=False)
print("✓ Deactivated all enrollments")

# Activate only the correct enrollment
correct_enrollment = StudentEnrollment.objects.filter(
    student=daji,
    class_enrolled_id=correct_class_id
).first()

if correct_enrollment:
    correct_enrollment.is_active = True
    correct_enrollment.save()
    print(f"✓ Activated enrollment in: {correct_enrollment.class_enrolled.name}")
    
    # Verify assignments are now visible
    assignments = Assignment.objects.filter(
        class_assigned=correct_enrollment.class_enrolled,
        is_active=True
    )
    print(f"✓ Student now has access to {assignments.count()} assignment(s)")
    
    for assignment in assignments:
        print(f"    - {assignment.title} (Due: {assignment.due_date})")
else:
    print("ERROR: Could not find enrollment for class ID 89")

print("\n" + "=" * 80)
print("FIX COMPLETE")
print("=" * 80)
