"""
Create sample exam results for Daji to populate the performance chart
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, StudentProfile, TeacherProfile
from academic.models import Subject
from examination.models import Examination, ExamType, ExamResult
from django.utils import timezone
from datetime import timedelta
import random

print("=" * 80)
print("CREATING SAMPLE EXAM RESULTS")
print("=" * 80)

# Get student
child = StudentProfile.objects.get(id=33)
print(f"\n✓ Student: {child.user.get_full_name()} (ID: {child.id})")

# Get enrollment
enrollment = child.get_current_enrollment()
if not enrollment:
    print("✗ No enrollment found!")
    exit(1)

print(f"✓ Enrollment: {enrollment.class_enrolled}")

# Get subjects
subjects = Subject.objects.filter(
    course=enrollment.class_enrolled.course,
    year=enrollment.class_enrolled.year,
    semester=enrollment.class_enrolled.semester
)

print(f"✓ Subjects: {subjects.count()}")

# Get or create exam type
exam_type, created = ExamType.objects.get_or_create(
    name="Mid-term Exam",
    defaults={'description': 'Mid-semester examination'}
)
print(f"\n✓ Exam Type: {exam_type.name} {'(created)' if created else '(existing)'}")

# Get a teacher
teacher = TeacherProfile.objects.first()
if not teacher:
    print("✗ No teacher found!")
    exit(1)

print(f"✓ Teacher: {teacher.user.get_full_name()}")

# Create exams and results for each subject
exam_date = timezone.now().date() - timedelta(days=30)

print("\n" + "=" * 80)
print("CREATING EXAMS AND RESULTS")
print("=" * 80)

for subject in subjects:
    print(f"\nSubject: {subject.name}")
    
    # Check if exam already exists
    existing_exam = Examination.objects.filter(
        subject=subject,
        exam_type=exam_type,
        class_for=enrollment.class_enrolled
    ).first()
    
    if existing_exam:
        exam = existing_exam
        print(f"  ✓ Using existing exam (ID: {exam.id})")
    else:
        # Create examination
        exam = Examination.objects.create(
            name=f"{exam_type.name} - {subject.name}",
            subject=subject,
            exam_type=exam_type,
            class_for=enrollment.class_enrolled,
            created_by=teacher,
            exam_date=exam_date,
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=2)).time(),
            total_marks=100,
            passing_marks=40,
            instructions="Complete all questions"
        )
        print(f"  ✓ Created exam (ID: {exam.id})")
    
    # Check if result already exists
    existing_result = ExamResult.objects.filter(
        student=child,
        examination=exam
    ).first()
    
    if existing_result:
        print(f"  ✓ Result already exists: {existing_result.marks_obtained}/100 ({existing_result.grade})")
    else:
        # Generate random marks (60-95 for variety)
        marks = random.randint(60, 95)
        
        # Create result (grade will be auto-calculated by save method)
        result = ExamResult.objects.create(
            student=child,
            examination=exam,
            marks_obtained=marks,
            grade='A',  # Will be overridden by save()
            entered_by=teacher,
            remarks=f"Good performance in {subject.name}"
        )
        
        print(f"  ✓ Created result: {marks}/100 ({result.grade})")

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Verify results
all_results = ExamResult.objects.filter(student=child)
print(f"\n✓ Total exam results for {child.user.get_full_name()}: {all_results.count()}")

print("\nResults summary:")
for result in all_results:
    percentage = (result.marks_obtained / result.examination.total_marks * 100)
    print(f"  - {result.examination.subject.name}: {result.marks_obtained}/{result.examination.total_marks} ({percentage:.1f}%) - Grade: {result.grade}")

print("\n" + "=" * 80)
print("✓✓✓ SAMPLE DATA CREATED SUCCESSFULLY ✓✓✓")
print("=" * 80)
print("\nThe performance chart should now display data!")
print("Refresh the parent dashboard to see the results.")
