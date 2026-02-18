#!/usr/bin/env python
"""
Script to fix students with multiple active enrollments
Keeps only the most recent enrollment active
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import StudentProfile
from academic.models import StudentEnrollment

print("=" * 80)
print("FIXING MULTIPLE ACTIVE ENROLLMENTS")
print("=" * 80)

# Find students with multiple active enrollments
students_with_multiple = StudentProfile.objects.filter(
    studentenrollment__is_active=True
).annotate(
    enrollment_count=django.db.models.Count('studentenrollment', filter=django.db.models.Q(studentenrollment__is_active=True))
).filter(enrollment_count__gt=1)

print(f"\nFound {students_with_multiple.count()} students with multiple active enrollments\n")

for student in students_with_multiple:
    enrollments = StudentEnrollment.objects.filter(
        student=student,
        is_active=True
    ).order_by('-enrollment_date')
    
    print(f"Student: {student.user.get_full_name()} ({student.student_id})")
    print(f"  Has {enrollments.count()} active enrollments:")
    
    for i, enrollment in enumerate(enrollments):
        print(f"    {i+1}. {enrollment.class_enrolled.name} (Enrolled: {enrollment.enrollment_date})")
    
    # Keep the most recent enrollment, deactivate others
    most_recent = enrollments.first()
    print(f"\n  ✓ Keeping: {most_recent.class_enrolled.name}")
    
    deactivated_count = 0
    for enrollment in enrollments[1:]:
        enrollment.is_active = False
        enrollment.save()
        print(f"  ✗ Deactivating: {enrollment.class_enrolled.name}")
        deactivated_count += 1
    
    print(f"  Deactivated {deactivated_count} old enrollments\n")
    print("-" * 80)

print("\n" + "=" * 80)
print("FIX COMPLETE")
print("=" * 80)
print("\nRecommendation: Students should only have ONE active enrollment at a time.")
print("If you need to move a student to a different class:")
print("  1. Deactivate their current enrollment")
print("  2. Create a new enrollment in the new class")
print("=" * 80)
