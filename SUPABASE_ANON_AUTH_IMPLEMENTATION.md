# Supabase Anonymous Sign-In Feature Documentation

## Overview

This implementation adds Supabase Anonymous Sign-In functionality to track users and store their chat history. Users are automatically authenticated anonymously when they visit the chat page, allowing the system to persistently store and retrieve their conversation history.

## Features

✅ **Anonymous User Authentication** - Users are automatically signed in anonymously without requiring email/password
✅ **User Tracking** - Each user receives a unique user ID for session tracking
✅ **Chat History Persistence** - All messages and responses are stored in the database
✅ **Session Management** - Sessions are automatically managed with expiration and refresh
✅ **Local Caching** - Chat history is cached locally in localStorage for instant access
✅ **Database Backup** - Conversation history is persisted in Supabase for long-term storage

## Architecture

### Backend Components

#### 1. **Authentication Service** (`services/auth_service.py`)
Handles anonymous user sign-in and session management.

**Key Methods:**
- `sign_in_anonymously()` - Creates a new anonymous user session
- `get_session(session_id)` - Retrieves session data
- `is_session_valid(session_id)` - Validates session expiry
- `refresh_session(session_id)` - Extends session lifetime
- `revoke_session(session_id)` - Logs out a session
- `cleanup_expired_sessions()` - Removes expired sessions

**Session Structure:**
```python
{
    "user_id": "uuid",
    "session_id": "uuid",
    "token": "token",
    "created_at": "ISO datetime",
    "is_anonymous": true
}
```

#### 2. **Database Manager** (`database.py`)
Extended with chat history methods:

**New Methods:**
- `save_chat_message()` - Stores a user message and bot response
- `get_chat_history(user_id, limit)` - Retrieves user's chat history
- `delete_chat_history(user_id)` - Removes all messages for a user
- `clear_old_sessions(days)` - Removes old chat history

#### 3. **Routes**

**Authentication Routes** (`routes/auth.py`)
- `POST /auth/anonymous` - Create anonymous session
- `GET /auth/validate/{session_id}` - Validate session
- `POST /auth/refresh/{session_id}` - Refresh session
- `POST /auth/logout/{session_id}` - Revoke session
- `GET /auth/session/{session_id}` - Get session info
- `POST /auth/cleanup` - Clean expired sessions
- `GET /auth/health` - Health check

**Chat History Routes** (`routes/history.py`)
- `POST /history/save` - Save chat message
- `POST /history/get` - Retrieve chat history
- `POST /history/clear` - Clear user's history
- `GET /history/session/{session_id}` - Get session history
- `GET /history/health` - Health check

**Chat Routes** (updated `routes/chat.py`)
- Enhanced `/chat/` endpoint to save messages with user ID

### Frontend Components

#### 1. **Authentication Composable** (`app/composables/useChat.ts`)

Provides authentication and session management functions:

**Available Functions:**
- `signInAnonymously()` - Authenticate user
- `validateSession(sessionId)` - Check session validity
- `refreshSession(sessionId)` - Extend session
- `logout()` - End session
- `restoreSession()` - Restore from sessionStorage

**State Variables:**
- `userId` - Current user's UUID
- `sessionId` - Current session UUID
- `authToken` - Authentication token
- `isAuthenticated` - Authentication status

#### 2. **Chat Page Updates** (`app/pages/chat.vue`)

**Changes:**
- Automatic anonymous authentication on mount
- User ID passed with each chat message
- Session refresh every 20 minutes
- Enhanced localStorage with user tracking

## Database Schema

### Required Supabase Tables

#### `chat_history` Table
```sql
CREATE TABLE chat_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  session_id UUID NOT NULL,
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  message_type VARCHAR(50) DEFAULT 'text',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX idx_user_id ON chat_history(user_id);
CREATE INDEX idx_session_id ON chat_history(session_id);
CREATE INDEX idx_created_at ON chat_history(created_at);
```

#### `auth_users` Table (Optional - for future reference)
```sql
CREATE TABLE auth_users (
  user_id UUID PRIMARY KEY,
  is_anonymous BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  last_activity TIMESTAMP DEFAULT NOW()
);
```

## Setup Instructions

### 1. Environment Variables

Add these to your `.env` file:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
OPENAI_API_KEY=your-openai-key
```

### 2. Create Supabase Tables

Run the SQL scripts above in Supabase SQL Editor to create the `chat_history` table.

### 3. Configure CORS (Supabase)

In Supabase Dashboard:
- Go to Settings → API
- Ensure your frontend URL is in the allowed origins

### 4. Install Dependencies

Backend:
```bash
cd backend
pip install supabase python-dotenv
```

Frontend:
Already included in Nuxt project.

### 5. Deploy

Backend:
```bash
# For Vercel
vercel deploy

# For local development
python main.py
```

Frontend:
```bash
npm run build
npm run preview
```

## API Usage Examples

### 1. Anonymous Sign-In

```javascript
// Frontend
const { signInAnonymously } = useAuthentication()
const authResponse = await signInAnonymously()
// Response:
// {
//   success: true,
//   user_id: "uuid",
//   session_id: "uuid",
//   token: "token",
//   is_anonymous: true
// }
```

### 2. Send Chat Message with Tracking

```javascript
// Frontend sends request with user_id
const response = await $fetch('/chat/', {
  method: 'POST',
  body: {
    message: "What are your projects?",
    session_id: sessionId,
    user_id: userId  // Included for tracking
  }
})
```

### 3. Save Chat to Database

```python
# Backend automatically saves via chat route
await db_manager.save_chat_message(
    user_id="user-uuid",
    message="What are your projects?",
    response="I've worked on several projects...",
    session_id="session-uuid",
    message_type="text"
)
```

### 4. Retrieve Chat History

```javascript
// Frontend
const history = await $fetch('/history/get', {
  method: 'POST',
  body: {
    user_id: userId,
    limit: 50
  }
})
```

## Data Flow

### User Authentication Flow
```
1. User visits chat page
   ↓
