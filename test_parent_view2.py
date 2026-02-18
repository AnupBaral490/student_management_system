"""
Test the parent dashboard view using Django test client
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.test import Client
from accounts.models import User

# Create a test client
client = Client()

# Get the parent user
parent_user = User.objects.get(username='dajikopita')

print("\n" + "="*70)
print("TESTING PARENT DASHBOARD VIEW WITH TEST CLIENT")
print("="*70)
print(f"\nUser: {parent_user.username}")
print(f"User Type: {parent_user.user_type}")

# Log in as the parent
client.force_login(parent_user)

try:
    # Make a request to the dashboard
    response = client.get('/accounts/dashboard/')
    
    print(f"\nResponse Status: {response.status_code}")
    
    # Check the context
    if response.context:
        context = response.context
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
                    print(f"  GPA: {child_info['gpa']}")
            else:
                print("\n⚠️  Children data is empty!")
                print("\nDebugging info:")
                if 'children_profiles' in context:
                    print(f"  Children Profiles: {context['children_profiles']}")
                    print(f"  Children Profiles Count: {context['children_profiles'].count()}")
        else:
            print("\n⚠️  'children_data' not in context!")
            print("\nAvailable context keys:")
            for key in context.keys():
                print(f"  - {key}")
    else:
        print("\n⚠️  Response has no context")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
