# Lesson Access Control Feature

## Overview

The Lesson Access Control feature allows administrators to enable or disable specific lessons for individual students. This is useful for:

- **Subscription Management**: Control access based on payment plans
- **Course Progression**: Lock advanced lessons until prerequisites are met
- **Account Suspension**: Temporarily restrict access for non-compliant users
- **Custom Learning Paths**: Create personalized curriculum for each student
- **Beta Testing**: Grant early access to select users

## Architecture

### Access Control Logic

- **Default Behavior**: All lessons are accessible to all authenticated users
- **Blacklist Approach**: Access records are created only to RESTRICT access
- **No Record = Allowed**: If no access record exists, the user can access the lesson
- **Admin Bypass**: Administrators can always access all lessons regardless of restrictions

### Database Schema

```sql
CREATE TABLE user_lesson_access (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id VARCHAR NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    disabled_by VARCHAR REFERENCES users(id) ON DELETE SET NULL,
    disabled_reason VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_user_lesson UNIQUE (user_id, lesson_id)
);
```

**Key Fields:**
- `user_id`: The student whose access is being controlled
- `lesson_id`: The lesson being restricted/enabled
- `is_enabled`: `true` = student can access, `false` = student cannot access
- `disabled_by`: Admin who disabled the lesson (for audit trail)
- `disabled_reason`: Optional explanation for restriction

## API Endpoints

### Admin Endpoints (Require Admin Privileges)

All endpoints are prefixed with `/api/admin`

#### 1. Get All Students
```http
GET /api/admin/students
```

Returns list of all non-admin users.

**Response:**
```json
[
  {
    "id": "user-uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true
  }
]
```

#### 2. Get Student's Lesson Access
```http
GET /api/admin/students/{user_id}/lessons
```

Returns all lessons with access status for a specific student.

**Response:**
```json
[
  {
    "lesson_id": "lesson-uuid",
    "lesson_title": "Introduction to LLMs",
    "lesson_slug": "intro-to-llms",
    "is_enabled": true,
    "access_record_id": null,
    "disabled_reason": null
  },
  {
    "lesson_id": "lesson-uuid-2",
    "lesson_title": "Advanced Prompting",
    "lesson_slug": "advanced-prompting",
    "is_enabled": false,
    "access_record_id": "record-uuid",
    "disabled_reason": "Premium content - upgrade required"
  }
]
```

#### 3. Update Lesson Access
```http
PUT /api/admin/students/{user_id}/lessons/{lesson_id}/access
Content-Type: application/json

{
  "is_enabled": false,
  "disabled_reason": "Account suspended for non-payment"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lesson 'Introduction to LLMs' disabled for student 'johndoe'",
  "access_record": {
    "id": "record-uuid",
    "user_id": "user-uuid",
    "lesson_id": "lesson-uuid",
    "is_enabled": false,
    "disabled_by": "admin-uuid",
    "disabled_reason": "Account suspended for non-payment",
    "created_at": "2025-11-19T20:00:00Z",
    "updated_at": "2025-11-19T20:30:00Z"
  }
}
```

#### 4. Remove Access Restriction (Revert to Default)
```http
DELETE /api/admin/students/{user_id}/lessons/{lesson_id}/access
```

Removes the access record, allowing default access behavior.

**Response:**
```json
{
  "success": true,
  "message": "Access restriction removed. Student now has default access to this lesson."
}
```

#### 5. Disable All Lessons for a Student
```http
POST /api/admin/students/{user_id}/lessons/disable-all?reason=Account%20suspended
```

Useful for account suspension scenarios.

**Response:**
```json
{
  "success": true,
  "message": "Disabled 22 lessons for student 'johndoe'",
  "disabled_count": 22
}
```

#### 6. Enable All Lessons for a Student
```http
POST /api/admin/students/{user_id}/lessons/enable-all
```

Removes all access restrictions for a student.

**Response:**
```json
{
  "success": true,
  "message": "Enabled all lessons for student 'johndoe'. Removed 5 restrictions.",
  "removed_count": 5
}
```

### Student-Facing Endpoints (Modified)

#### Get Lessons (with Access Info)
```http
GET /api/lessons
```

**Response (includes is_accessible field):**
```json
[
  {
    "id": "lesson-uuid",
    "title": "Introduction to LLMs",
    "slug": "intro-to-llms",
    "description": "Learn LLM basics",
    "difficulty": "beginner",
    "order": 1,
    "language": "python",
    "estimated_time": 45,
    "tags": ["llm", "basics"],
    "is_accessible": true
  }
]
```

#### Get Lesson by ID/Slug
```http
GET /api/lessons/{lesson_id}
GET /api/lessons/slug/{slug}
```

Returns `403 Forbidden` if student does not have access:
```json
{
  "detail": "You do not have access to this lesson. Please contact an administrator."
}
```

## Frontend Components

### Admin Panel (`/admin/students`)

**Access:** Admin users only

**Features:**
- View all students
- Select a student to manage
- See all lessons with their access status
- Enable/disable individual lessons
- Add reasons for disabling
- Bulk disable/enable all lessons
- Visual indicators (locked/unlocked badges)

**Usage:**
1. Log in as an admin user
2. Navigate to the Admin Panel button in the header
3. Select a student from the left sidebar
4. Toggle lesson access on the right panel
5. Add reasons when disabling lessons

### Student Lesson List (`/lessons`)

