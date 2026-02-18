#!/usr/bin/env python
"""
Test script to verify student fee display shows student names
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from fees.models import StudentFee
from accounts.models import StudentProfile

print("=" * 60)
print("STUDENT FEE DISPLAY TEST")
print("=" * 60)

# Test StudentProfile __str__ method
print("\n1. Testing StudentProfile __str__ method:")
students = StudentProfile.objects.all()[:5]
for student in students:
    print(f"   - {student}")

# Test StudentFee display
print("\n2. Testing StudentFee records:")
fees = StudentFee.objects.select_related('student__user', 'fee_structure').all()[:5]
for fee in fees:
    print(f"   - Student: {fee.student}")
    print(f"     Name: {fee.student.user.get_full_name()}")
    print(f"     ID: {fee.student.student_id}")
    print(f"     Fee: {fee.fee_structure}")
    print(f"     Status: {fee.payment_status}")
    print()

print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nNow when you:")
print("1. Go to admin/fees/studentfee/")
print("2. Click 'Add student fee'")
print("3. The student dropdown will show: 'Student Name (Student ID)'")
print("4. The list view will show student names in the 'Student Name' column")
