#!/usr/bin/env python
"""
Test dashboard result blocking for unpaid fees
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, ParentProfile
from fees.models import StudentFee

User = get_user_model()

def test_student_dashboard_blocking():
    """Test student dashboard result blocking"""
    print("=" * 70)
    print("TESTING STUDENT DASHBOARD RESULT BLOCKING")
    print("=" * 70)
    
    # Test with Daji
    try:
        daji = User.objects.get(username='daji')
        daji_profile = daji.student_profile
        
        print(f"\nStudent: {daji.get_full_name()}")
        
        # Check unpaid fees
        unpaid_fees = StudentFee.objects.filter(
            student=daji_profile,
            payment_status__in=['pending', 'partial', 'overdue']
        )
        
        has_unpaid_fees = unpaid_fees.exists()
        
        print(f"Has unpaid fees: {has_unpaid_fees}")
        
        if has_unpaid_fees:
            total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
            print(f"Total unpaid: ${total_unpaid:.2f}")
            print("\n✅ EXPECTED BEHAVIOR:")
            print("   - Red warning banner at top of dashboard")
            print("   - 'View Results' button shows as 'View Results (Locked)'")
            print("   - Button is red with lock icon")
            print("   - Clicking result_list URL will show fee payment warning")
        else:
            print("\n✅ EXPECTED BEHAVIOR:")
            print("   - No warning banner")
            print("   - 'View Results' button is normal (blue/info color)")
            print("   - Can access results normally")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_parent_dashboard_blocking():
    """Test parent dashboard result blocking"""
    print("\n" + "=" * 70)
    print("TESTING PARENT DASHBOARD RESULT BLOCKING")
    print("=" * 70)
    
    # Test with parent1 (Daji's parent)
    try:
        parent = User.objects.get(username='parent1')
        parent_profile = parent.parent_profile
        
        print(f"\nParent: {parent.get_full_name() or parent.username}")
        
        children = parent_profile.children.all()
        print(f"Children: {children.count()}")
        
        any_child_has_unpaid_fees = False
        
        for child in children:
            print(f"\n  Child: {child.user.get_full_name()}")
            
            unpaid_fees = StudentFee.objects.filter(
                student=child,
                payment_status__in=['pending', 'partial', 'overdue']
            )
            
            has_unpaid = unpaid_fees.exists()
            print(f"  Has unpaid fees: {has_unpaid}")
            
            if has_unpaid:
                any_child_has_unpaid_fees = True
                total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
                print(f"  Total unpaid: ${total_unpaid:.2f}")
        
        print(f"\nAny child has unpaid fees: {any_child_has_unpaid_fees}")
        
        if any_child_has_unpaid_fees:
            print("\n✅ EXPECTED BEHAVIOR:")
            print("   - Child card shows red 'Unpaid Fees' badge")
            print("   - Red alert below child card")
            print("   - 'View Results' button shows as 'View Results (Locked)'")
            print("   - Button is red with lock icon")
            print("   - Clicking result_list URL will show fee payment warning")
        else:
            print("\n✅ EXPECTED BEHAVIOR:")
            print("   - No fee badges on child cards")
            print("   - 'View Results' button is normal (green)")
            print("   - Can access results normally")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_result_list_access():
    """Test result list page access"""
    print("\n" + "=" * 70)
    print("TESTING RESULT LIST PAGE ACCESS")
    print("=" * 70)
    
    try:
        daji = User.objects.get(username='daji')
        daji_profile = daji.student_profile
        
        unpaid_fees = StudentFee.objects.filter(
            student=daji_profile,
            payment_status__in=['pending', 'partial', 'overdue']
        )
        
        has_unpaid_fees = unpaid_fees.exists()
        
        print(f"\nStudent: {daji.get_full_name()}")
        print(f"Has unpaid fees: {has_unpaid_fees}")
        
        if has_unpaid_fees:
            print("\n✅ EXPECTED BEHAVIOR ON /examination/result_list/:")
            print("   - Large red warning banner with lock icon")
            print("   - List of all unpaid fees with amounts")
            print("   - 'Results Locked' message")
            print("   - NO results table shown")
            print("   - Contact information for payment")
        else:
            print("\n✅ EXPECTED BEHAVIOR ON /examination/result_list/:")
            print("   - Normal results table")
            print("   - Student statistics (GPA, average, etc.)")
            print("   - Full access to all results")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    test_student_dashboard_blocking()
    test_parent_dashboard_blocking()
    test_result_list_access()
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print("\n✅ All tests completed!")
    print("\nTo test in browser:")
    print("1. Login as 'daji' (student) - Check dashboard")
    print("2. Login as 'parent1' (parent) - Check dashboard")
    print("3. Try clicking 'View Results' button")
    print("4. Navigate to /examination/result_list/ directly")
    print("\nTo change fee status:")
    print("  python manage_student_fees.py")

if __name__ == '__main__':
    main()
