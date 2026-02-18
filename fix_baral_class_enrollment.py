#!/usr/bin/env python
"""
Script to enroll Daji in Baral teacher's class
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import StudentProfile
from academic.models import StudentEnrollment, Class

print("=" * 80)
print("FIXING DAJI'S ENROLLMENT FOR BARAL'S CLASS")
print("=" * 80)

# Get Daji's student profile
daji = StudentProfile.objects.filter(student_id='212').first()

if not daji:
    print("ERROR: Could not find student with ID 212")
    exit(1)

print(f"\nStudent: {daji.user.get_full_name()} ({daji.student_id})")

# Get Baral's class (BIM 7th Semester - Class ID: 90)
baral_class = Class.objects.filter(id=90).first()

if not baral_class:
    print("ERROR: Could not find class with ID 90")
    exit(1)

print(f"Target Class: {baral_class.name} (ID: {baral_class.id})")

# Check current enrollment
current_enrollment = StudentEnrollment.objects.filter(
    student=daji,
    is_active=True
).first()

if current_enrollment:
    print(f"\nCurrent Active Enrollment: {current_enrollment.class_enrolled.name} (ID: {current_enrollment.class_enrolled.id})")
    
    # Deactivate current enrollment
    current_enrollment.is_active = False
    current_enrollment.save()
    print("✓ Deactivated current enrollment")

# Create new enrollment in Baral's class
new_enrollment, created = StudentEnrollment.objects.get_or_create(
    student=daji,
    class_enrolled=baral_class,
    defaults={'is_active': True}
)

if not created:
    new_enrollment.is_active = True
    new_enrollment.save()
    print("✓ Reactivated existing enrollment in Baral's class")
else:
    print("✓ Created new enrollment in Baral's class")

# Verify the fix
print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Check if Daji now appears in Baral's class
from academic.models import TeacherSubjectAssignment

baral_assignments = TeacherSubjectAssignment.objects.filter(
    class_assigned=baral_class
).select_related('subject')

print(f"\nBaral's Subjects in this class:")
for assignment in baral_assignments:
    print(f"  - {assignment.subject.name}")
    
    # Count students
    student_count = StudentEnrollment.objects.filter(
        class_enrolled=assignment.class_assigned,
        is_active=True
    ).count()
    print(f"    Students enrolled: {student_count}")

print("\n" + "=" * 80)
print("FIX COMPLETE")
print("=" * 80)
print("\nDaji is now enrolled in Baral's class.")
print("Students should now appear when Baral marks attendance.")
