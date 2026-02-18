# Parent-Children Setup Guide

## Overview
The parent dashboard now displays real children data that is linked through the admin panel. Parents can see their children's academic information, attendance, and notifications.

## How to Link Children to Parents (Admin Panel)

### Step 1: Access the Admin Panel
1. Log in to the admin panel at `/admin/`
2. Navigate to **Accounts** → **Parent profiles**

### Step 2: Edit Parent Profile
1. Click on the parent profile you want to edit
2. You will see a section called **Children**
3. This section shows two boxes:
   - **Available student profiles** (left box)
   - **Chosen student profiles** (right box)

### Step 3: Add Children
1. In the **Available student profiles** box, find the student(s) you want to link
2. Select the student(s) by clicking on them
3. Click the **right arrow (→)** button to move them to **Chosen student profiles**
4. You can select multiple students by holding Ctrl (Windows) or Cmd (Mac)
5. Click **Save** at the bottom of the page

### Step 4: Remove Children (if needed)
1. In the **Chosen student profiles** box, select the student(s) you want to remove
2. Click the **left arrow (←)** button to move them back to **Available student profiles**
3. Click **Save**

## What Parents Will See

Once children are linked, parents will see on their dashboard:

### My Children Section
- Child's name and profile picture
- Student ID
- Current course and semester
- Attendance percentage (color-coded):
  - Green: ≥75%
  - Yellow: 50-74%
  - Red: <50%
- GPA (when available)

### Recent Notifications
- Notifications sent to their children
- Priority levels (High, Medium, Low)
- Timestamp

### Quick Actions
- View Attendance
- View Results
- All Notifications
- Contact Teachers
- Download Reports

## Features

### Real-Time Data
- Attendance is calculated from actual attendance records
- Enrollment information is pulled from the current academic year
- Notifications are fetched from the notifications system

### Multiple Children Support
- Parents can have multiple children linked
- Each child's information is displayed in a separate card
- All children's notifications are aggregated

### Empty State
If no children are linked, parents will see:
- A friendly message: "No Children Linked"
- Instructions to contact the administrator

## Technical Details

### Database Relationship
- `ParentProfile` has a ManyToMany relationship with `StudentProfile`
- Field name: `children`
- This allows one parent to have multiple children
- One child can have multiple parents (both mother and father)

### Data Displayed
- **Enrollment**: Current class, course, year, and semester
- **Attendance**: Calculated from AttendanceRecord model
- **Notifications**: Fetched from Notification model
- **GPA**: Placeholder for future examination system integration

## Troubleshooting

### Parent sees "No Children Linked"
- Check if children are added in the admin panel
- Verify the parent profile exists
- Ensure student profiles exist for the children

### Attendance shows 0%
- Check if attendance records exist for the student
- Verify the student is enrolled in a class
- Ensure attendance sessions have been created

### No notifications appear
- Check if notifications have been created for the students
- Verify notifications are not filtered out
- Ensure the notification system is working

## Next Steps

To enhance the parent dashboard further, consider:
1. Adding exam results and grades
2. Implementing parent-teacher messaging
3. Adding assignment tracking
4. Creating downloadable progress reports
5. Adding calendar integration for events
