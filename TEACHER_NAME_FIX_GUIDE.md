# Teacher Name Display Fix

## Problem
In the parent dashboard "Contact Teachers" section, teacher IDs (like 112, 202, 332) were showing instead of teacher names.

## Root Cause
Teachers' User accounts didn't have `first_name` and `last_name` fields populated. When Django's `get_full_name()` method is called on a User without these fields, it returns an empty string.

## Solution Applied

### 1. Template Fix
Updated `templates/accounts/contact_teachers.html` to:
- Display username as fallback if first_name/last_name are empty
- Show "ID: " prefix before employee_id for clarity

### 2. Management Command
Created `fix_teacher_names.py` command to automatically populate teacher names from usernames.

## How to Fix Teacher Names

### Option 1: Run the Management Command (Recommended)
```bash
python manage.py fix_teacher_names
```

This will:
- Find all teachers with empty first_name/last_name
- Split username by underscore (e.g., "john_doe" → "John Doe")
- Set appropriate first_name and last_name
- Display results for verification

### Option 2: Manual Fix via Django Admin
1. Go to Django Admin: http://localhost:8000/admin/
2. Navigate to "Users"
3. Filter by user_type = "teacher"
4. For each teacher:
   - Click to edit
   - Fill in "First name" and "Last name" fields
   - Save

### Option 3: Manual Fix via Django Shell
```python
python manage.py shell

from accounts.models import User, TeacherProfile

# Example: Fix a specific teacher
teacher_user = User.objects.get(username='teacher_username')
teacher_user.first_name = 'John'
teacher_user.last_name = 'Doe'
teacher_user.save()

# Or fix all teachers at once
for teacher in TeacherProfile.objects.all():
    user = teacher.user
    if not user.first_name:
        # Set appropriate names
        user.first_name = 'Teacher'
        user.last_name = teacher.employee_id
        user.save()
```

## Verification
After fixing, visit the parent dashboard and click "Contact Teachers". You should now see:
- Teacher's full name (e.g., "John Doe")
- Employee ID below the name (e.g., "ID: 112")
- Profile picture or avatar icon

## Prevention
When creating new teachers, always ensure:
1. Set first_name and last_name in the User model
2. Or use a username that can be split into meaningful names
3. Consider adding validation in the teacher creation form

## Files Modified
- `templates/accounts/contact_teachers.html` - Template fix for teacher name display
- `templates/accounts/send_message.html` - Template fix for teacher dropdown
- `templates/accounts/student_dashboard.html` - Template fix for class teacher display
- `accounts/management/commands/fix_teacher_names.py` - New management command

## What Was Fixed

### Before
- Teacher IDs (112, 202, 332) were showing instead of names
- Empty spaces where teacher names should appear
- Confusing display for parents

### After
- Teacher names display properly (e.g., "John Doe")
- Username shows as fallback if first_name/last_name are empty
- Employee ID shows with "ID: " prefix for clarity
- Consistent display across all parent and student views
