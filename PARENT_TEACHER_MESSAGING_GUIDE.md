# Parent-Teacher Messaging System

## Overview
A complete messaging system that allows parents to contact their children's teachers directly through the platform.

## Features

### For Parents:
1. **Contact Teachers Page** - View all teachers teaching their children
2. **Send Messages** - Send messages to specific teachers about specific children
3. **Message Inbox** - View all sent and received messages
4. **Message Threads** - View conversation history with replies
5. **Reply to Messages** - Respond to teacher messages

### For Teachers:
1. **Message Inbox** - View all messages from parents
2. **Reply to Parents** - Respond to parent inquiries
3. **View Student Context** - See which student the message is about
4. **Message Status** - Track read/unread messages

## How It Works

### Parent Workflow:

1. **Access Contact Teachers**
   - Click "Contact Teachers" button on parent dashboard
   - View list of all teachers teaching their children
   - See teacher details: name, subjects, which children they teach

2. **Send a Message**
   - Click "Send Message" on a teacher's card
   - Select which child the message is about
   - Select the teacher (auto-populated if clicked from teacher card)
   - Enter subject and message
   - Click "Send Message"

3. **View Messages**
   - Click "View All Messages" or access from dashboard
   - See all sent and received messages
   - New messages are highlighted
   - Click "View" to see message details

4. **Reply to Messages**
   - Open a message from inbox
   - View the conversation thread
   - Type reply in the form at the bottom
   - Click "Send Reply"

### Teacher Workflow:

1. **Access Messages**
   - Go to Messages from navigation or dashboard
   - View all messages from parents
   - New messages are highlighted in blue

2. **Read Messages**
   - Click "View" on any message
   - See the full conversation thread
   - Message is automatically marked as read

3. **Reply to Parents**
   - Type reply in the form
   - Click "Send Reply"
   - Parent will see the reply in their inbox

## Database Model

### ParentTeacherMessage
- **sender**: User who sent the message
- **recipient**: User who receives the message
- **student**: Which student the message is about (optional)
- **subject**: Message subject line
- **message**: Message content
- **status**: sent, read, or replied
- **parent_read**: Boolean - has parent read it
- **teacher_read**: Boolean - has teacher read it
- **created_at**: When message was sent
- **read_at**: When message was first read
- **replied_to**: Link to original message (for threading)

## URLs

### Parent URLs:
- `/accounts/contact-teachers/` - View all teachers
- `/accounts/messages/` - Message inbox
- `/accounts/messages/send/` - Send new message
- `/accounts/messages/send/<teacher_id>/` - Send to specific teacher
- `/accounts/messages/send/<teacher_id>/<student_id>/` - Send about specific student
- `/accounts/messages/<message_id>/` - View message details

### Teacher URLs:
- `/accounts/messages/` - Message inbox
- `/accounts/messages/<message_id>/` - View message details

## Templates Created

1. **contact_teachers.html** - List of teachers with send message buttons
2. **send_message.html** - Form to compose new message
3. **message_inbox.html** - List of all messages
4. **message_detail.html** - View message thread and reply

## Features

### Message Status Tracking
- **New**: Red badge for unread messages
- **Read**: Green badge for read messages
- **Sent**: Gray badge for messages you sent
- **Replied**: Status updates when replied

### Visual Indicators
- Sent messages: Blue background
- Received messages: Green background
- Unread messages: Highlighted row in inbox
- User type badges: Show if sender is parent or teacher

### Security
- Parents can only message teachers of their children
- Teachers can only see messages sent to them
- Messages are private between sender and recipient
- Student context is always maintained

## Admin Panel

Administrators can:
- View all messages
- Filter by status, date, sender type
- Search by subject, message content, usernames
- See message details and threads

## Integration with Parent Dashboard

The "Contact Teachers" button in Quick Actions now:
- Links to `/accounts/contact-teachers/`
- Shows all teachers teaching parent's children
- Provides easy access to send messages
- Displays teacher information and subjects

## Notifications (Future Enhancement)

Potential additions:
- Email notifications when new message received
- Push notifications for mobile
- Unread message count badge
- Message read receipts
- Typing indicators

## Usage Example

### Parent sends message:
1. Parent logs in → Dashboard
2. Clicks "Contact Teachers"
3. Sees list of teachers (e.g., Mr. Smith teaching Math to their child Daji)
4. Clicks "Send Message" on Mr. Smith's card
5. Selects "Daji" as the student
6. Enters subject: "Question about homework"
7. Enters message: "Could you please clarify the assignment for Chapter 5?"
8. Clicks "Send Message"

### Teacher receives and replies:
1. Teacher logs in → Sees notification of new message
2. Goes to Messages
3. Sees message from parent (highlighted as new)
4. Clicks "View"
5. Reads the message
6. Types reply: "The assignment is to complete exercises 1-10 on page 45."
7. Clicks "Send Reply"

### Parent sees reply:
1. Parent logs in → Goes to Messages
2. Sees reply from teacher (highlighted as new)
3. Clicks "View"
4. Reads teacher's response
5. Can reply again if needed

## Testing

To test the system:

1. **Create test data**:
   - Ensure parent has children linked
   - Ensure children are enrolled in classes
   - Ensure teachers are assigned to those classes

2. **Test as parent**:
   - Log in as parent (e.g., dajikopita)
   - Click "Contact Teachers"
   - Send a message to a teacher
   - Check inbox for sent message

3. **Test as teacher**:
   - Log in as teacher
   - Check messages inbox
   - View the message from parent
   - Send a reply

4. **Verify**:
   - Parent should see reply in inbox
   - Message status should update
   - Read status should be tracked

## Files Created/Modified

### New Files:
- `accounts/messaging_models.py` - Message model definition
- `accounts/messaging_views.py` - All messaging views
- `templates/accounts/contact_teachers.html`
- `templates/accounts/send_message.html`
- `templates/accounts/message_inbox.html`
- `templates/accounts/message_detail.html`

### Modified Files:
- `accounts/models.py` - Added ParentTeacherMessage model
- `accounts/urls.py` - Added messaging URLs
- `accounts/admin.py` - Registered message model
- `templates/accounts/parent_dashboard.html` - Updated Contact Teachers link

### Migrations:
- `accounts/migrations/0002_parentteachermessage.py` - Created message table

## Benefits

1. **Direct Communication** - Parents can reach teachers directly
2. **Context Preserved** - Messages linked to specific students
3. **Thread History** - Full conversation history maintained
4. **Status Tracking** - Know when messages are read
5. **Easy Access** - Integrated into dashboard
6. **Organized** - All messages in one inbox
7. **Secure** - Only authorized users can access messages

The system is now fully functional and ready to use!
