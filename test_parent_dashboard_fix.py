#!/usr/bin/env python
"""
Test script to verify parent dashboard is working correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import ParentProfile, StudentProfile
from fees.models import StudentFee

User = get_user_model()

def test_parent_dashboard():
    """Test parent dashboard data loading"""
    print("=" * 60)
    print("TESTING PARENT DASHBOARD")
    print("=" * 60)
    
    # Find a parent user
    parents = User.objects.filter(user_type='parent')
    
    if not parents.exists():
        print("❌ No parent users found in the system")
        return
    
    for parent in parents[:3]:  # Test first 3 parents
        print(f"\n{'='*60}")
        print(f"Testing Parent: {parent.username} - {parent.get_full_name()}")
        print(f"{'='*60}")
        
        try:
            parent_profile = parent.parent_profile
            print(f"✓ Parent profile found")
            
            # Get children
            children = parent_profile.children.all()
            print(f"✓ Children count: {children.count()}")
            
            for child in children:
                print(f"\n  Child: {child.user.get_full_name()}")
                print(f"  Student ID: {child.student_id}")
                
                # Check enrollment
                try:
                    enrollment = child.get_current_enrollment()
                    if enrollment:
                        print(f"  ✓ Enrolled in: {enrollment.class_enrolled.name}")
                    else:
                        print(f"  ⚠ No active enrollment")
                except Exception as e:
                    print(f"  ⚠ Enrollment error: {e}")
                
                # Check fees
                try:
                    unpaid_fees = StudentFee.objects.filter(
                        student=child,
                        payment_status__in=['pending', 'partial', 'overdue']
                    )
                    
                    if unpaid_fees.exists():
                        total_unpaid = sum(fee.balance_amount for fee in unpaid_fees)
                        print(f"  💰 Unpaid fees: ${total_unpaid:.2f} ({unpaid_fees.count()} items)")
                        for fee in unpaid_fees:
                            print(f"     - {fee.fee_structure}: ${fee.balance_amount:.2f} ({fee.payment_status})")
                    else:
                        print(f"  ✓ No unpaid fees")
                except Exception as e:
                    print(f"  ⚠ Fee check error: {e}")
            
            print(f"\n✅ Parent dashboard data loaded successfully for {parent.username}")
            
        except ParentProfile.DoesNotExist:
            print(f"❌ Parent profile not found for {parent.username}")
        except Exception as e:
            print(f"❌ Error loading parent dashboard: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == '__main__':
    test_parent_dashboard()
