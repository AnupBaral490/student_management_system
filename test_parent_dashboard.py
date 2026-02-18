"""
Test script to verify parent dashboard functionality
Run this with: python manage.py shell < test_parent_dashboard.py
"""

from accounts.models import User, ParentProfile, StudentProfile
from academic.models import StudentEnrollment, Subject
from attendance.models import AttendanceRecord
from examination.models import ExamResult

print("\n" + "="*60)
print("PARENT DASHBOARD DATA CHECK")
print("="*60)

# Check if parent users exist
parents = User.objects.filter(user_type='parent')
print(f"\n1. Total Parent Users: {parents.count()}")

for parent in parents:
    print(f"\n   Parent: {parent.username} ({parent.get_full_name()})")
    
    try:
        parent_profile = parent.parent_profile
        children = parent_profile.children.all()
        print(f"   Children linked: {children.count()}")
        
        if children.count() == 0:
            print("   ⚠️  No children linked to this parent!")
            print("   → Go to Admin Panel → Accounts → Parent profiles")
            print("   → Edit this parent and add children")
        
        for child in children:
            print(f"\n   Child: {child.user.get_full_name()} (ID: {child.student_id})")
            
            # Check enrollment
            enrollment = child.get_current_enrollment()
            if enrollment:
                print(f"   ✓ Enrolled in: {enrollment.class_enrolled}")
                
                # Check subjects
                subjects = Subject.objects.filter(
                    course=enrollment.class_enrolled.course,
                    year=enrollment.class_enrolled.year,
                    semester=enrollment.class_enrolled.semester
                )
                print(f"   ✓ Subjects: {subjects.count()}")
                
                # Check exam results
                results = ExamResult.objects.filter(student=child)
                print(f"   ✓ Exam Results: {results.count()}")
                
                # Check attendance
                attendance = AttendanceRecord.objects.filter(student=child)
                print(f"   ✓ Attendance Records: {attendance.count()}")
                
            else:
                print(f"   ⚠️  Not enrolled in any class")
                print("   → Go to Admin Panel → Academic → Student enrollments")
                print("   → Create enrollment for this student")
                
    except ParentProfile.DoesNotExist:
        print(f"   ⚠️  Parent profile not found!")

print("\n" + "="*60)
print("RECOMMENDATIONS")
print("="*60)

# Check if there are students available to link
students = StudentProfile.objects.all()
print(f"\nTotal Students Available: {students.count()}")

if students.count() > 0 and parents.count() > 0:
    print("\nTo link children to parents:")
    print("1. Go to: http://localhost:8000/admin/")
    print("2. Navigate to: Accounts → Parent profiles")
    print("3. Click on a parent to edit")
    print("4. In the 'Children' section, select students and click →")
    print("5. Click 'Save'")
    print("6. Refresh the parent dashboard to see the changes")

print("\n" + "="*60 + "\n")
