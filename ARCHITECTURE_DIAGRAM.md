# System Architecture: Supabase Anonymous Sign-In

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Nuxt 3)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Chat Page (chat.vue)                        │  │
│  │  - User sends message                                    │  │
│  │  - Displays chat history                                 │  │
│  │  - Shows response                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        useAuthentication Composable                      │  │
│  │  - signInAnonymously()                                   │  │
│  │  - validateSession()                                     │  │
│  │  - refreshSession()                                      │  │
│  │  - Manages user_id, session_id, auth_token              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Storage (Dual Layer)                        │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ sessionStorage (Session-scoped)                     │ │  │
│  │  │  - user_id, session_id, auth_token                  │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ localStorage (Browser lifetime)                     │ │  │
│  │  │  - Chat messages array                              │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│           API Requests (HTTP/HTTPS)                             │
│                              ↓                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Authentication Routes                         │  │
│  │  POST /auth/anonymous                                    │  │
│  │  GET /auth/validate/{session_id}                         │  │
│  │  POST /auth/refresh/{session_id}                         │  │
│  │  POST /auth/logout/{session_id}                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Auth Service                                  │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ Session Management (In-Memory Cache)              │ │  │
│  │  │  - create_session()                                │ │  │
│  │  │  - validate_session()                              │ │  │
│  │  │  - refresh_session()                               │ │  │
│  │  │  - cleanup_expired()                               │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Chat Routes                                   │  │
│  │  POST /chat/                                             │  │
│  │  - Process message                                      │  │
│  │  - Call ChatbotService                                  │  │
│  │  - Auto-save with user_id                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Chat History Routes                           │  │
│  │  POST /history/save                                      │  │
│  │  POST /history/get                                       │  │
│  │  POST /history/clear                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Database Manager                             │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ save_chat_message()                                │ │  │
│  │  │ get_chat_history()                                 │ │  │
│  │  │ delete_chat_history()                              │ │  │
│  │  │ clear_old_sessions()                               │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SUPABASE (Cloud DB)                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                         │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ chat_history Table                                │ │  │
│  │  │  - id (UUID)                                       │ │  │
│  │  │  - user_id (UUID) [indexed]                        │ │  │
│  │  │  - session_id (UUID) [indexed]                     │ │  │
│  │  │  - message (TEXT)                                  │ │  │
│  │  │  - response (TEXT)                                 │ │  │
│  │  │  - message_type (VARCHAR)                          │ │  │
│  │  │  - created_at (TIMESTAMP) [indexed]                │ │  │
│  │  │  - updated_at (TIMESTAMP)                          │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Row Level Security (RLS)                    │  │
│  │  - Users can insert chat messages                       │  │
│  │  - Users can read chat messages                         │  │
│  │  - Users can delete chat messages                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              API (REST/Auth)                             │  │
│  │  - Authentication                                       │  │
│  │  - Database access                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

### 1. User Authentication Flow

```
User visits chat page
        ↓
[Check sessionStorage for credentials]
        ↓
        ├─ Found? → Restore session → Continue to chat
        │
        └─ Not found? → 
           POST /auth/anonymous
           Backend receives request
           Create anonymous user (UUID)
           Create session (UUID)
           Generate token (JWT/UUID)
           Store in session cache
           Return { user_id, session_id, token }
           Frontend stores in sessionStorage
           ↓
           Session valid for 24 hours
           Auto-refresh every 20 minutes
           ↓
           Ready for chat
```

### 2. Chat Message Flow

```
User types message
        ↓
Frontend adds to messages array
        ↓
Save to localStorage
        ↓
POST /chat/
├─ message: "What are your projects?"
├─ session_id: "session-uuid"
└─ user_id: "user-uuid"
        ↓
Backend receives request
├─ Rate limit check
├─ Validate user_id & session_id
├─ Pass to ChatbotService
├─ Generate AI response
└─ Call auto-save:
   POST /history/save
   └─ DB stores: {user_id, message, response, timestamp}
        ↓
Response sent to frontend:
├─ type: "text" or "projects_list"
├─ data: response content
└─ session_id: session-uuid
        ↓
Frontend receives response
├─ Adds to messages array
├─ Saves to localStorage
└─ Displays to user
        ↓
Message persisted in 2 places:
├─ localStorage (instant access)
└─ Supabase (long-term storage)
```

### 3. History Retrieval Flow

```
User opens app / page refresh
        ↓
[Check localStorage for messages]
        ↓
Found? → Display messages
        ↓
[In background] Load from DB
POST /history/get
├─ user_id: "user-uuid"
├─ limit: 50
└─ Returns all messages for user
        ↓
Frontend updates localStorage
        ↓
User can continue/resume conversation
```

## Session State Machine

