# Exam Creation and Visibility Guide

## Overview
The examination system allows teachers to create exams that automatically appear on teacher, student, and parent dashboards.

## How It Works

### For Teachers:
1. Navigate to the "Examinations" section in the teacher dashboard
2. Click "Create New Exam"
3. Fill in the exam details:
   - **Exam Name**: Name of the examination
   - **Exam Type**: Select from available types (Mid-term, Final, Quiz, etc.)
   - **Subject**: Only subjects you teach will appear
   - **Class**: Only classes you're assigned to will appear
   - **Date & Time**: When the exam will be held
   - **Marks**: Total marks and passing marks
   - **Instructions**: Optional instructions for students
4. Click "Create Exam"

### Automatic Visibility:

#### Teacher Dashboard:
- All exams created by the teacher appear in the "Examinations" section
- Teachers can view, edit, and enter results for their exams
- Filter exams by type, subject, or class

#### Student Dashboard:
- Students see exams for their enrolled class
- Exams appear in the "Examinations" section
- Students can view:
  - Exam name and subject
  - Date and time
  - Total marks
  - Instructions
  - Status (Upcoming/Completed)

#### Parent Dashboard:
- Parents see exams for all their children's classes
- Can view exam schedules and results
- Receive notifications when results are published

## Current Implementation

### Database Flow:
```
Teacher creates exam
    ↓
Examination record created with:
    - created_by = teacher
    - class_for = selected class
    - subject = selected subject
    ↓
System automatically filters:
    - Teachers: See their own exams
    - Students: See exams for their enrolled class
    - Parents: See exams for their children's classes
```

### View Logic:

**Teacher View** (`examination/views.py`):
```python
exams = Examination.objects.filter(
    created_by=request.user.teacher_profile
).select_related('subject', 'exam_type', 'class_for')
```

**Student View** (`examination/views.py`):
```python
enrollment = request.user.student_profile.get_current_enrollment()
exams = Examination.objects.filter(
    class_for=enrollment.class_enrolled
).select_related('subject', 'exam_type', 'created_by__user')
```

**Parent View** (similar logic for children's classes)

## Features

### Exam Creation Form:
- ✓ Dynamic subject dropdown (only teacher's subjects)
- ✓ Dynamic class dropdown (only teacher's classes)
- ✓ Exam type selection
- ✓ Date and time validation
- ✓ Auto-calculate passing marks (40% of total)
- ✓ Instructions field

### Exam List:
- ✓ Filter by type, subject, class
- ✓ Status badges (Upcoming/Completed)
- ✓ Quick access to enter results
- ✓ Responsive table layout

### Automatic Features:
- ✓ Exams appear immediately after creation
- ✓ No manual publishing required
- ✓ Filtered by user role automatically
- ✓ Students only see their class exams
- ✓ Teachers only see their own exams

## Important Notes

### For Exam Visibility:
1. **Students must be enrolled** in the class where the exam is created
2. **Teacher must be assigned** to teach that subject in that class
3. **One active enrollment** per student (to avoid confusion)

### Best Practices:
1. Create exams well in advance
2. Include clear instructions
3. Set appropriate passing marks
4. Verify the correct class is selected
5. Enter results promptly after the exam

## Troubleshooting

### Exam Not Showing for Students:
- Check if student is enrolled in the correct class
- Verify the exam's `class_for` matches student's enrollment
- Ensure student has only ONE active enrollment

### Exam Not Showing for Teacher:
- Verify the teacher created the exam
- Check if teacher is logged in with correct account
- Ensure exam was saved successfully

### No Subjects/Classes in Dropdown:
- Teacher must have TeacherSubjectAssignment records
- Contact admin to assign subjects and classes to the teacher

## Testing

To test the complete flow:

1. **As Teacher**:
   - Log in as a teacher
   - Go to Examinations → Create New Exam
   - Fill in all details
   - Submit the form
   - Verify exam appears in "All Examinations"

2. **As Student**:
   - Log in as a student enrolled in the same class
   - Go to Examinations
   - Verify the exam appears in the list

3. **As Parent**:
   - Log in as a parent
   - Go to Examinations (if available)
   - Verify exams for children appear

## Files Modified

- `templates/examination/create_exam.html` - Updated to use Django form properly
- `examination/views.py` - Already has correct filtering logic
- `examination/forms.py` - Already filters subjects and classes by teacher

## Summary

✓ Exam creation form now uses real database data
✓ Subjects and classes are filtered by teacher's assignments
✓ Exams automatically appear on all relevant dashboards
✓ No additional configuration needed after creation
✓ System handles visibility based on user roles automatically
