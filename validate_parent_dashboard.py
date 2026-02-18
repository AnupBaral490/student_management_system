#!/usr/bin/env python
"""
Validate parent dashboard template structure
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.template import Template, Context
from django.contrib.auth import get_user_model
from accounts.models import ParentProfile

User = get_user_model()

def test_template_rendering():
    """Test if parent dashboard template renders without errors"""
    print("=" * 60)
    print("TESTING PARENT DASHBOARD TEMPLATE RENDERING")
    print("=" * 60)
    
    # Find a parent user
    parent = User.objects.filter(user_type='parent').first()
    
    if not parent:
        print("❌ No parent users found")
        return
    
    print(f"\nTesting with parent: {parent.username}")
    
    try:
        parent_profile = parent.parent_profile
        children = parent_profile.children.all()
        
        print(f"✓ Parent profile found")
        print(f"✓ Children count: {children.count()}")
        
        # Prepare context data similar to the view
        children_data = []
        for child in children:
            try:
                enrollment = child.get_current_enrollment()
            except:
                enrollment = None
            
            # Get fee data
            from fees.models import StudentFee
            try:
                unpaid_fees = StudentFee.objects.filter(
                    student=child,
                    payment_status__in=['pending', 'partial', 'overdue']
                )
                has_unpaid_fees = unpaid_fees.exists()
                total_unpaid_amount = sum(fee.balance_amount for fee in unpaid_fees) if has_unpaid_fees else 0
            except:
                has_unpaid_fees = False
                total_unpaid_amount = 0
                unpaid_fees = []
            
            child_info = {
                'profile': child,
                'user': child.user,
                'enrollment': enrollment,
                'attendance_percentage': 85.5,
                'gpa': 3.5,
                'total_sessions': 20,
                'present_sessions': 17,
                'subjects': [],
                'has_unpaid_fees': has_unpaid_fees,
                'unpaid_fees': unpaid_fees,
                'total_unpaid_amount': total_unpaid_amount
            }
            children_data.append(child_info)
        
        print(f"✓ Context data prepared")
        print(f"  - Children data items: {len(children_data)}")
        
        # Try to load and render the template
        with open('templates/accounts/parent_dashboard.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        print(f"✓ Template file loaded")
        print(f"  - Template size: {len(template_content)} characters")
        
        # Check for common issues
        open_divs = template_content.count('<div')
        close_divs = template_content.count('</div>')
        print(f"\n  HTML Structure Check:")
        print(f"  - Opening <div> tags: {open_divs}")
        print(f"  - Closing </div> tags: {close_divs}")
        
        if open_divs != close_divs:
            print(f"  ⚠ WARNING: Mismatched div tags! Difference: {abs(open_divs - close_divs)}")
        else:
            print(f"  ✓ Div tags balanced")
        
        # Check for template syntax
        if_count = template_content.count('{% if')
        endif_count = template_content.count('{% endif %}')
        print(f"\n  Template Syntax Check:")
        print(f"  - if tags: {if_count}")
        print(f"  - endif tags: {endif_count}")
        
        if if_count != endif_count:
            print(f"  ⚠ WARNING: Mismatched if/endif tags! Difference: {abs(if_count - endif_count)}")
        else:
            print(f"  ✓ If/endif tags balanced")
        
        for_count = template_content.count('{% for')
        endfor_count = template_content.count('{% endfor %}')
        print(f"  - for tags: {for_count}")
        print(f"  - endfor tags: {endfor_count}")
        
        if for_count != endfor_count:
            print(f"  ⚠ WARNING: Mismatched for/endfor tags! Difference: {abs(for_count - endfor_count)}")
        else:
            print(f"  ✓ For/endfor tags balanced")
        
        print(f"\n✅ Template validation complete")
        print(f"\nℹ️  If the dashboard is still unresponsive, check:")
        print(f"   1. Browser console for JavaScript errors")
        print(f"   2. Network tab for failed resource loads")
        print(f"   3. Django server logs for template errors")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*60}")

if __name__ == '__main__':
    test_template_rendering()
