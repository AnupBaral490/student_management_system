"""
Setup teachers for Daji's class
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, StudentProfile, TeacherProfile
from academic.models import TeacherSubjectAssignment, Subject, Class, StudentEnrollment

print("\n" + "="*70)
print("SETTING UP TEACHERS FOR DAJI'S CLASS")
print("="*70)

# Get Daji
daji = StudentProfile.objects.get(student_id='212')
print(f"\n✓ Found student: {daji.user.get_full_name()}")

# Get enrollment
enrollment = daji.get_current_enrollment()
if not enrollment:
    print("✗ Daji is not enrolled!")
    exit()

print(f"✓ Enrolled in: {enrollment.class_enrolled}")

# Get subjects for this class
subjects = Subject.objects.filter(
    course=enrollment.class_enrolled.course,
    year=enrollment.class_enrolled.year,
    semester=enrollment.class_enrolled.semester
)

print(f"\n📚 Subjects in this class: {subjects.count()}")
for subject in subjects:
    print(f"  - {subject.name} ({subject.code})")

# Get teachers
teachers = TeacherProfile.objects.all()
print(f"\n👨‍🏫 Available Teachers: {teachers.count()}")
for teacher in teachers:
    name = teacher.user.get_full_name() or teacher.user.username
    print(f"  - {name} (ID: {teacher.id})")

# Check existing assignments
existing_assignments = TeacherSubjectAssignment.objects.filter(
    class_assigned=enrollment.class_enrolled
)

print(f"\n📋 Existing Assignments: {existing_assignments.count()}")
for assignment in existing_assignments:
    teacher_name = assignment.teacher.user.get_full_name() or assignment.teacher.user.username
    print(f"  - {teacher_name} → {assignment.subject.name}")

# Create missing assignments
if teachers.exists() and subjects.exists():
    print("\n🔧 Creating/Updating Assignments...")
    
    # Use Baral Teacher (ID: 8) as the main teacher
    main_teacher = TeacherProfile.objects.get(id=8)
    print(f"Using teacher: {main_teacher.user.get_full_name()}")
    
    created_count = 0
    for subject in subjects:
        # Check if assignment exists
        assignment, created = TeacherSubjectAssignment.objects.get_or_create(
            teacher=main_teacher,
            subject=subject,
            class_assigned=enrollment.class_enrolled,
            defaults={'academic_year': enrollment.class_enrolled.academic_year}
        )
        
        if created:
            print(f"  ✓ Created: {main_teacher.user.get_full_name()} → {subject.name}")
            created_count += 1
        else:
            print(f"  - Already exists: {subject.name}")
    
    print(f"\n✓ Created {created_count} new assignments")
else:
    print("\n⚠️  Cannot create assignments - missing teachers or subjects")

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

# Verify assignments
final_assignments = TeacherSubjectAssignment.objects.filter(
    class_assigned=enrollment.class_enrolled
).select_related('teacher__user', 'subject')

print(f"\nTotal Assignments for {enrollment.class_enrolled}: {final_assignments.count()}")
for assignment in final_assignments:
    teacher_name = assignment.teacher.user.get_full_name() or assignment.teacher.user.username
    print(f"  ✓ {teacher_name} teaches {assignment.subject.name}")

print("\n" + "="*70 + "\n")