**Features:**
- Locked lessons show 🔒 badge
- Locked lessons are visually dimmed
- Clicking locked lessons shows an error message
- Students cannot access locked lessons directly
- Admin button appears for admin users

## Setup & Deployment

### 1. Run Database Migration

The migration script has already been run, but for future deployments:

```bash
docker exec coding_platform_backend python -m database.add_lesson_access_table
```

**Output:**
```
✅ Successfully created user_lesson_access table
✅ Created indexes for optimal query performance
```

### 2. Verify Admin User

Ensure you have at least one admin user:

```sql
-- Check admin users
SELECT id, username, email, is_admin FROM users WHERE is_admin = true;

-- Grant admin privileges to a user
UPDATE users SET is_admin = true WHERE username = 'your_username';
```

### 3. Restart Services (if needed)

```bash
docker-compose restart backend frontend
```

### 4. Test the Feature

1. **Create Test Users:**
   - Create 1 admin user
   - Create 2-3 regular student users

2. **Test Admin Panel:**
   - Log in as admin
   - Navigate to `/admin/students`
   - Disable a lesson for a student
   - Verify the lesson shows as locked for that student

3. **Test Student View:**
   - Log in as a regular student
   - Verify locked lessons show 🔒 badge
   - Try to access a locked lesson (should show error)
   - Verify unlocked lessons work normally

4. **Test API Endpoints:**
   ```bash
   # Get students
   curl -H "Authorization: Bearer <admin_token>" \
     http://localhost:8000/api/admin/students

   # Get student lesson access
   curl -H "Authorization: Bearer <admin_token>" \
     http://localhost:8000/api/admin/students/{user_id}/lessons

   # Disable a lesson
   curl -X PUT \
     -H "Authorization: Bearer <admin_token>" \
     -H "Content-Type: application/json" \
     -d '{"is_enabled": false, "disabled_reason": "Test"}' \
     http://localhost:8000/api/admin/students/{user_id}/lessons/{lesson_id}/access
   ```

## Security Considerations

### Authorization Checks

1. **Admin Endpoints**: All admin endpoints check `is_admin` flag before allowing operations
2. **Lesson Access**: Non-admin users cannot bypass access controls
3. **Audit Trail**: `disabled_by` field tracks which admin made changes
4. **Token-Based Auth**: All endpoints require valid JWT authentication

### Best Practices

- **Reasons for Restrictions**: Always provide a clear reason when disabling lessons
- **Review Access Regularly**: Periodically review access restrictions
- **Communication**: Inform students before restricting access
- **Backup Before Bulk Operations**: Before using "Disable All", ensure you can restore access
- **Admin Logs**: Monitor admin panel usage for security

## Use Cases & Examples

### 1. Freemium Model

```javascript
// Enable first 5 lessons, lock the rest for free users
const freeLessons = 5
for (let i = 0; i < allLessons.length; i++) {
  if (i >= freeLessons) {
    await updateLessonAccess(userId, allLessons[i].id, {
      is_enabled: false,
      disabled_reason: "Upgrade to Premium to access this lesson"
    })
  }
}
```

### 2. Progressive Unlock

```javascript
// Unlock lessons one by one as student completes prerequisites
async function unlockNextLesson(userId, completedLessonOrder) {
  const nextLesson = lessons.find(l => l.order === completedLessonOrder + 1)
  if (nextLesson) {
    await updateLessonAccess(userId, nextLesson.id, {
      is_enabled: true
    })
  }
}
```

### 3. Account Suspension

```javascript
// Suspend all access
await disableAllLessons(userId, "Account suspended - payment overdue")

// Restore access after payment
await enableAllLessons(userId)
```

### 4. Beta Testing

```javascript
// Grant early access to beta testers
const betaLessons = lessons.filter(l => l.tags.includes('beta'))
for (const lesson of betaLessons) {
  await updateLessonAccess(betaTesterUserId, lesson.id, {
    is_enabled: true
  })
}
```

## Troubleshooting

### Issue: Admin panel not showing

**Solution:** Ensure user has `is_admin = true`:
```sql
UPDATE users SET is_admin = true WHERE username = 'admin';
```

### Issue: Lessons not showing as locked

**Solution:**
1. Check API response includes `is_accessible` field
2. Verify access record exists in database
3. Clear frontend cache and refresh

### Issue: Students can still access locked lessons

**Solution:**
1. Verify backend access check is working: Try accessing `/api/lessons/slug/{slug}` directly
2. Check if user is admin (admins bypass restrictions)
3. Ensure access record has `is_enabled = false`

### Issue: 403 Forbidden when accessing admin panel

**Solution:** Only users with `is_admin = true` can access admin endpoints.

## Future Enhancements

Potential improvements for this feature:

1. **Time-Based Access**: Schedule lesson availability (available from/until dates)
2. **Group Access Control**: Manage access by user groups/cohorts
3. **Automatic Unlocking**: Auto-enable lessons based on progress or achievements
4. **Access Analytics**: Track which lessons are most frequently restricted
5. **Email Notifications**: Notify students when lessons are enabled/disabled
6. **Prerequisite Chains**: Automatically lock/unlock based on completion
7. **Bulk Import**: CSV upload for setting access for multiple users
8. **Access History**: View audit log of all access changes

## API Documentation

Full API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Look for the "Admin" tag to see all access control endpoints.

---

**Feature Status:** ✅ Production Ready

**Version:** 1.0.0

**Last Updated:** 2025-11-19
