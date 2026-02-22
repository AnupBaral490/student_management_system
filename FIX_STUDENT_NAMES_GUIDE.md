# Fix Student Names Display Guide

## Problem
Student names were not showing in the exam result entry form - only student IDs were visible.

## Root Cause
The `first_name` and `last_name` fields in the User model were not populated for student accounts. The system was using `get_full_name()` which returns an empty string when these fields are blank.

## Solution Applied

### 1. Updated Templates
Modified the following templates to properly display student names with fallback to username:
- `templates/examination/enter_results.html` - Exam result entry form
- `templates/examination/result_list.html` - Results listing

The templates now check if `first_name` or `last_name` exist, and if not, display the username instead.

### 2. Created Management Command
Created a management command to populate student names from their usernames:
- `accounts/management/commands/populate_student_names.py`

## How to Fix Existing Student Data

Run this command to populate first_name and last_name for all students:

```bash
python manage.py populate_student_names
```

This command will:
- Find all users with `user_type='student'`
- Skip students who already have first_name and last_name
- Split the username into first and last name
- Capitalize the names properly
- Save the updated user records

## Example Output
```
Updated: daji -> Daji 
Updated: bhola -> Bhola 
Updated: bisal -> Bisal 
Updated: darshan -> Darshan 

Successfully updated 4 student names!
```

## For Future Student Creation

When creating new students, make sure to populate the `first_name` and `last_name` fields in the User model, not just the username. This ensures proper display throughout the system.

## Alternative: Manual Update via Admin Panel

You can also manually update student names through the Django admin panel:
1. Go to Admin Panel → Users
2. Click on a student user
3. Fill in the "First name" and "Last name" fields
4. Save

## Template Pattern Used

The templates now use this pattern for displaying student names:

```django
{% if student.user.first_name or student.user.last_name %}
    {{ student.user.first_name }} {{ student.user.last_name }}
{% else %}
    {{ student.user.username }}
{% endif %}
```

This ensures names are always displayed, even if the first_name/last_name fields are empty.
