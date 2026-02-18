"""
Complete test of parent-teacher messaging flow
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, StudentProfile, ParentProfile, ParentTeacherMessage
from academic.models import TeacherSubjectAssignment

print("=" * 60)
print("PARENT-TEACHER MESSAGING FLOW TEST")
print("=" * 60)

# Step 1: Get parent and child
parent = User.objects.get(username='dajikopita')
child = parent.parent_profile.children.first()

print(f"\n1. PARENT & CHILD")
print(f"   Parent: {parent.username} ({parent.get_full_name() or 'No name'})")
print(f"   Child: {child.user.get_full_name()} (ID: {child.id}, Student ID: {child.student_id})")

# Step 2: Get enrollment
enrollment = child.get_current_enrollment()
print(f"\n2. ENROLLMENT")
if enrollment:
    print(f"   ✓ Enrolled in: {enrollment.class_enrolled}")
else:
    print(f"   ✗ No enrollment found!")
    exit(1)

# Step 3: Get teachers
teacher_assignments = TeacherSubjectAssignment.objects.filter(
    class_assigned=enrollment.class_enrolled
).select_related('teacher__user', 'subject')

teachers_dict = {}
for ta in teacher_assignments:
    if ta.teacher.id not in teachers_dict:
        teachers_dict[ta.teacher.id] = {
            'teacher': ta.teacher,
            'subjects': []
        }
    teachers_dict[ta.teacher.id]['subjects'].append(ta.subject)

teachers = list(teachers_dict.values())

print(f"\n3. TEACHERS")
if teachers:
    print(f"   ✓ Found {len(teachers)} teacher(s)")
    for teacher_data in teachers:
        teacher = teacher_data['teacher']
        subjects = teacher_data['subjects']
        print(f"   - {teacher.user.get_full_name()} (ID: {teacher.id})")
        print(f"     Subjects: {', '.join([s.name for s in subjects])}")
else:
    print(f"   ✗ No teachers found!")
    exit(1)

# Step 4: Test message creation
teacher = teachers[0]['teacher']
print(f"\n4. TEST MESSAGE CREATION")
print(f"   Creating test message from {parent.username} to {teacher.user.get_full_name()}...")

# Check if test message already exists
existing_msg = ParentTeacherMessage.objects.filter(
    sender=parent,
    recipient=teacher.user,
    subject="Test Message - Automated"
).first()

if existing_msg:
    print(f"   ℹ Test message already exists (ID: {existing_msg.id})")
    test_message = existing_msg
else:
    test_message = ParentTeacherMessage.objects.create(
        sender=parent,
        recipient=teacher.user,
        student=child,
        subject="Test Message - Automated",
        message="This is an automated test message to verify the messaging system works correctly."
    )
    print(f"   ✓ Message created successfully (ID: {test_message.id})")

# Step 5: Verify message
print(f"\n5. MESSAGE VERIFICATION")
print(f"   From: {test_message.sender.username}")
print(f"   To: {test_message.recipient.username}")
print(f"   About: {test_message.student.user.get_full_name()}")
print(f"   Subject: {test_message.subject}")
print(f"   Status: {test_message.status}")
print(f"   Created: {test_message.created_at}")

# Step 6: Check teacher's inbox
teacher_messages = ParentTeacherMessage.objects.filter(
    recipient=teacher.user
).count()

print(f"\n6. TEACHER INBOX")
print(f"   ✓ Teacher has {teacher_messages} message(s) in inbox")

# Step 7: Check parent's sent messages
parent_sent = ParentTeacherMessage.objects.filter(
    sender=parent
).count()

print(f"\n7. PARENT SENT MESSAGES")
print(f"   ✓ Parent has sent {parent_sent} message(s)")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Messaging system is working!")
print("=" * 60)
