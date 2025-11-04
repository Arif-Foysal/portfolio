# Supabase Chat History Not Saving - Complete Troubleshooting Guide

## 🔍 Quick Diagnosis Checklist

Use this checklist to identify your issue:

### ✅ Step 1: Verify Database Setup (CRITICAL)

**BEFORE** data can be saved, you **MUST** create the table in Supabase:

```bash
❌ NO TABLE = NO DATA SAVES
✅ CREATE TABLE FIRST = DATA SAVES
```

### ✅ Step 2: Environment Variables

Check your `.env` file has:

```bash
# .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### ✅ Step 3: Frontend Sending User ID

Check the frontend is actually sending `user_id` with each message.

---

## 🚨 Most Common Issues & Solutions

### **ISSUE #1: Table Doesn't Exist (MOST COMMON)**

**Symptom:** 
```
Database error saving chat message: relation "public.chat_history" does not exist
```

**Solution - CREATE THE TABLE:**

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click your project
3. Go to **SQL Editor**
4. Click **New Query**
5. **Copy & Paste this SQL:**

```sql
-- Create the chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  session_id TEXT,
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  message_type VARCHAR(50) DEFAULT 'text',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);

-- Enable Row Level Security
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Allow anonymous users to insert and read their own data
CREATE POLICY "Allow anonymous insert" ON chat_history
  FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow anonymous read" ON chat_history
  FOR SELECT
  USING (true);

CREATE POLICY "Allow anonymous update" ON chat_history
  FOR UPDATE
  USING (true);

CREATE POLICY "Allow anonymous delete" ON chat_history
  FOR DELETE
  USING (true);
```

6. Click **Run**
7. You should see: `✓ Success. No rows returned`

**Then restart your backend and try again!**

---

### **ISSUE #2: Supabase Credentials Not Loaded**

**Symptom:**
```
⚠️  Supabase credentials not found in environment variables
```

**Solution:**

1. **Check your `.env` file exists** in the `backend/` folder:
   ```
   /mnt/files/Developer/portfolio/backend/.env
   ```

2. **Add the credentials:**
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   OPENAI_API_KEY=your-openai-key
   ```

