# API Endpoints Reference

## Authentication Endpoints

### 1. Create Anonymous Session
**Endpoint:** `POST /auth/anonymous`

**Description:** Creates a new anonymous user session

**Request:**
```json
{
  // No body required
}
```

**Response (200):**
```json
{
  "success": true,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "is_anonymous": true
}
```

**Error (500):**
```json
{
  "detail": "Failed to create anonymous session"
}
```

**Usage:**
```javascript
const auth = await $fetch('/auth/anonymous', { method: 'POST' })
```

---

### 2. Validate Session
**Endpoint:** `GET /auth/validate/{session_id}`

**Description:** Check if a session is valid and not expired

**Parameters:**
- `session_id` (path) - UUID of the session to validate

**Response (200 - Valid):**
```json
{
  "valid": true,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Session is valid"
}
```

**Response (200 - Expired):**
```json
{
  "valid": false,
  "message": "Session expired or not found"
}
```

**Usage:**
```javascript
const isValid = await $fetch(`/auth/validate/${sessionId}`)
if (isValid.valid) {
  console.log('User:', isValid.user_id)
}
```

---

### 3. Refresh Session
**Endpoint:** `POST /auth/refresh/{session_id}`

**Description:** Extend session expiry time by 24 hours

**Parameters:**
- `session_id` (path) - UUID of the session to refresh

**Response (200):**
```json
{
  "success": true,
  "message": "Session refreshed"
}
```

**Error (404):**
```json
{
  "detail": "Session not found"
}
```

**Usage:**
```javascript
await $fetch(`/auth/refresh/${sessionId}`, { method: 'POST' })
```

---

### 4. Logout/Revoke Session
**Endpoint:** `POST /auth/logout/{session_id}`

**Description:** End and revoke a session

**Parameters:**
- `session_id` (path) - UUID of the session to revoke

**Response (200):**
```json
{
  "success": true,
  "message": "Session revoked"
}
```

**Usage:**
```javascript
await $fetch(`/auth/logout/${sessionId}`, { method: 'POST' })
```

---

### 5. Get Session Information
**Endpoint:** `GET /auth/session/{session_id}`

**Description:** Get detailed information about a session

**Parameters:**
- `session_id` (path) - UUID of the session

**Response (200):**
```json
{
  "valid": true,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_anonymous": true,
  "created_at": "2024-11-04T10:30:00Z",
  "expires_at": "2024-11-05T10:30:00Z"
}
```

**Error (404):**
```json
{
  "valid": false,
  "message": "Session not found or expired"
}
```

---

### 6. Cleanup Expired Sessions
**Endpoint:** `POST /auth/cleanup`

**Description:** Remove all expired sessions (Admin endpoint)

**Response (200):**
```json
{
  "success": true,
  "message": "Cleaned up 42 expired sessions",
  "count": 42
}
```

**Usage:**
```bash
curl -X POST https://your-api.com/auth/cleanup
```

---

### 7. Auth Health Check
**Endpoint:** `GET /auth/health`

**Description:** Check if auth service is running

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Auth service is running",
  "supabase_available": true
}
```

---

## Chat History Endpoints

### 1. Save Chat Message
**Endpoint:** `POST /history/save`

**Description:** Save a chat message and response

**Query Parameters:**
- `user_id` (string, required) - User UUID
- `message` (string, required) - User's message
- `response` (string, required) - Bot's response
- `session_id` (string, required) - Session UUID
- `message_type` (string, optional) - Message type (default: "text")

**Response (200):**
```json
{
  "success": true,
  "message": "Chat message saved",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "created_at": "2024-11-04T10:30:00Z"
  }
}
```

**Usage:**
```javascript
await $fetch('/history/save', {
  method: 'POST',
  body: {
    user_id: userId,
    message: "What projects have you built?",
    response: "I've built several projects...",
    session_id: sessionId,
    message_type: "text"
  }
})
```

---

### 2. Get Chat History
**Endpoint:** `POST /history/get`

**Description:** Retrieve chat history for a user

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001",  // Optional
  "limit": 50  // Optional, default: 50
}
```

**Response (200):**
```json
{
  "success": true,
  "messages": [
    {
      "id": "msg-1",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "session_id": "550e8400-e29b-41d4-a716-446655440001",
      "message": "What projects have you built?",
      "response": "I've built several projects...",
      "message_type": "text",
      "created_at": "2024-11-04T10:30:00Z"
    }
  ],
  "total_count": 1
}
```

