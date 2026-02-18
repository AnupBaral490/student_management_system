#!/usr/bin/env python
"""
Manage student fees - Set paid/unpaid status for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile
from fees.models import StudentFee

User = get_user_model()

def list_all_student_fees():
    """List all students and their fee status"""
    print("=" * 80)
    print("ALL STUDENTS FEE STATUS")
    print("=" * 80)
    
    students = StudentProfile.objects.all().select_related('user')
    
    for student in students:
        print(f"\n{'='*80}")
        print(f"Student: {student.user.get_full_name()} ({student.user.username})")
        print(f"Student ID: {student.student_id}")
        
        fees = StudentFee.objects.filter(student=student)
        
        if fees.exists():
            print(f"Fee Records: {fees.count()}")
            for fee in fees:
                print(f"\n  Fee: {fee.fee_structure}")
                print(f"  Amount Due: ${fee.amount_due:.2f}")
                print(f"  Amount Paid: ${fee.amount_paid:.2f}")
                print(f"  Balance: ${fee.balance_amount:.2f}")
                print(f"  Status: {fee.payment_status}")
                
                if fee.payment_status in ['pending', 'partial', 'overdue']:
                    print(f"  ⚠️  UNPAID - Will appear in teacher dashboard")
                else:
                    print(f"  ✓ PAID - Will NOT appear in teacher dashboard")
        else:
            print("  No fee records")

def set_fee_status(username, status='unpaid'):
    """Set a student's fee to paid or unpaid"""
    print("=" * 80)
    print(f"SETTING FEE STATUS FOR {username.upper()}")
    print("=" * 80)
    
    try:
        user = User.objects.get(username=username)
        student = user.student_profile
        
        print(f"\n✓ Found: {user.get_full_name()}")
        
        fees = StudentFee.objects.filter(student=student)
        
        if not fees.exists():
            print("❌ No fee records found for this student")
            return
        
        for fee in fees:
            print(f"\nProcessing fee: {fee.fee_structure}")
            
            if status == 'unpaid':
                # Set to unpaid
                fee.amount_paid = 0
                fee.payment_status = 'pending'
                fee.save()
                print(f"  ✓ Set to UNPAID")
                print(f"    Amount Paid: ${fee.amount_paid:.2f}")
                print(f"    Balance: ${fee.balance_amount:.2f}")
                print(f"    Status: {fee.payment_status}")
            elif status == 'partial':
                # Set to partially paid (50%)
                fee.amount_paid = fee.amount_due * 0.5
                fee.payment_status = 'partial'
                fee.save()
                print(f"  ✓ Set to PARTIALLY PAID")
                print(f"    Amount Paid: ${fee.amount_paid:.2f}")
                print(f"    Balance: ${fee.balance_amount:.2f}")
                print(f"    Status: {fee.payment_status}")
            elif status == 'paid':
                # Set to fully paid
                fee.amount_paid = fee.amount_due
                fee.payment_status = 'paid'
                fee.save()
                print(f"  ✓ Set to PAID")
                print(f"    Amount Paid: ${fee.amount_paid:.2f}")
                print(f"    Balance: ${fee.balance_amount:.2f}")
                print(f"    Status: {fee.payment_status}")
            else:
                print(f"  ❌ Invalid status: {status}")
        
        print(f"\n✅ Fee status updated successfully")
        
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
    except StudentProfile.DoesNotExist:
        print(f"❌ Student profile not found for '{username}'")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 80)
        print("STUDENT FEE MANAGEMENT")
        print("=" * 80)
        print("\n1. List all students and their fee status")
        print("2. Set student fee to UNPAID")
        print("3. Set student fee to PARTIALLY PAID")
        print("4. Set student fee to PAID")
        print("5. Quick set Daji to UNPAID (for testing)")
        print("6. Quick set Daji to PAID")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            list_all_student_fees()
        elif choice == '2':
            username = input("Enter student username: ").strip()
            set_fee_status(username, 'unpaid')
        elif choice == '3':
            username = input("Enter student username: ").strip()
            set_fee_status(username, 'partial')
        elif choice == '4':
            username = input("Enter student username: ").strip()
            set_fee_status(username, 'paid')
        elif choice == '5':
            set_fee_status('daji', 'unpaid')
            print("\n✅ Daji's fee set to UNPAID")
            print("   Teacher Baral will now see Daji in the unpaid fees list")
        elif choice == '6':
            set_fee_status('daji', 'paid')
            print("\n✅ Daji's fee set to PAID")
            print("   Teacher Baral will NOT see Daji in the unpaid fees list")
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()
