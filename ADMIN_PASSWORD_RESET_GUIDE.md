# Admin Password Reset Guide

## ✅ ALREADY IMPLEMENTED

The admin password reset functionality is already fully implemented in your system! Admins can reset passwords for any user (students, teachers, parents).

## How It Works

### For Admins:

1. **Navigate to User Management**
   - Go to Admin Dashboard
   - Click "User Management" in sidebar
   - Or visit: `/accounts/admin/users/`

2. **Find the User**
   - Use filters to find user by type (Student/Teacher/Parent)
   - Use search to find by name, username, or email
   - Browse the user list

3. **Reset Password**
   - Click the **key icon** (🔑) in the Actions column
   - Or click "Reset Password" button
   - You'll be taken to the password reset page

4. **Set New Password**
   - Enter new password (minimum 8 characters)
   - Confirm the password
   - Click "Reset Password" button

5. **Inform the User**
   - Give the new password to the user
   - User can log in with the new password
   - Recommend user to change password after first login

## Features

### Password Reset Page Features:

#### 1. User Information Display
- Profile picture
- Full name
- Username
- Email address
- User type (Student/Teacher/Parent)
- Last login time

#### 2. Password Generation Tools
- **Generate Strong Password**: Auto-generates a secure 12-character password
- **Show/Hide Password**: Toggle visibility of password fields
- **Copy to Clipboard**: Copy generated password for easy sharing

#### 3. Password Requirements
- Minimum 8 characters long
- Mix of letters and numbers recommended
- Avoid common passwords

#### 4. Real-time Validation
- Password strength indicator
- Password match confirmation
- Visual feedback (green/red borders)

#### 5. Security Features
- Only admins can access
- Confirmation required
- Success message after reset
- Audit trail (last login tracking)

## Step-by-Step Guide

### Scenario: Student Forgot Password

1. **Admin logs in** to the system
2. **Navigate to User Management**:
   ```
   Sidebar → User Management
   ```

3. **Filter for Students**:
   - Select "Student" from User Type dropdown
   - Click "Filter" button

4. **Find the Student**:
   - Use search box to find by name
   - Or browse the list

5. **Click Reset Password**:
   - Click the key icon (🔑) in Actions column
   - Student's details will be displayed

6. **Generate New Password**:
   - Click "Generate Strong Password" button
   - A secure password is automatically created
   - Click "Copy" to copy password

7. **Confirm Password**:
   - Password is auto-filled in both fields
   - Click "Reset Password" button

8. **Share with Student**:
   - Give the new password to the student
   - Student can now log in

### Scenario: Teacher Forgot Password

Same process as above, but:
- Filter by "Teacher" user type
- Find the teacher
- Reset password
- Share new password with teacher

### Scenario: Parent Forgot Password

Same process as above, but:
- Filter by "Parent" user type
- Find the parent
- Reset password
- Share new password with parent

## URL Structure

```
Base URL: /accounts/admin/users/

User List: /accounts/admin/users/
Reset Password: /accounts/admin/users/<user_id>/reset-password/
```

## Example URLs

```
User List: http://127.0.0.1:8000/accounts/admin/users/
Reset for User ID 5: http://127.0.0.1:8000/accounts/admin/users/5/reset-password/
```

## Screenshots Guide

### 1. User Management Page
```
┌─────────────────────────────────────────────────┐
│ Manage Users                    [+ Add New User]│
├─────────────────────────────────────────────────┤
│ Filters:                                        │
│ [User Type ▼] [Search...] [Filter]             │
├─────────────────────────────────────────────────┤
│ Profile | Name | Username | Type | Actions     │
├─────────────────────────────────────────────────┤
│ [👤]   | John | john123  | 🔵   | [✏️][🔑][🗑️]│
│ [👤]   | Jane | jane456  | 🟢   | [✏️][🔑][🗑️]│
└─────────────────────────────────────────────────┘
                                    ↑
                              Reset Password
```

### 2. Reset Password Page
```
┌─────────────────────────────────────────────────┐
│ Reset Password              [← Back to Users]  │
├─────────────────────────────────────────────────┤
│                   [👤 Photo]                    │
│                   John Doe                      │
│              Student • john@email.com           │
├─────────────────────────────────────────────────┤
│ ⚠️ Password Reset Warning                      │
│ You are about to reset password for this user  │
├─────────────────────────────────────────────────┤
│ User Details:                                   │
│ • Username: john123                             │
│ • Email: john@email.com                         │
│ • Type: Student                                 │
│ • Last Login: Feb 16, 2026 10:30 AM            │
├─────────────────────────────────────────────────┤
│ New Password: [____________]                    │
│ [Generate] [Show] [Copy]                        │
│                                                 │
│ Confirm Password: [____________]                │
│ [Show]                                          │
├─────────────────────────────────────────────────┤
│ ℹ️ Password Requirements:                      │
│ • Minimum 8 characters                          │
│ • Mix of letters and numbers                    │
│ • Avoid common passwords                        │
├─────────────────────────────────────────────────┤
│                    [Cancel] [Reset Password]    │
└─────────────────────────────────────────────────┘
```

