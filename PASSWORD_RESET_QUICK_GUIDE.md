# Password Reset - Quick Reference

## ✅ FEATURE ALREADY EXISTS!

Admins can reset passwords for students, teachers, and parents.

## Quick Steps

### 1. Go to User Management
```
Sidebar → User Management
```

### 2. Find the User
- Filter by type (Student/Teacher/Parent)
- Search by name, username, or email

### 3. Click Reset Password
- Click the **key icon** (🔑) in Actions column

### 4. Set New Password
- Click "Generate Strong Password" (recommended)
- Or enter password manually (min 8 characters)
- Click "Copy" to copy password
- Click "Reset Password" button

### 5. Share with User
- Give the new password to the user
- User can log in immediately

## Visual Guide

```
User List Page:
┌────────────────────────────────────────┐
│ Name    | Type    | Actions           │
├────────────────────────────────────────┤
│ John    | Student | [✏️] [🔑] [🗑️]   │
│ Jane    | Teacher | [✏️] [🔑] [🗑️]   │
│ Bob     | Parent  | [✏️] [🔑] [🗑️]   │
└────────────────────────────────────────┘
                      ↑
                Click this key icon
```

```
Reset Password Page:
┌────────────────────────────────────────┐
│           [👤 User Photo]              │
│           John Doe                     │
│           Student                      │
├────────────────────────────────────────┤
│ New Password: [____________]           │
│ [Generate] [Show] [Copy]               │
│                                        │
│ Confirm: [____________]                │
│ [Show]                                 │
├────────────────────────────────────────┤
│         [Cancel] [Reset Password]      │
└────────────────────────────────────────┘
```

## Button Functions

| Button | Function |
|--------|----------|
| **Generate** | Creates strong 12-char password |
| **Show** | Reveals password text |
| **Copy** | Copies password to clipboard |
| **Reset Password** | Saves new password |

## URLs

```
User List: /accounts/admin/users/
Reset Password: /accounts/admin/users/<user_id>/reset-password/
```

## Password Requirements

✅ Minimum 8 characters
✅ Mix of letters and numbers
✅ Avoid common passwords

## Tips

💡 **Use "Generate Strong Password"** - Creates secure password automatically
💡 **Click "Copy"** - Easy to share with user
💡 **Tell user to change password** - After first login
💡 **Verify user identity** - Before resetting

## Common Scenarios

### Student Forgot Password
1. Filter by "Student"
2. Find student
3. Click key icon (🔑)
4. Generate password
5. Copy and share

### Teacher Forgot Password
1. Filter by "Teacher"
2. Find teacher
3. Click key icon (🔑)
4. Generate password
5. Copy and share

### Parent Forgot Password
1. Filter by "Parent"
2. Find parent
3. Click key icon (🔑)
4. Generate password
5. Copy and share

## Security Notes

🔒 Only admins can reset passwords
🔒 Passwords are encrypted
🔒 Share passwords securely
🔒 Recommend users change password after reset

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't find user | Check filters and search |
| Button not visible | Verify admin login |
| Password too short | Use Generate or add more chars |
| Passwords don't match | Use Generate or retype carefully |
| User can't login | Verify password copied correctly |

## Example Workflow

```
Admin Login
    ↓
User Management
    ↓
Filter/Search User
    ↓
Click Key Icon (🔑)
    ↓
Generate Password
    ↓
Copy Password
    ↓
Reset Password
    ↓
Share with User
    ↓
User Logs In
```

## That's It!

The feature is ready to use. Just navigate to User Management and click the key icon next to any user! 🎉
