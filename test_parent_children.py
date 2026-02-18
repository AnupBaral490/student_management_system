from accounts.models import User, ParentProfile, StudentProfile
from attendance.models import AttendanceRecord

parent_user = User.objects.get(username='parent1')
parent_profile = parent_user.parent_profile
children = parent_profile.children.all()

print('Parent:', parent_user.username)
print('Children count:', children.count())
print('Children:', list(children))

for child in children:
    print(f'\nChild: {child}')
    print(f'  User: {child.user}')
    print(f'  Username: {child.user.username}')
    print(f'  Full name: {child.user.get_full_name()}')
    
    # Test enrollment
    enrollment = child.get_current_enrollment()
    print(f'  Enrollment: {enrollment}')
    
    # Test attendance
    attendance_records = AttendanceRecord.objects.filter(student=child)
    print(f'  Attendance records: {attendance_records.count()}')
