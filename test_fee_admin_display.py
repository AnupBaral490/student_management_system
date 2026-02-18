#!/usr/bin/env python
"""
Test script to verify the fee admin display shows student names correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from fees.models import StudentFee
from fees.admin import StudentFeeAdmin

def test_admin_display():
    print("=" * 80)
    print("TESTING FEE ADMIN DISPLAY")
    print("=" * 80)
    
    # Create an instance of the admin class
    admin = StudentFeeAdmin(StudentFee, None)
    
    # Get all student fees
    student_fees = StudentFee.objects.select_related(
        'student', 
        'student__user', 
        'fee_structure'
    ).all()
    
    print(f"\nTotal Student Fee Records: {student_fees.count()}\n")
    
    # Test each display method
    for fee in student_fees:
        print(f"Fee ID: {fee.id}")
        print(f"  Student Name (admin method): {admin.student_name(fee)}")
        print(f"  Student ID (admin method): {admin.student_id(fee)}")
        print(f"  Fee Structure: {fee.fee_structure}")
        print(f"  Amount Due: {admin.amount_due_display(fee)}")
        print(f"  Amount Paid: {admin.amount_paid_display(fee)}")
        print(f"  Balance: {admin.balance_display(fee)}")
        print(f"  Status: {admin.payment_status_badge(fee)}")
        print()

if __name__ == '__main__':
    test_admin_display()
