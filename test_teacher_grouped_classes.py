#!/usr/bin/env python
"""
Test script to visualize how teacher classes will be grouped by semester
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from accounts.models import User, TeacherProfile
from academic.models import TeacherSubjectAssignment, StudentEnrollment
from collections import defaultdict

def test_grouped_classes():
    print("=" * 80)
    print("TEACHER DASHBOARD - GROUPED BY CLASS/SEMESTER")
    print("=" * 80)
    
    # Find teacher baral
    try:
        teacher_user = User.objects.get(username='baral')
        teacher_profile = teacher_user.teacher_profile
        
        print(f"\nTeacher: {teacher_user.get_full_name() or teacher_user.username}")
        print("=" * 80)
        
        # Get teacher's assignments
        teacher_assignments = TeacherSubjectAssignment.objects.filter(
            teacher=teacher_profile
        ).select_related('subject', 'class_assigned').order_by('class_assigned__name')
        
        # Group by class name
        grouped_classes = defaultdict(list)
        for assignment in teacher_assignments:
            grouped_classes[assignment.class_assigned.name].append(assignment)
        
        print(f"\nTotal Classes: {len(grouped_classes)}")
        print(f"Total Subjects: {teacher_assignments.count()}")
        print("=" * 80)
        
        # Display grouped
        for class_name, assignments in grouped_classes.items():
            print(f"\n╔{'═' * 78}╗")
            print(f"║ {class_name:^76} ║")
            print(f"╠{'═' * 78}╣")
            
            # Get student count for this class
            first_assignment = assignments[0]
            student_count = StudentEnrollment.objects.filter(
                class_enrolled=first_assignment.class_assigned,
                is_active=True
            ).count()
            
            print(f"║ 📚 {len(assignments)} Subjects  •  👥 {student_count} Students{' ' * (76 - len(f'{len(assignments)} Subjects  •  {student_count} Students') - 6)}║")
            print(f"╠{'═' * 78}╣")
            
            # Display subjects in this class
            for idx, assignment in enumerate(assignments, 1):
                print(f"║                                                                              ║")
                print(f"║  {idx}. {assignment.subject.name:<70} ║")
                print(f"║     Section: {assignment.class_assigned.section:<62} ║")
                print(f"║                                                                              ║")
                print(f"║     [View Students]  [Mark Attendance]  [Create Assignment]  [View Exams]   ║")
                
                if idx < len(assignments):
                    print(f"║     {'-' * 70}   ║")
            
            print(f"╚{'═' * 78}╝")
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        for class_name, assignments in grouped_classes.items():
            print(f"\n{class_name}:")
            for assignment in assignments:
                print(f"  • {assignment.subject.name}")
        
    except User.DoesNotExist:
        print("\nTeacher 'baral' not found.")

if __name__ == '__main__':
    test_grouped_classes()