## Button Functions

### Generate Strong Password
- **Function**: Creates a random 12-character password
- **Characters**: Letters (a-z, A-Z), Numbers (0-9), Symbols (!@#$%^&*)
- **Auto-fill**: Fills both password fields
- **Visual**: Shows success message

### Show/Hide Password
- **Function**: Toggles password visibility
- **Icon**: Eye (👁️) when hidden, Eye-slash (👁️‍🗨️) when visible
- **Text**: Changes from "Show" to "Hide"

### Copy to Clipboard
- **Function**: Copies password to clipboard
- **Visual**: Shows "Password copied!" message
- **Use**: Easy sharing with user

## Security Considerations

### Access Control:
✅ Only admins can reset passwords
✅ User authentication required
✅ Permission checks enforced

### Password Security:
✅ Passwords are hashed (not stored in plain text)
✅ Strong password generation available
✅ Minimum length requirement (8 characters)
✅ Password confirmation required

### Audit Trail:
✅ Last login time tracked
✅ Success messages logged
✅ Admin action recorded

## Best Practices

### For Admins:

1. **Verify User Identity**
   - Confirm user's identity before resetting
   - Check email or student ID

2. **Use Strong Passwords**
   - Use the "Generate Strong Password" feature
   - Don't use simple passwords like "12345678"

3. **Secure Communication**
   - Share password securely (in person, phone, secure message)
   - Don't email passwords in plain text

4. **Recommend Password Change**
   - Tell user to change password after first login
   - Explain how to change password in profile settings

5. **Document the Reset**
   - Keep a log of password resets
   - Note date, time, and reason

### For Users:

1. **Change Password After Reset**
   - Log in with new password
   - Go to Profile → Change Password
   - Set a personal password

2. **Use Strong Passwords**
   - Mix of uppercase and lowercase
   - Include numbers and symbols
   - Avoid personal information

3. **Keep Password Secure**
   - Don't share with others
   - Don't write it down
   - Use password manager if needed

## Troubleshooting

### Issue: Can't find user
**Solution**: 
- Check user type filter
- Try searching by username or email
- Verify user exists in system

### Issue: Password reset button not visible
**Solution**:
- Verify you're logged in as admin
- Check user permissions
- Refresh the page

### Issue: Password doesn't meet requirements
**Solution**:
- Use "Generate Strong Password" button
- Ensure minimum 8 characters
- Include letters and numbers

### Issue: Passwords don't match
**Solution**:
- Re-type both passwords carefully
- Use "Show" button to verify
- Use "Generate" to auto-fill both

### Issue: User can't log in with new password
**Solution**:
- Verify password was copied correctly
- Check for extra spaces
- Try resetting again
- Verify user is active

## Files Involved

### Backend:
- `accounts/views.py` - `admin_reset_password()` function
- `accounts/forms.py` - `AdminPasswordResetForm` class
- `accounts/urls.py` - URL routing

### Frontend:
- `templates/accounts/admin_user_list.html` - User list with reset button
- `templates/accounts/admin_reset_password.html` - Reset password form

### Features:
- Password generation
- Password visibility toggle
- Clipboard copy
- Real-time validation
- Success messages

## Testing the Feature

### Test Steps:

1. **Login as Admin**
   ```
   Username: admin
   Password: [your admin password]
   ```

2. **Navigate to User Management**
   ```
   Dashboard → User Management
   ```

3. **Select a Test User**
   - Filter by user type
   - Find a test account

4. **Click Reset Password**
   - Click key icon (🔑)
   - Verify user details displayed

5. **Generate Password**
   - Click "Generate Strong Password"
   - Verify password appears in both fields

6. **Copy Password**
   - Click "Copy" button
   - Verify "copied" message appears

7. **Submit Form**
   - Click "Reset Password"
   - Verify success message

8. **Test Login**
   - Logout
   - Login as the test user
   - Use the new password
   - Verify successful login

## Summary

The password reset feature is fully functional and includes:

✅ **Easy Access**: One click from user list
✅ **User-Friendly**: Clear interface with user details
✅ **Secure**: Strong password generation
✅ **Convenient**: Copy to clipboard, show/hide
✅ **Validated**: Real-time password checking
✅ **Professional**: Success messages and confirmations

Admins can quickly and securely reset passwords for any user in the system!
