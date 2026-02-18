"""
Test the parent dashboard view directly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from accounts.models import User
from accounts.views import dashboard

# Create a request factory
factory = RequestFactory()

# Get the parent user
parent_user = User.objects.get(username='dajikopita')

# Create a fake request
request = factory.get('/accounts/dashboard/')
request.user = parent_user

print("\n" + "="*70)
print("TESTING PARENT DASHBOARD VIEW")
print("="*70)
print(f"\nUser: {parent_user.username}")
print(f"User Type: {parent_user.user_type}")

try:
    # Call the view
    response = dashboard(request)
    
    print(f"\nResponse Status: {response.status_code}")
    
    # Check the context
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"\nContext Keys: {list(context.keys())}")
        
        if 'children_data' in context:
            children_data = context['children_data']
            print(f"\nChildren Data Count: {len(children_data)}")
            
            if len(children_data) > 0:
                print("\n✓ SUCCESS! Children data is present in context")
                for idx, child_info in enumerate(children_data, 1):
                    print(f"\nChild #{idx}:")
                    print(f"  Name: {child_info['user'].get_full_name()}")
                    print(f"  Student ID: {child_info['profile'].student_id}")
                    print(f"  Enrollment: {child_info['enrollment']}")
                    print(f"  Attendance: {child_info['attendance_percentage']}%")
                    print(f"  Subjects: {len(child_info['subjects'])}")
            else:
                print("\n⚠️  Children data is empty!")
        else:
            print("\n⚠️  'children_data' not in context!")
            
        if 'children_profiles' in context:
            print(f"\nChildren Profiles Count: {context['children_profiles'].count()}")
    else:
        print("\n⚠️  Response has no context_data")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
