"""
Complete test of the parent-teacher messaging system
Tests both parent and teacher perspectives
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, ParentTeacherMessage

print("=" * 80)
print("COMPLETE PARENT-TEACHER MESSAGING SYSTEM TEST")
print("=" * 80)

# PART 1: PARENT PERSPECTIVE
print("\n" + "=" * 80)
print("PART 1: PARENT PERSPECTIVE")
print("=" * 80)

parent = User.objects.get(username='dajikopita')
print(f"\n✓ Parent: {parent.username}")

# Get parent's children
children = parent.parent_profile.children.all()
print(f"✓ Children: {children.count()}")
for child in children:
    print(f"  - {child.user.get_full_name()} (ID: {child.id})")

# Get parent's sent messages
sent_messages = ParentTeacherMessage.objects.filter(
    sender=parent
).order_by('-created_at')

print(f"\n✓ Messages sent by parent: {sent_messages.count()}")
for msg in sent_messages:
    print(f"  - To: {msg.recipient.get_full_name()} | Subject: {msg.subject} | Status: {msg.status}")

# PART 2: TEACHER PERSPECTIVE
print("\n" + "=" * 80)
print("PART 2: TEACHER PERSPECTIVE")
print("=" * 80)

teacher = User.objects.get(username='baral')
print(f"\n✓ Teacher: {teacher.username} ({teacher.get_full_name()})")

# Get teacher's received messages
received_messages = ParentTeacherMessage.objects.filter(
    recipient=teacher
).select_related('sender', 'student__user').order_by('-created_at')

print(f"\n✓ Messages received by teacher: {received_messages.count()}")

# Show unread messages
unread_messages = received_messages.filter(teacher_read=False)
print(f"✓ Unread messages: {unread_messages.count()}")

# Show messages for dashboard (last 5)
dashboard_messages = received_messages[:5]
print(f"\n✓ Messages shown on dashboard (last 5): {dashboard_messages.count()}")

print("\nDashboard Messages Preview:")
print("-" * 80)
for msg in dashboard_messages:
    status_icon = "🔵" if not msg.teacher_read else "✓"
    print(f"{status_icon} [{msg.status.upper()}] {msg.subject}")
    print(f"   From: {msg.sender.username} | About: {msg.student.user.get_full_name()}")
    print(f"   Preview: {msg.message[:60]}...")
    print(f"   Sent: {msg.created_at.strftime('%Y-%m-%d %H:%M')}")
    print("-" * 80)

# PART 3: MESSAGE FLOW VERIFICATION
print("\n" + "=" * 80)
print("PART 3: MESSAGE FLOW VERIFICATION")
print("=" * 80)

# Check if messages are properly linked
print("\n✓ Verifying message relationships:")
for msg in received_messages:
    sender_is_parent = msg.sender.user_type == 'parent'
    recipient_is_teacher = msg.recipient.user_type == 'teacher'
    has_student = msg.student is not None
    
    print(f"\nMessage ID {msg.id}:")
    print(f"  ✓ Sender is parent: {sender_is_parent}")
    print(f"  ✓ Recipient is teacher: {recipient_is_teacher}")
    print(f"  ✓ Has student reference: {has_student}")
    
    if has_student:
        # Check if student is child of sender
        is_child = msg.student in msg.sender.parent_profile.children.all()
        print(f"  ✓ Student is sender's child: {is_child}")
        
        # Check if teacher teaches this student
        from academic.models import TeacherSubjectAssignment
        enrollment = msg.student.get_current_enrollment()
        if enrollment:
            teaches_student = TeacherSubjectAssignment.objects.filter(
                teacher=msg.recipient.teacher_profile,
                class_assigned=enrollment.class_enrolled
            ).exists()
            print(f"  ✓ Teacher teaches this student: {teaches_student}")

# PART 4: FEATURE CHECKLIST
print("\n" + "=" * 80)
print("PART 4: FEATURE CHECKLIST")
print("=" * 80)

features = [
    ("Parent can view children", children.exists()),
    ("Parent can send messages", sent_messages.exists()),
    ("Teacher receives messages", received_messages.exists()),
    ("Messages have student reference", all(msg.student for msg in received_messages)),
    ("Unread status tracking", unread_messages.exists()),
    ("Message status tracking", all(msg.status in ['sent', 'read', 'replied'] for msg in received_messages)),
    ("Dashboard shows recent messages", dashboard_messages.count() > 0),
    ("Messages properly linked", all(msg.sender.user_type == 'parent' and msg.recipient.user_type == 'teacher' for msg in received_messages)),
]

print("\n✓ Feature Status:")
for feature, status in features:
    icon = "✓" if status else "✗"
    print(f"  {icon} {feature}")

# SUMMARY
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

all_passed = all(status for _, status in features)
if all_passed:
    print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("\nThe parent-teacher messaging system is fully functional:")
    print("  • Parents can send messages to teachers")
    print("  • Teachers can see messages on their dashboard")
    print("  • Messages are properly linked to students")
    print("  • Unread status is tracked")
    print("  • Message status is tracked (sent/read/replied)")
else:
    print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
    print("\nPlease review the failed features above.")

print("=" * 80)