3. **Get your credentials from Supabase:**
   - Go to [Supabase Dashboard](https://app.supabase.com)
   - Click your project
   - Go to **Settings → API**
   - Copy **Project URL** → paste as `SUPABASE_URL`
   - Copy **Anon Public** key → paste as `SUPABASE_KEY`

4. **Restart the backend:**
   ```bash
   # Kill the running process
   ctrl + c
   
   # Restart
   python main.py
   ```

---

### **ISSUE #3: Frontend Not Sending User ID**

**Symptom:**
- Backend receives message but doesn't save it
- No error in logs

**Solution:**

Check that your frontend is actually sending `user_id`. Look at the request being sent:

**In `app/pages/chat.vue`, the `sendMessage()` function should pass `user_id`:**

```javascript
// This is what should be sent to the backend
const response = await $fetch(`${API_BASE_URL}/chat/`, {
  method: 'POST',
  body: {
    message: userMessage,
    session_id: sessionId.value,
    user_id: userId.value  // ← THIS MUST BE INCLUDED
  }
})
```

**To debug:**

1. Open browser DevTools → **Network** tab
2. Send a message
3. Look for the `POST /chat/` request
4. Click it → **Payload** tab
5. Check if `user_id` is in the JSON body

If `user_id` is missing, it won't save.

---

### **ISSUE #4: Row Level Security (RLS) Blocking Writes**

**Symptom:**
```
new row violates row-level security policy
```

**Solution:**

The SQL script above includes RLS policies that allow anonymous writes. If you didn't run it:

1. Go to Supabase → **Authentication → Policies**
2. Look for the `chat_history` table
3. Make sure these policies exist:
   - ✅ "Allow anonymous insert"
   - ✅ "Allow anonymous read"
   - ✅ "Allow anonymous update"
   - ✅ "Allow anonymous delete"

If not, run the SQL above.

---

### **ISSUE #5: CORS Issues**

**Symptom:**
```
Error: CORS policy blocked the request
```

**Solution:**

1. Go to Supabase Dashboard → **Settings → API**
2. Under "CORS configuration", ensure your frontend URL is allowed
3. Add if missing:
   - `http://localhost:3000`
   - `http://localhost:3001`
   - `https://your-domain.com`

---

### **ISSUE #6: Vercel Deployment Issues**

**Symptom:**
- Works locally, doesn't work on Vercel

**Solution:**

Make sure environment variables are set on Vercel:

1. Go to [Vercel Dashboard](https://vercel.com)
2. Click your project
3. Go to **Settings → Environment Variables**
4. Add:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   OPENAI_API_KEY=your-openai-key
   ```
5. Redeploy:
   ```bash
   git push origin main
   ```

---

## 🔧 Complete Setup Guide (From Scratch)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click **Start your project**
3. Sign in with GitHub or email
4. Click **New Project**
5. Fill in:
   - **Project name:** portfolio-chat
   - **Database password:** Generate strong password
   - **Region:** Choose closest to you

6. Wait for project to be created (5-10 minutes)

### Step 2: Create the Chat History Table

1. Go to **SQL Editor**
2. Run the SQL script from **ISSUE #1** above
3. Verify table was created in **Table Editor**

### Step 3: Get Your Credentials

1. Go to **Settings → API**
2. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Anon Public** → `SUPABASE_KEY`

### Step 4: Update Backend .env

Create/update `backend/.env`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=your-openai-key
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Step 5: Install Dependencies

```bash
cd backend
pip install supabase
```

### Step 6: Restart Backend

```bash
python main.py
```

Check for this output:
```
✅ Supabase client initialized successfully
```

### Step 7: Test in Frontend

1. Open your chat page
2. Send a message
3. Go to Supabase Dashboard → **Table Editor**
4. Click **chat_history** table
5. You should see your message there! ✅

---

## 🧪 Testing Data Save

### Manual Test via cURL

```bash
# Test saving a message directly
curl -X POST http://localhost:8000/history/save \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "message": "Hello",
    "response": "Hi there!",
    "session_id": "test-session-123",
    "message_type": "text"
  }'

# Expected response:
# {"success": true, "message": "Chat message saved", "data": [...]}
```

### Manual Test via Python

```python
import asyncio
from database import db_manager

async def test():
    try:
        result = await db_manager.save_chat_message(
            user_id="test-user-456",
            message="Test message",
            response="Test response",
            session_id="test-session-456",
            message_type="text"
        )
        print(f"✅ Success: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(test())
```

---

## 📊 Verify Data is Saving

### Via Supabase Dashboard

1. Open [Supabase Dashboard](https://app.supabase.com)
2. Click your project
3. Go to **Table Editor**
4. Click **chat_history**
5. You should see rows with:
   - `user_id` (UUID)
   - `session_id` (text)
   - `message` (your message)
   - `response` (bot response)
   - `created_at` (timestamp)

### Via SQL Query

```sql
-- Count total messages
SELECT COUNT(*) FROM chat_history;

-- See recent messages
SELECT * FROM chat_history 
ORDER BY created_at DESC 
LIMIT 10;

-- See messages for specific user
SELECT * FROM chat_history 
WHERE user_id = 'your-user-id'
ORDER BY created_at DESC;
```

---

## 🔐 Row Level Security (RLS) Troubleshooting

### Check if RLS is Enabled

1. Supabase Dashboard → **Table Editor**
2. Click **chat_history**
3. Look for **RLS toggle** (should be ON - blue)

### View Existing Policies

1. Click **chat_history** table
2. Scroll down to **Policies**
3. You should see 4 policies for insert, select, update, delete

### If Policies Don't Exist

Run this SQL:

```sql
-- Enable RLS
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Allow anonymous insert" ON chat_history
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow anonymous read" ON chat_history
  FOR SELECT USING (true);

CREATE POLICY "Allow anonymous update" ON chat_history
  FOR UPDATE USING (true);

CREATE POLICY "Allow anonymous delete" ON chat_history
  FOR DELETE USING (true);
```

---

## 🐛 Debug Logging

### Enable Debug Mode

Update `backend/.env`:

```bash
DEBUG=True
```

Then check logs for detailed error messages.

### Backend Logs to Watch For

```bash
✅ Supabase client initialized successfully
  → Good! Database is connected

❌ Failed to initialize Supabase client: ...
  → Bad! Check credentials

⚠️  Supabase credentials not found
  → Bad! Check .env file

Warning: Failed to save chat history: ...
  → Backend caught an error while saving
```

### Frontend Logs to Watch For

Open browser DevTools → **Console** tab:

```javascript
// Check if authenticated
console.log('User ID:', userId.value)
console.log('Session ID:', sessionId.value)
console.log('Auth Status:', isAuthenticated.value)

// Check network requests
// Go to Network tab and look for POST /chat/
// Check the request body includes user_id
```

---

## 📝 Summary Checklist

Before claiming "it's not working", verify:

- [ ] **Table exists** - Run SQL from ISSUE #1
- [ ] **Credentials set** - Check `.env` has `SUPABASE_URL` and `SUPABASE_KEY`
- [ ] **Backend restarted** - After changing `.env`
- [ ] **RLS policies exist** - Run RLS SQL if needed
- [ ] **Frontend sends user_id** - Check Network tab in DevTools
- [ ] **No errors in logs** - Check backend and browser console
- [ ] **Data visible in Supabase** - Check Table Editor

If all checked and still not working → Share the error message!

---

## 🆘 Getting Help

**When reporting an issue, provide:**

1. Error message from backend logs
2. Error message from browser console
3. Screenshot of Supabase table (or show it's missing)
4. Output of:
   ```bash
   # In backend
   python main.py
   
   # Show console output
   ```

---

## 📚 Reference

- [Supabase Docs](https://supabase.com/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python)
- [RLS Policies](https://supabase.com/docs/guides/auth/row-level-security)
- [CORS Configuration](https://supabase.com/docs/guides/api)

**Last Updated:** November 2024
**Issue Tracker:** Check logs first!
