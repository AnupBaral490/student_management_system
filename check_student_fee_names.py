#!/usr/bin/env python
"""
Script to check student fee records and verify student names are properly linked
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from fees.models import StudentFee
from accounts.models import StudentProfile

def check_student_fees():
    print("=" * 80)
    print("CHECKING STUDENT FEE RECORDS")
    print("=" * 80)
    
    # Get all student fees
    student_fees = StudentFee.objects.select_related(
        'student', 
        'student__user', 
        'fee_structure'
    ).all()
    
    print(f"\nTotal Student Fee Records: {student_fees.count()}")
    print("-" * 80)
    
    for fee in student_fees:
        print(f"\nFee ID: {fee.id}")
        print(f"Student Object: {fee.student}")
        
        if fee.student:
            print(f"  - Student ID: {fee.student.student_id}")
            print(f"  - User Object: {fee.student.user}")
            
            if fee.student.user:
                print(f"  - Username: {fee.student.user.username}")
                print(f"  - First Name: {fee.student.user.first_name}")
                print(f"  - Last Name: {fee.student.user.last_name}")
                print(f"  - Full Name: {fee.student.user.get_full_name()}")
            else:
                print("  - WARNING: No user linked to student!")
        else:
            print("  - WARNING: No student linked to fee!")
        
        print(f"Fee Structure: {fee.fee_structure}")
        print(f"Amount Due: ${fee.amount_due}")
        print(f"Status: {fee.payment_status}")
    
    print("\n" + "=" * 80)
    print("CHECKING ALL STUDENT PROFILES")
    print("=" * 80)
    
    students = StudentProfile.objects.select_related('user').all()
    print(f"\nTotal Students: {students.count()}")
    
    for student in students:
        print(f"\nStudent ID: {student.student_id}")
        print(f"  User: {student.user}")
        print(f"  Username: {student.user.username}")
        print(f"  Full Name: {student.user.get_full_name()}")
        print(f"  String Representation: {str(student)}")

if __name__ == '__main__':
    check_student_fees()
