#!/usr/bin/env python
"""
Verify teacher dashboard shows unpaid fees correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import TeacherProfile
from fees.models import StudentFee
from academic.models import TeacherSubjectAssignment, StudentEnrollment

User = get_user_model()

def simulate_teacher_dashboard_view():
    """Simulate what the teacher dashboard view generates"""
    print("=" * 70)
    print("SIMULATING TEACHER BARAL'S DASHBOARD VIEW")
    print("=" * 70)
    
    try:
        baral_user = User.objects.get(username='baral')
        teacher_profile = baral_user.teacher_profile
        
        print(f"\n✓ Teacher: {baral_user.get_full_name()}")
        
        # Get teacher's assignments (same as in the view)
        teacher_assignments = TeacherSubjectAssignment.objects.filter(
            teacher=teacher_profile
        ).select_related('subject', 'class_assigned')
        
        print(f"✓ Teaching assignments: {teacher_assignments.count()}")
        
        # Get students with unpaid fees (same logic as in the view)
        students_with_unpaid_fees = []
        
        for assignment in teacher_assignments:
            class_obj = assignment.class_assigned
            enrollments = StudentEnrollment.objects.filter(
                class_enrolled=class_obj,
                is_active=True
            ).select_related('student__user')
            
            for enrollment in enrollments:
                unpaid_fees = StudentFee.objects.filter(
                    student=enrollment.student,
                    payment_status__in=['pending', 'partial', 'overdue']
                ).select_related('fee_structure')
                
                if unpaid_fees.exists():
                    total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
                    students_with_unpaid_fees.append({
                        'student': enrollment.student,
                        'class': class_obj,
                        'total_unpaid': total_unpaid,
                        'fee_count': unpaid_fees.count()
                    })
        
        # Limit to 10 (same as in the view)
        students_with_unpaid_fees = students_with_unpaid_fees[:10]
        
        print(f"\n{'='*70}")
        print("DASHBOARD CONTEXT DATA")
        print(f"{'='*70}")
        print(f"students_with_unpaid_fees count: {len(students_with_unpaid_fees)}")
        
        if students_with_unpaid_fees:
            print("\n✅ UNPAID FEES SECTION WILL BE DISPLAYED")
            print("\nStudents that will appear in the dashboard:")
            print("-" * 70)
            for item in students_with_unpaid_fees:
                print(f"\nStudent: {item['student'].user.get_full_name()}")
                print(f"  Student ID: {item['student'].student_id}")
                print(f"  Class: {item['class'].name}")
                print(f"  Total Unpaid: ${item['total_unpaid']:.2f}")
                print(f"  Fee Items: {item['fee_count']}")
        else:
            print("\n⚠️  UNPAID FEES SECTION WILL NOT BE DISPLAYED")
            print("   (No students with unpaid fees found)")
        
        print(f"\n{'='*70}")
        print("TEMPLATE RENDERING")
        print(f"{'='*70}")
        
        if students_with_unpaid_fees:
            print("\nThe template will render:")
            print("  {% if students_with_unpaid_fees %} ← TRUE")
            print("    <div class='card shadow'>")
            print("      <div class='card-header bg-danger'>")
            print("        Students with Unpaid Fees")
            print("      </div>")
            print("      <table>")
            for item in students_with_unpaid_fees:
                print(f"        <tr>")
                print(f"          <td>{item['student'].user.get_full_name()}</td>")
                print(f"          <td>{item['student'].student_id}</td>")
                print(f"          <td>{item['class'].name}</td>")
                print(f"          <td>${item['total_unpaid']:.2f}</td>")
                print(f"        </tr>")
            print("      </table>")
            print("    </div>")
            print("  {% endif %}")
        else:
            print("\nThe template will render:")
            print("  {% if students_with_unpaid_fees %} ← FALSE")
            print("  (Section will not appear)")
        
        print(f"\n{'='*70}")
        print("✅ VERIFICATION COMPLETE")
        print(f"{'='*70}")
        
        if students_with_unpaid_fees:
            print("\n✅ Teacher Baral WILL see students with unpaid fees")
            print("   The 'Students with Unpaid Fees' card will appear on the dashboard")
        else:
            print("\n⚠️  Teacher Baral will NOT see the unpaid fees section")
            print("   All students in Baral's classes have paid their fees")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    simulate_teacher_dashboard_view()
