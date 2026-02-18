#!/usr/bin/env python
"""
Check Daji's fee status and teacher Baral's view
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, TeacherProfile
from fees.models import StudentFee
from academic.models import TeacherSubjectAssignment, StudentEnrollment

User = get_user_model()

def check_daji_fees():
    """Check Daji's fee status"""
    print("=" * 70)
    print("CHECKING DAJI'S FEE STATUS")
    print("=" * 70)
    
    # Find Daji
    try:
        daji_user = User.objects.get(username='daji')
        print(f"\n✓ Found user: {daji_user.username} - {daji_user.get_full_name()}")
        
        daji_profile = daji_user.student_profile
        print(f"✓ Student ID: {daji_profile.student_id}")
        
        # Check enrollment
        enrollment = daji_profile.get_current_enrollment()
        if enrollment:
            print(f"✓ Enrolled in: {enrollment.class_enrolled.name}")
            print(f"  Course: {enrollment.class_enrolled.course.name}")
        else:
            print("⚠ No active enrollment")
        
        # Check all fees
        all_fees = StudentFee.objects.filter(student=daji_profile)
        print(f"\n📊 Total Fee Records: {all_fees.count()}")
        
        if all_fees.exists():
            for fee in all_fees:
                print(f"\n  Fee Structure: {fee.fee_structure}")
                print(f"  Amount Due: ${fee.amount_due}")
                print(f"  Amount Paid: ${fee.amount_paid}")
                print(f"  Balance: ${fee.balance_amount}")
                print(f"  Status: {fee.payment_status}")
                print(f"  Due Date: {fee.fee_structure.due_date}")
        else:
            print("  ℹ️  No fee records found for Daji")
        
        # Check unpaid fees specifically
        unpaid_fees = StudentFee.objects.filter(
            student=daji_profile,
            payment_status__in=['pending', 'partial', 'overdue']
        )
        
        print(f"\n💰 Unpaid Fees: {unpaid_fees.count()}")
        if unpaid_fees.exists():
            total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
            print(f"   Total Unpaid Amount: ${total_unpaid:.2f}")
            for fee in unpaid_fees:
                print(f"   - {fee.fee_structure}: ${fee.balance_amount:.2f} ({fee.payment_status})")
        else:
            print("   ✓ All fees are paid!")
        
    except User.DoesNotExist:
        print("❌ User 'daji' not found")
        return
    except StudentProfile.DoesNotExist:
        print("❌ Student profile not found for daji")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return

def check_baral_teacher_view():
    """Check what teacher Baral can see"""
    print("\n" + "=" * 70)
    print("CHECKING TEACHER BARAL'S VIEW")
    print("=" * 70)
    
    try:
        baral_user = User.objects.get(username='baral')
        print(f"\n✓ Found teacher: {baral_user.username} - {baral_user.get_full_name()}")
        
        baral_profile = baral_user.teacher_profile
        print(f"✓ Teacher profile found")
        
        # Get teacher's assignments
        teacher_assignments = TeacherSubjectAssignment.objects.filter(
            teacher=baral_profile
        ).select_related('subject', 'class_assigned')
        
        print(f"\n📚 Teaching Assignments: {teacher_assignments.count()}")
        
        students_with_unpaid_fees = []
        
        for assignment in teacher_assignments:
            class_obj = assignment.class_assigned
            print(f"\n  Class: {class_obj.name}")
            print(f"  Subject: {assignment.subject.name}")
            
            # Get students in this class
            enrollments = StudentEnrollment.objects.filter(
                class_enrolled=class_obj,
                is_active=True
            ).select_related('student__user')
            
            print(f"  Students enrolled: {enrollments.count()}")
            
            for enrollment in enrollments:
                student = enrollment.student
                print(f"\n    Student: {student.user.get_full_name()} ({student.student_id})")
                
                # Check unpaid fees
                unpaid_fees = StudentFee.objects.filter(
                    student=student,
                    payment_status__in=['pending', 'partial', 'overdue']
                ).select_related('fee_structure')
                
                if unpaid_fees.exists():
                    total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
                    print(f"    💰 Unpaid Fees: ${total_unpaid:.2f} ({unpaid_fees.count()} items)")
                    
                    students_with_unpaid_fees.append({
                        'student': student,
                        'class': class_obj,
                        'total_unpaid': total_unpaid,
                        'fee_count': unpaid_fees.count()
                    })
                    
                    for fee in unpaid_fees:
                        print(f"       - {fee.fee_structure}: ${fee.balance_amount:.2f} ({fee.payment_status})")
                else:
                    print(f"    ✓ No unpaid fees")
        
        print(f"\n{'='*70}")
        print(f"SUMMARY FOR TEACHER BARAL")
        print(f"{'='*70}")
        print(f"Total students with unpaid fees: {len(students_with_unpaid_fees)}")
        
        if students_with_unpaid_fees:
            print("\nStudents with unpaid fees:")
            for item in students_with_unpaid_fees:
                print(f"  • {item['student'].user.get_full_name()} - ${item['total_unpaid']:.2f}")
        else:
            print("\n✓ All students in Baral's classes have paid their fees")
        
    except User.DoesNotExist:
        print("❌ User 'baral' not found")
        return
    except TeacherProfile.DoesNotExist:
        print("❌ Teacher profile not found for baral")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return

