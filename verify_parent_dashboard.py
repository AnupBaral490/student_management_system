"""
Quick verification script for parent dashboard
Run with: python verify_parent_dashboard.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, ParentProfile
from academic.models import Subject
from attendance.models import AttendanceRecord

print("\n" + "="*70)
print("PARENT DASHBOARD VERIFICATION")
print("="*70)

# Check dajikopita
try:
    parent_user = User.objects.get(username='dajikopita')
    print(f"\n✓ Found parent user: {parent_user.username}")
    
    parent_profile = parent_user.parent_profile
    print(f"✓ Found parent profile")
    
    children = parent_profile.children.all()
    print(f"✓ Children count: {children.count()}")
    
    if children.count() > 0:
        print("\n" + "-"*70)
        print("CHILDREN DATA:")
        print("-"*70)
        
        for child in children:
            print(f"\nChild: {child.user.get_full_name()} ({child.user.username})")
            print(f"  Student ID: {child.student_id}")
            
            # Check enrollment
            enrollment = child.get_current_enrollment()
            if enrollment:
                print(f"  ✓ Enrolled: {enrollment.class_enrolled}")
                
                # Check subjects
                subjects = Subject.objects.filter(
                    course=enrollment.class_enrolled.course,
                    year=enrollment.class_enrolled.year,
                    semester=enrollment.class_enrolled.semester
                )
                print(f"  ✓ Subjects: {subjects.count()}")
                
                # Check attendance
                attendance = AttendanceRecord.objects.filter(student=child)
                total = attendance.count()
                present = attendance.filter(status__in=['present', 'late']).count()
                percentage = (present / total * 100) if total > 0 else 0
                print(f"  ✓ Attendance: {percentage:.1f}% ({present}/{total})")
            else:
                print(f"  ⚠️  Not enrolled")
        
        print("\n" + "="*70)
        print("✓ VERIFICATION SUCCESSFUL")
        print("="*70)
        print("\nThe parent dashboard should now display:")
        print("  - Children information")
        print("  - Enrollment details")
        print("  - Subjects (with 'Not Graded Yet' if no exam results)")
        print("  - Attendance percentage")
        print("\nTo see the dashboard:")
        print("  1. Make sure the Django server is running")
        print("  2. Log in as 'dajikopita'")
        print("  3. Go to the dashboard")
        print("\n" + "="*70 + "\n")
    else:
        print("\n⚠️  No children linked!")
        print("\nTo link children, run:")
        print("  python manage.py link_parent_child dajikopita daji")
        
except User.DoesNotExist:
    print("\n✗ Parent user 'dajikopita' not found")
except ParentProfile.DoesNotExist:
    print("\n✗ Parent profile not found for 'dajikopita'")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