**Usage:**
```javascript
const history = await $fetch('/history/get', {
  method: 'POST',
  body: {
    user_id: userId,
    limit: 50
  }
})

history.messages.forEach(msg => {
  console.log(msg.message, '→', msg.response)
})
```

---

### 3. Clear Chat History
**Endpoint:** `POST /history/clear`

**Description:** Delete all chat history for a user

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001"  // Optional
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Chat history cleared",
  "deleted_count": 0
}
```

**Usage:**
```javascript
await $fetch('/history/clear', {
  method: 'POST',
  body: { user_id: userId }
})
```

---

### 4. Get Session History
**Endpoint:** `GET /history/session/{session_id}`

**Description:** Get chat history for a specific session

**Parameters:**
- `session_id` (path) - Session UUID
- `limit` (query, optional) - Max messages to return (default: 50)

**Response (200):**
```json
{
  "success": true,
  "message": "Use /history/get endpoint with user_id",
  "messages": []
}
```

---

### 5. History Health Check
**Endpoint:** `GET /history/health`

**Description:** Check if history service is running

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Chat history service is running",
  "database_connected": true
}
```

---

## Chat Endpoints

### 1. Send Chat Message
**Endpoint:** `POST /chat/`

**Description:** Send a message and get a response

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {token}  // Optional
```

**Request Body:**
```json
{
  "message": "What are your projects?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001"  // For tracking
}
```

**Response (200):**
```json
{
  "type": "text",
  "data": "I've worked on several exciting projects including...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200 - Projects List):**
```json
{
  "type": "projects_list",
  "data": [
    {
      "name": "Blue Horizon",
      "description": "A project management tool",
      "technologies": ["React", "Node.js", "MongoDB"],
      "link": "https://example.com",
      "github_link": "https://github.com/user/project"
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error (429 - Rate Limited):**
```json
{
  "detail": "Rate limit exceeded. Maximum 10 requests per minute."
}
```

**Error (503 - Service Unavailable):**
```json
{
  "detail": "Chatbot service is not available. Please check OpenAI API configuration."
}
```

**Usage:**
```javascript
const response = await $fetch('/chat/', {
  method: 'POST',
  body: {
    message: "Tell me about your projects",
    session_id: sessionId,
    user_id: userId
  }
})

if (response.type === 'text') {
  console.log(response.data)
} else if (response.type === 'projects_list') {
  response.data.forEach(project => {
    console.log(`${project.name}: ${project.description}`)
  })
}
```

---

### 2. Chat Health Check
**Endpoint:** `GET /chat/health`

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Chat service is running"
}
```

---

## Error Responses

### Common Error Formats

**400 - Bad Request:**
```json
{
  "detail": "Invalid input format"
}
```

**404 - Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**429 - Rate Limited:**
```json
{
  "detail": "Rate limit exceeded. Maximum X requests per Y."
}
```

**500 - Server Error:**
```json
{
  "detail": "An error occurred while processing your request."
}
```

**503 - Service Unavailable:**
```json
{
  "detail": "Service is temporarily unavailable."
}
```

---

## Rate Limiting

- **Chat Endpoint:** 10 requests per minute per session
- **Auth Endpoints:** 30 requests per minute per IP
- **History Endpoints:** No limit (use with care)

---

## Authentication Headers

For authenticated requests, include:

```
Authorization: Bearer {token}
Content-Type: application/json
```

Where `{token}` is the token returned from `/auth/anonymous`.

---

## Example: Complete Flow

```javascript
// 1. Sign in anonymously
const auth = await $fetch('/auth/anonymous', { method: 'POST' })
const { user_id, session_id, token } = auth

// 2. Send a message
const response = await $fetch('/chat/', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: {
    message: "Show me your projects",
    session_id: session_id,
    user_id: user_id
  }
})

// 3. Save to history (auto-done by /chat/ endpoint)

// 4. Later, retrieve history
const history = await $fetch('/history/get', {
  method: 'POST',
  body: {
    user_id: user_id,
    limit: 50
  }
})

// 5. Logout
await $fetch(`/auth/logout/${session_id}`, { method: 'POST' })
```

---

**Last Updated:** November 2024