2. Frontend checks for stored session
   ↓
3. If no session, call POST /auth/anonymous
   ↓
4. Backend creates anonymous user
   ↓
5. Returns user_id, session_id, token
   ↓
6. Frontend stores in sessionStorage
   ↓
7. User is authenticated
```

### Chat Message Flow
```
1. User sends message
   ↓
2. Frontend adds message to local messages array
   ↓
3. Frontend saves to localStorage
   ↓
4. Frontend sends to POST /chat/ with user_id
   ↓
5. Backend processes message
   ↓
6. Backend saves to database via db_manager
   ↓
7. Backend returns response
   ↓
8. Frontend displays response
   ↓
9. Message persisted in:
   - localStorage (client-side cache)
   - Supabase (server-side storage)
```

## Session Management

### Session Lifecycle

| Event | Duration | Action |
|-------|----------|--------|
| Created | - | Anonymous sign-in |
| Active | 24 hours | Auto-refresh every 20 min |
| Expired | - | Auto-cleanup on next validation |
| Logout | - | Manual revocation |

### Session Refresh
```javascript
// Automatic refresh every 20 minutes
setInterval(() => {
  if (sessionId.value) {
    refreshSession(sessionId.value)
  }
}, 20 * 60 * 1000)
```

### Session Cleanup
```python
# Cleanup expired sessions every hour
# Admin endpoint: POST /auth/cleanup
auth_service.cleanup_expired_sessions()
```

## Storage Strategy

### Client-Side (localStorage)
- **What:** Message list
- **Why:** Fast access, offline support
- **Persistence:** Browser lifetime or manual clear
- **Key:** `chat_messages`

### Client-Side (sessionStorage)
- **What:** User ID, Session ID, Auth Token
- **Why:** Session-scoped, secure within same session
- **Persistence:** Session lifetime
- **Key:** `user_id`, `session_id`, `auth_token`

### Server-Side (Supabase)
- **What:** Complete chat history
- **Why:** Persistent, queryable, shared across devices
- **Persistence:** Until manually deleted
- **Table:** `chat_history`

## Security Considerations

⚠️ **Important for Production:**

1. **Authentication Routes:**
   - Protect `/auth/cleanup` endpoint with API key
   - Implement rate limiting
   - Add request validation

2. **Database:**
   - Enable Row Level Security (RLS) on Supabase
   - Add user_id filter to queries
   - Encrypt sensitive data at rest

3. **Frontend:**
   - Never store sensitive data in localStorage
   - Validate token on each request
   - Implement CSRF protection

4. **API:**
   - Use HTTPS only
   - Validate CORS headers
   - Implement API key authentication

## Troubleshooting

### Issue: "Database client not available"
**Solution:** 
- Check SUPABASE_URL and SUPABASE_KEY in .env
- Verify Supabase project is active
- Check network connectivity

### Issue: "Failed to authenticate"
**Solution:**
- Clear sessionStorage
- Check browser console for errors
- Verify /auth/anonymous endpoint is accessible

### Issue: "Chat history not loading"
**Solution:**
- Check localStorage is enabled
- Verify chat_history table exists in Supabase
- Check RLS policies aren't blocking queries

### Issue: "Session expired"
**Solution:**
- Automatic refresh should prevent this
- If persists, clear sessionStorage and refresh page
- Check server logs for session cleanup issues

## Performance Optimization

### Current Optimizations
✅ Local caching with localStorage
✅ Session refresh at safe intervals
✅ Database indexes on frequently queried columns
✅ Response compression via gzip

### Future Optimizations
- Implement Redis for session store (vs in-memory)
- Add pagination to chat history queries
- Compress old messages (archive)
- Implement fuzzy search on messages

## Monitoring & Analytics

### Metrics to Track
- Active anonymous users
- Average messages per session
- Session duration
- Failed authentication attempts
- API response times

### Health Checks
```javascript
// Frontend
GET /auth/health
GET /history/health

// Returns database connectivity status
```

## Maintenance

### Regular Tasks
- **Weekly:** Review error logs
- **Monthly:** Clean expired sessions (`POST /auth/cleanup`)
- **Quarterly:** Archive old chat history (>90 days)
- **Annually:** Update security policies

### Database Maintenance
```sql
-- Clean sessions older than 30 days
DELETE FROM chat_history 
WHERE created_at < NOW() - INTERVAL '30 days'
  AND user_id NOT IN (
    SELECT DISTINCT user_id FROM chat_history 
    WHERE created_at > NOW() - INTERVAL '7 days'
  );
```

## Future Enhancements

1. **User Profiles** - Convert anonymous to registered users
2. **Search** - Full-text search across chat history
3. **Export** - Download chat history as PDF/JSON
4. **Sharing** - Share chat sessions with others
5. **Analytics** - User engagement metrics
6. **AI Summaries** - Auto-generate conversation summaries
7. **Multi-device** - Sync history across devices

## Support & Documentation

- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Chat Service Architecture](./CHAT_PERSISTENCE_COMPLETE.md)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2024 | Initial implementation |
| 1.1 | Upcoming | User profile conversion |
| 2.0 | Planned | Full auth system |

---

**Last Updated:** November 2024
**Maintained By:** Development Team
