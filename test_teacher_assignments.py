"""
Test script to check teacher assignments for parent's children
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, ParentProfile, StudentProfile
from academic.models import TeacherSubjectAssignment, StudentEnrollment

print("\n" + "="*70)
print("CHECKING TEACHER ASSIGNMENTS FOR PARENT'S CHILDREN")
print("="*70)

# Get parent
try:
    parent_user = User.objects.get(username='dajikopita')
    print(f"\n✓ Found parent: {parent_user.username}")
    
    parent_profile = parent_user.parent_profile
    children = parent_profile.children.all()
    print(f"✓ Children: {children.count()}")
    
    for child in children:
        print(f"\n--- Child: {child.user.get_full_name()} ---")
        print(f"Student ID: {child.student_id}")
        
        # Get enrollment
        enrollment = child.get_current_enrollment()
        if enrollment:
            print(f"✓ Enrolled in: {enrollment.class_enrolled}")
            print(f"  Course: {enrollment.class_enrolled.course.name}")
            print(f"  Year: {enrollment.class_enrolled.year}")
            print(f"  Semester: {enrollment.class_enrolled.semester}")
            print(f"  Section: {enrollment.class_enrolled.section}")
            
            # Check teacher assignments for this class
            teacher_assignments = TeacherSubjectAssignment.objects.filter(
                class_assigned=enrollment.class_enrolled
            ).select_related('teacher__user', 'subject')
            
            print(f"\n📚 Teacher Assignments: {teacher_assignments.count()}")
            
            if teacher_assignments.exists():
                for assignment in teacher_assignments:
                    print(f"  ✓ {assignment.teacher.user.get_full_name()} - {assignment.subject.name}")
            else:
                print("  ⚠️  NO TEACHER ASSIGNMENTS FOUND!")
                print("\n  To fix this:")
                print("  1. Go to Django Admin: /admin/")
                print("  2. Navigate to: Academic → Teacher subject assignments")
                print("  3. Click 'Add Teacher Subject Assignment'")
                print("  4. Select:")
                print(f"     - Teacher: (any teacher)")
                print(f"     - Subject: (any subject for this course)")
                print(f"     - Class: {enrollment.class_enrolled}")
                print("  5. Click 'Save'")
        else:
            print("  ⚠️  Not enrolled in any class")
            
except User.DoesNotExist:
    print("\n✗ Parent 'dajikopita' not found")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("CHECKING ALL TEACHER ASSIGNMENTS IN SYSTEM")
print("="*70)

all_assignments = TeacherSubjectAssignment.objects.all().select_related('teacher__user', 'subject', 'class_assigned')
print(f"\nTotal Teacher Assignments: {all_assignments.count()}")

if all_assignments.exists():
    for assignment in all_assignments[:10]:  # Show first 10
        print(f"  - {assignment.teacher.user.get_full_name()} teaches {assignment.subject.name} to {assignment.class_assigned}")
else:
    print("\n⚠️  NO TEACHER ASSIGNMENTS IN THE SYSTEM!")
    print("\nYou need to create teacher assignments:")
    print("1. Go to /admin/")
    print("2. Academic → Teacher subject assignments")
    print("3. Create assignments linking teachers to classes and subjects")

print("\n" + "="*70 + "\n")