def create_sample_fee_for_daji():
    """Create a sample unpaid fee for Daji for testing"""
    print("\n" + "=" * 70)
    print("CREATE SAMPLE UNPAID FEE FOR DAJI")
    print("=" * 70)
    
    try:
        daji_user = User.objects.get(username='daji')
        daji_profile = daji_user.student_profile
        enrollment = daji_profile.get_current_enrollment()
        
        if not enrollment:
            print("❌ Daji is not enrolled in any class")
            return
        
        from fees.models import FeeStructure
        from academic.models import AcademicYear
        
        # Get or create academic year
        academic_year = AcademicYear.objects.first()
        if not academic_year:
            print("❌ No academic year found")
            return
        
        # Check if fee structure exists for Daji's class
        fee_structure = FeeStructure.objects.filter(
            class_assigned=enrollment.class_enrolled,
            academic_year=academic_year
        ).first()
        
        if not fee_structure:
            print(f"Creating fee structure for {enrollment.class_enrolled.name}...")
            from django.utils import timezone
            from datetime import timedelta
            
            fee_structure = FeeStructure.objects.create(
                class_assigned=enrollment.class_enrolled,
                academic_year=academic_year,
                tuition_fee=5000.00,
                library_fee=200.00,
                lab_fee=300.00,
                sports_fee=100.00,
                frequency='semester',
                due_date=timezone.now().date() + timedelta(days=30),
                is_active=True
            )
            print(f"✓ Created fee structure: {fee_structure}")
        else:
            print(f"✓ Fee structure exists: {fee_structure}")
        
        # Check if student fee exists
        student_fee = StudentFee.objects.filter(
            student=daji_profile,
            fee_structure=fee_structure
        ).first()
        
        if not student_fee:
            print(f"Creating student fee record for Daji...")
            student_fee = StudentFee.objects.create(
                student=daji_profile,
                fee_structure=fee_structure,
                amount_due=fee_structure.total_fee,
                amount_paid=0,
                payment_status='pending'
            )
            print(f"✓ Created student fee: ${student_fee.amount_due}")
        else:
            print(f"✓ Student fee exists")
            print(f"  Amount Due: ${student_fee.amount_due}")
            print(f"  Amount Paid: ${student_fee.amount_paid}")
            print(f"  Balance: ${student_fee.balance_amount}")
            print(f"  Status: {student_fee.payment_status}")
            
            # Make it unpaid if it's paid
            if student_fee.payment_status == 'paid':
                print("\n  Making fee unpaid for testing...")
                student_fee.amount_paid = 0
                student_fee.payment_status = 'pending'
                student_fee.save()
                print(f"  ✓ Fee status changed to: {student_fee.payment_status}")
        
        print(f"\n✅ Daji now has an unpaid fee of ${student_fee.balance_amount:.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_daji_fees()
    check_baral_teacher_view()
    
    # Ask if user wants to create a sample fee
    print("\n" + "=" * 70)
    response = input("\nDo you want to create/reset an unpaid fee for Daji? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        create_sample_fee_for_daji()
        print("\n" + "=" * 70)
        print("RE-CHECKING AFTER FEE CREATION")
        print("=" * 70)
        check_daji_fees()
        check_baral_teacher_view()
