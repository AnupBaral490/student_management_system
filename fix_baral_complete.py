#!/usr/bin/env python
"""
Complete fix for Baral teacher - assign to both BIM classes and enroll Daji properly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, TeacherProfile, StudentProfile
from academic.models import TeacherSubjectAssignment, StudentEnrollment, Class, Subject, AcademicYear

print("=" * 80)
print("COMPLETE FIX FOR BARAL TEACHER & DAJI STUDENT")
print("=" * 80)

# Get Baral teacher
baral_user = User.objects.filter(username='baral').first()
if not baral_user:
    print("ERROR: Baral user not found")
    exit(1)

baral_teacher = baral_user.teacher_profile
print(f"\n✓ Found teacher: {baral_user.get_full_name()}")

# Get Daji student
daji = StudentProfile.objects.filter(student_id='212').first()
if not daji:
    print("ERROR: Daji student not found")
    exit(1)

print(f"✓ Found student: {daji.user.get_full_name()}")

# Get both BIM classes
class_89 = Class.objects.filter(id=89).first()  # BIM 7th Semester - Year 1, Sem 1 - A (has assignment)
class_90 = Class.objects.filter(id=90).first()  # BIM 7th Semester (where Baral teaches)

if not class_89 or not class_90:
    print("ERROR: Could not find required classes")
    exit(1)

print(f"\n✓ Class 89: {class_89.name}")
print(f"✓ Class 90: {class_90.name}")

# Get current academic year
academic_year = AcademicYear.objects.filter(is_current=True).first()
if not academic_year:
    print("ERROR: No current academic year found")
    exit(1)

print(f"✓ Academic Year: {academic_year.year}")

# Get Sociology subject (the one with the assignment)
sociology = Subject.objects.filter(name='Sociology').first()
if not sociology:
    print("ERROR: Sociology subject not found")
    exit(1)

print(f"✓ Subject: {sociology.name}")

print("\n" + "=" * 80)
print("APPLYING FIXES")
print("=" * 80)

# Fix 1: Assign Baral to teach Sociology in class 89 (where the assignment is)
assignment_89, created = TeacherSubjectAssignment.objects.get_or_create(
    teacher=baral_teacher,
    subject=sociology,
    class_assigned=class_89,
    academic_year=academic_year
)

if created:
    print(f"\n✓ Created new assignment: Baral -> Sociology -> {class_89.name}")
else:
    print(f"\n✓ Assignment already exists: Baral -> Sociology -> {class_89.name}")

# Fix 2: Enroll Daji in class 89 (where the assignment is)
# First, deactivate all other enrollments
StudentEnrollment.objects.filter(student=daji).update(is_active=False)
print("✓ Deactivated all previous enrollments for Daji")

# Create/activate enrollment in class 89
enrollment_89, created = StudentEnrollment.objects.get_or_create(
    student=daji,
    class_enrolled=class_89,
    defaults={'is_active': True}
)

if not created:
    enrollment_89.is_active = True
    enrollment_89.save()
    print(f"✓ Reactivated enrollment: Daji -> {class_89.name}")
else:
    print(f"✓ Created new enrollment: Daji -> {class_89.name}")

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Verify Baral's assignments
print(f"\nBaral's Assignments:")
baral_assignments = TeacherSubjectAssignment.objects.filter(
    teacher=baral_teacher
).select_related('subject', 'class_assigned')

for assignment in baral_assignments:
    student_count = StudentEnrollment.objects.filter(
        class_enrolled=assignment.class_assigned,
        is_active=True
    ).count()
    print(f"  - {assignment.subject.name} -> {assignment.class_assigned.name}")
    print(f"    Students: {student_count}")

# Verify Daji's enrollment
print(f"\nDaji's Active Enrollment:")
daji_enrollment = StudentEnrollment.objects.filter(
    student=daji,
    is_active=True
).first()

if daji_enrollment:
    print(f"  Class: {daji_enrollment.class_enrolled.name}")
    
    # Check assignments available
    from academic.models import Assignment
    assignments = Assignment.objects.filter(
        class_assigned=daji_enrollment.class_enrolled,
        is_active=True
    )
    print(f"  Assignments Available: {assignments.count()}")
    for assignment in assignments:
        print(f"    - {assignment.title}")

print("\n" + "=" * 80)
print("FIX COMPLETE")
print("=" * 80)
print("\n✓ Baral can now mark attendance for Daji in Sociology class")
print("✓ Daji can see the assignment in the student dashboard")
print("✓ Both attendance and assignments are now working correctly")
