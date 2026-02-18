# Student Dashboard - Upcoming Exams Feature

## Overview
Added an "Upcoming Exams" section to the student dashboard that displays all scheduled exams for the student's enrolled class.

## Changes Made

### 1. Backend (accounts/views.py)
Added upcoming exams query to the student dashboard view:

```python
# Get upcoming exams
from examination.models import Examination
upcoming_exams = Examination.objects.filter(
    class_for=enrollment.class_enrolled,
    exam_date__gte=django_timezone.now().date()
).select_related('subject', 'exam_type').order_by('exam_date', 'start_time')[:5]
```

**Features:**
- Filters exams by student's enrolled class
- Shows only future exams (exam_date >= today)
- Orders by date and time (earliest first)
- Limits to 5 most recent upcoming exams
- Includes related subject and exam type data

### 2. Frontend (templates/accounts/student_dashboard.html)

#### Added Upcoming Exams Section:
- Full-width card with gradient header
- Responsive table layout showing:
  - Exam name and subject
  - Exam type badge
  - Date and time
  - Total marks
  - Status (Today/Upcoming)
- "View All" button linking to full exam list
- Empty state when no exams scheduled

#### Updated Quick Actions:
- Added "Upcoming Exams" quick action button
- Purple gradient icon for visual distinction
- Links directly to exam list page

#### Added CSS Styles:
- `.exam-icon-modern` - Icon styling for exam entries
- `.bg-purple` - Purple gradient background for exam button

## Features

### Exam Display:
- ✓ Shows exam name and subject
- ✓ Displays exam type (Mid-term, Final, Quiz, etc.)
- ✓ Shows date in readable format (e.g., "Feb 15, 2026")
- ✓ Displays time range (e.g., "9:00 AM - 11:00 AM")
- ✓ Shows total marks
- ✓ Status badge:
  - Red "Today" badge for exams happening today
  - Yellow "Upcoming" badge for future exams

### User Experience:
- ✓ Clean, modern table layout
- ✓ Responsive design (works on mobile)
- ✓ Visual icons for better readability
- ✓ Quick access from dashboard
- ✓ Empty state message when no exams
- ✓ "View All" link to see complete exam list

## How It Works

### For Students:
1. Log in to student dashboard
2. Scroll to "Upcoming Exams" section
3. View all scheduled exams for your class
4. Click "View All" to see complete exam list with past exams
5. Use "Upcoming Exams" quick action for fast access

### Automatic Updates:
- Exams appear automatically when created by teachers
- Only shows exams for student's enrolled class
- Updates in real-time (no caching)
- Sorted by date (earliest first)

## Data Flow

```
Teacher creates exam
    ↓
Exam saved with class_for = student's class
    ↓
Student dashboard queries:
    - Filter by class_for = student's enrollment
    - Filter by exam_date >= today
    - Order by exam_date, start_time
    ↓
Display in "Upcoming Exams" section
```

## Example Display

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 Upcoming Exams                          [View All →]     │
├─────────────────────────────────────────────────────────────┤
│ Exam Name      │ Type    │ Date        │ Time      │ Marks │
├─────────────────────────────────────────────────────────────┤
│ 📄 Mid-term    │ Mid-term│ Feb 15, 2026│ 9:00 AM - │ 100   │
│    Sociology   │         │             │ 11:00 AM  │       │
├─────────────────────────────────────────────────────────────┤
│ 📄 Final Exam  │ Final   │ Feb 20, 2026│ 2:00 PM - │ 150   │
│    Database    │         │             │ 4:30 PM   │       │
└─────────────────────────────────────────────────────────────┘
```

## Benefits

### For Students:
- Clear visibility of upcoming exams
- Easy exam schedule planning
- Quick access from dashboard
- No need to navigate multiple pages
- See all important exam details at a glance

### For Teachers:
- Students are better informed
- Reduced questions about exam schedules
- Better exam preparation by students

### For Parents:
- Can see children's exam schedules (if parent dashboard is implemented)
- Better support for exam preparation

## Testing

To test the feature:

1. **Create an exam as teacher:**
   - Log in as teacher
   - Create exam for a specific class
   - Set exam date to future date

2. **View as student:**
   - Log in as student enrolled in that class
   - Go to dashboard
   - Verify exam appears in "Upcoming Exams" section

3. **Test edge cases:**
   - No exams: Should show empty state
   - Exam today: Should show "Today" badge
   - Past exam: Should NOT appear in upcoming exams
   - Multiple exams: Should show in chronological order

## Files Modified

1. `accounts/views.py` - Added upcoming_exams query
2. `templates/accounts/student_dashboard.html` - Added exams section and quick action
3. Both files updated with proper error handling for missing enrollments

## Future Enhancements

Potential improvements:
- Add countdown timer for exams
- Show exam instructions preview
- Add calendar view of exams
- Email/SMS reminders for upcoming exams
- Show exam preparation resources
- Display exam results after completion

## Summary

✓ Upcoming exams now visible on student dashboard
✓ Shows next 5 upcoming exams
✓ Clean, modern table layout
✓ Quick action button for easy access
✓ Automatic updates when teachers create exams
✓ Responsive design for all devices
