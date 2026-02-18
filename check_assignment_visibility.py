#!/usr/bin/env python
"""
Script to diagnose why assignments aren't showing for students
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, StudentProfile
from academic.models import Assignment, StudentEnrollment, Class

print("=" * 80)
print("ASSIGNMENT VISIBILITY DIAGNOSTIC")
print("=" * 80)

# Get all assignments
assignments = Assignment.objects.all()
print(f"\n📋 Total Assignments in System: {assignments.count()}")

for assignment in assignments:
    print(f"\n  Assignment: {assignment.title}")
    print(f"  Subject: {assignment.subject.name}")
    print(f"  Class: {assignment.class_assigned}")
    print(f"  Teacher: {assignment.teacher.user.get_full_name()}")
    print(f"  Active: {assignment.is_active}")
    print(f"  Due Date: {assignment.due_date}")
    
    # Count students in this class
    students_in_class = StudentEnrollment.objects.filter(
        class_enrolled=assignment.class_assigned,
        is_active=True
    ).count()
    print(f"  Students in Class: {students_in_class}")

# Get all student enrollments
print(f"\n\n👨‍🎓 Student Enrollments:")
print("=" * 80)

enrollments = StudentEnrollment.objects.filter(is_active=True).select_related(
    'student__user', 'class_enrolled__course'
)

for enrollment in enrollments:
    student_name = enrollment.student.user.get_full_name()
    student_id = enrollment.student.student_id
    class_name = enrollment.class_enrolled.name
    
    print(f"\n  Student: {student_name} ({student_id})")
    print(f"  Class: {class_name}")
    print(f"  Class ID: {enrollment.class_enrolled.id}")
    
    # Check assignments for this student
    student_assignments = Assignment.objects.filter(
        class_assigned=enrollment.class_enrolled,
        is_active=True
    )
    
    print(f"  Assignments Available: {student_assignments.count()}")
    
    if student_assignments.exists():
        for assignment in student_assignments:
            print(f"    - {assignment.title} (Due: {assignment.due_date})")
    else:
        print(f"    ⚠️  No assignments found for this class!")

# Check for class mismatches
print(f"\n\n🔍 Checking for Potential Issues:")
print("=" * 80)

all_classes = Class.objects.all()
print(f"\nTotal Classes in System: {all_classes.count()}")

for cls in all_classes:
    student_count = StudentEnrollment.objects.filter(
        class_enrolled=cls,
        is_active=True
    ).count()
    assignment_count = Assignment.objects.filter(
        class_assigned=cls,
        is_active=True
    ).count()
    
    print(f"\n  Class: {cls.name}")
    print(f"  Class ID: {cls.id}")
    print(f"  Students: {student_count}")
    print(f"  Assignments: {assignment_count}")
    
    if assignment_count > 0 and student_count == 0:
        print(f"  ⚠️  WARNING: Assignments exist but no students enrolled!")
    elif student_count > 0 and assignment_count == 0:
        print(f"  ℹ️  INFO: Students enrolled but no assignments created yet")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