```
┌─────────────────┐
│  Not Signed In  │
└────────┬────────┘
         │
         │ POST /auth/anonymous
         ↓
    ┌─────────────┐
    │   Active    │ ← (Auto-refresh every 20 min)
    │  (24 hours) │
    └──────┬──────┘
           │
           ├─ POST /auth/logout → Revoked
           │
           ├─ Time expires (24h) → Expired
           │
           └─ Cleanup job → Cleaned up
                ↓
           ┌────────────┐
           │  Inactive  │
           └────────────┘
```

## Data Lifecycle

```
FRONTEND (Temporary)
├─ sessionStorage
│  ├─ Lifetime: Tab/session
│  └─ Contains: user_id, session_id, token
│
└─ localStorage
   ├─ Lifetime: Browser
   └─ Contains: Chat messages array


SERVER (Temporary)
├─ Session Cache (RAM)
│  ├─ Lifetime: 24 hours
│  └─ Contains: Session metadata
│
└─ Cleanup Job (daily)
   └─ Removes expired sessions


DATABASE (Permanent)
├─ chat_history Table
│  ├─ Lifetime: Until deleted
│  └─ Contains: All messages + metadata
│
├─ Indexes
│  ├─ user_id → Fast user lookups
│  ├─ session_id → Fast session lookups
│  └─ created_at → Time-based queries
│
└─ RLS Policies
   └─ Access control & security
```

## Component Interactions

```
┌──────────────────────────────────┐
│   useAuthentication (Composable)  │
│                                   │
│  signInAnonymously()  ────────────┼──→ POST /auth/anonymous
│  validateSession()    ────────────┼──→ GET /auth/validate/
│  refreshSession()     ────────────┼──→ POST /auth/refresh/
│  logout()             ────────────┼──→ POST /auth/logout/
│  restoreSession()     ────────────┼──→ sessionStorage read
│                                   │
└──────────────────────────────────┘
            ↓
┌──────────────────────────────────┐
│    Chat Page (chat.vue)           │
│                                   │
│  onMounted() → initialize auth    │
│  sendMessage() ────────────────┬──┼──→ POST /chat/
│                               │  │
│                               └──┼──→ POST /history/save (auto)
│                                  │
│  loadHistory() ─────────────────┼──→ POST /history/get
│  clearHistory() ────────────────┼──→ POST /history/clear
│                                  │
│  Storage ───────────────────────┼──→ localStorage
│                                  │
│                                  │
└──────────────────────────────────┘
            ↓
┌──────────────────────────────────┐
│  Authentication Service           │
│                                   │
│  - Session management             │
│  - Token validation               │
│  - Session cleanup                │
│                                   │
└──────────────────────────────────┘
            ↓
┌──────────────────────────────────┐
│  Database Manager                 │
│                                   │
│  - Query chat_history             │
│  - Insert messages                │
│  - Delete old data                │
│                                   │
└──────────────────────────────────┘
            ↓
┌──────────────────────────────────┐
│  Supabase PostgreSQL              │
│                                   │
│  - Persistent storage             │
│  - User data isolation            │
│  - Query indexing                 │
│                                   │
└──────────────────────────────────┘
```

## Deployment Architecture

```
                    ┌─────────────────────────┐
                    │   Internet / Browser    │
                    └────────────┬────────────┘
                                 │
                                 ↓
                    ┌─────────────────────────┐
                    │  Frontend (Vercel)      │
                    │  ├─ Nuxt 3 App          │
                    │  ├─ Static assets       │
                    │  └─ API client          │
                    └────────────┬────────────┘
                                 │ HTTPS
                                 ↓
                    ┌─────────────────────────┐
                    │  Backend (Vercel)       │
                    │  ├─ FastAPI Server      │
                    │  ├─ Auth Service        │
                    │  ├─ Chat Service        │
                    │  └─ Route Handlers      │
                    └────────────┬────────────┘
                                 │ Connection pool
                                 ↓
                    ┌─────────────────────────┐
                    │  Supabase              │
                    │  ├─ PostgreSQL DB      │
                    │  ├─ REST API           │
                    │  ├─ Auth System        │
                    │  └─ Security (RLS)     │
                    └─────────────────────────┘
```

## Error Handling Flow

```
User sends message
        ↓
Validate input
├─ Empty? → Show error
├─ Too long? → Show error
└─ Valid? → Continue
        ↓
Send to backend
        ↓
Rate limit check
├─ Exceeded? → Return 429 error
└─ OK? → Continue
        ↓
Process message
├─ Service error? → Return 500 error
└─ Success? → Continue
        ↓
Save to database
├─ Connection lost? → Log warning, continue
├─ Save failed? → Log error, cached locally
└─ Success? → Confirm
        ↓
Return response to user
        ↓
Display or error message
```

---

**Legend:**
- `→` = HTTP Request
- `├─` = Option/Branch
- `↓` = Data flow
- `||` = Parallel operations
- `(Details)` = Explanatory notes

---

**Last Updated:** November 2024
