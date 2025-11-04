# Data Flow: What Should Happen When You Send a Message

## 🔄 The Complete Flow (With Debugging Points)

```
┌─────────────────────────────────────────────────────────────┐
│ YOU: Type message and press Send                            │
└────────────────────────┬────────────────────────────────────┘
                         ↓
                    ✅ Frontend
        ┌──────────────────────────────┐
        │ Chat Page (chat.vue)          │
        │ - Add message to array        │
        │ - Show in UI                  │
        │ - Save to localStorage        │
        └────────────┬──────────────────┘
                     ↓
        ┌──────────────────────────────────────┐
        │ POST /chat/                          │
        │                                      │
        │ Body:                                │
        │ {                                    │
        │   "message": "Hello",                │
        │   "session_id": "sess-123",          │
        │   "user_id": "user-456"  ← CRITICAL │
        │ }                                    │
        └────────────┬─────────────────────────┘
                     ↓
        ┌─────────────────────────────────────────┐
        │          🌍 Network Request             │
        │     (Can see in DevTools Network tab)   │
        └────────────┬────────────────────────────┘
                     ↓
                  ✅ Backend
        ┌──────────────────────────────┐
        │ routes/chat.py               │
        │ - Receive message            │
        │ - Rate limit check           │
        │ - Pass to ChatbotService     │
        └────────────┬──────────────────┘
                     ↓
        ┌──────────────────────────────┐
        │ ChatbotService               │
        │ - Classify message           │
        │ - Generate response          │
        │ - Prepare response           │
        └────────────┬──────────────────┘
                     ↓
        ┌────────────────────────────────────────┐
        │ Check: Is database connected?          │
        │ if db_manager.is_connected():          │
        │   → YES: Continue                      │
        │   → NO: Skip saving (data lost!)       │
        └────────────┬─────────────────────────┘
                     ↓
        ┌────────────────────────────────────────┐
        │ db_manager.save_chat_message(          │
        │   user_id="user-456",                  │
        │   message="Hello",                     │
        │   response="Hi there!",                │
        │   session_id="sess-123",               │
        │   message_type="text"                  │
        │ )                                      │
        └────────────┬─────────────────────────┘
                     ↓
                ✅ Supabase
        ┌──────────────────────────────┐
        │ Database Connection          │
        │ Check: Does table exist?     │
        │ → YES: Insert row            │
        │ → NO: Error! (most common!)  │
        └────────────┬──────────────────┘
                     ↓
        ┌────────────────────────────────────────┐
        │ Check: RLS Policies Allow Insert?      │
        │ → YES: Row inserted                    │
        │ → NO: Error!                           │
        └────────────┬─────────────────────────┘
                     ↓
        ┌──────────────────────────────┐
        │ ✅ Data Saved to Database!   │
        │                              │
        │ chat_history table:          │
        │ ├─ id: abc-123               │
        │ ├─ user_id: user-456         │
        │ ├─ message: Hello            │
        │ ├─ response: Hi there!       │
        │ └─ created_at: [timestamp]   │
        └────────────┬──────────────────┘
                     ↓
        Response sent to frontend
                     ↓
        ┌──────────────────────────────┐
        │ Frontend receives response   │
        │ - Display bot message        │
        │ - Add to messages array      │
        │ - Save to localStorage       │
        └──────────────────────────────┘
                     ↓
                🎉 DONE!
    Data is now saved in 2 places:
    1. localStorage (browser)
    2. Supabase (cloud database)
```

---

## 🔴 Failure Points (Why Data Doesn't Save)

### ❌ Failure Point #1: Table Doesn't Exist

```
When: db_manager tries to insert
Error: relation "public.chat_history" does not exist

Why: SQL script never ran

Fix: Go to Supabase SQL Editor and run the creation script
```

### ❌ Failure Point #2: Credentials Not Set

```
When: Backend starts
Error: ⚠️  Supabase credentials not found

Why: .env file doesn't have SUPABASE_URL or SUPABASE_KEY

Fix: Add to backend/.env:
  SUPABASE_URL=https://your-project.supabase.co
  SUPABASE_KEY=your-anon-key
  
Then restart backend
```

### ❌ Failure Point #3: Frontend Not Sending user_id

```
When: Message is processed
Issue: Data not saved even though backend runs

Why: POST /chat/ body missing "user_id" field

Fix: Check DevTools Network tab → POST /chat/ → see if user_id in body

If missing: Check that frontend is calling:
  $fetch('/chat/', {
    body: {
      message: "...",
      user_id: userId.value  ← This must be here!
    }
  })
```

### ❌ Failure Point #4: RLS Policy Blocks Insert

```
When: Backend tries to insert
Error: new row violates row-level security policy

Why: RLS policies not set correctly

Fix: Go to Supabase SQL Editor and run the RLS script
  (Part of the creation script provided)
```

### ❌ Failure Point #5: Backend Not Restarted

```
When: After changing .env file
Issue: Backend still uses old credentials

Why: Python cached the old environment variables

Fix: 
  Ctrl + C (stop backend)
  python main.py (restart it)
  
Should see: ✅ Supabase client initialized successfully
```

---

## 🧪 How to Debug Each Step

### Debug #1: Is Backend Connected to Supabase?

Look at backend console output when it starts:

✅ **Good:**
```
✅ Supabase client initialized successfully
```

❌ **Bad:**
```
⚠️  Supabase credentials not found in environment variables
```

### Debug #2: Is Frontend Sending user_id?

1. Open DevTools (F12)
2. Go to **Network** tab
3. Send a message
4. Look for **POST /chat/** request
5. Click it → **Payload** tab
6. Check if you see:
```json
{
  "message": "Hello",
  "session_id": "...",
  "user_id": "..."  ← MUST BE HERE
}
```

✅ **If user_id is there:** Good!
❌ **If user_id is missing:** That's the problem!

### Debug #3: Did the SQL Run Successfully?

1. Supabase → **SQL Editor**
2. **New Query** 
3. Paste:
```sql
SELECT * FROM information_schema.tables 
WHERE table_name = 'chat_history';
```
4. Click **Run**
5. Check results

✅ **If you see a row:** Table exists!
❌ **If empty:** Table doesn't exist (run creation script)

### Debug #4: Is Data Actually in the Database?

1. Supabase → **Table Editor**
2. Click **chat_history**
3. You should see rows

✅ **If you see messages:** Data is saving!
❌ **If empty:** Something failed above

Or via SQL:
```sql
SELECT COUNT(*) as total_messages FROM chat_history;
```

---

## 📋 Step-by-Step Debugging Process

**If data is NOT saving, follow this:**

### Step 1: Check Backend Console
```bash
# Did you see this when starting?
✅ Supabase client initialized successfully

# If NO, check .env file has correct credentials
```

### Step 2: Check Table Exists
```
Supabase → Table Editor → chat_history table listed?

If NO → Run SQL creation script
If YES → Continue
```

### Step 3: Check Frontend Sending user_id
```
DevTools → Network → POST /chat/ → Payload tab
See user_id in the JSON?

If NO → Frontend code issue
If YES → Continue
```

### Step 4: Check RLS Policies
```
Supabase → chat_history → Policies
See 4 policies? (insert, read, update, delete)

If NO → Run RLS script
If YES → Continue
```

### Step 5: Check Data in Database
```
Supabase → Table Editor → chat_history
See any rows?

If YES → ✅ It's working!
If NO → Something failed above, review steps 1-4
```

---

## ✅ Success Indicators

### You Know It's Working When:

1. **Backend starts without errors:**
   ```
   ✅ Supabase client initialized successfully
   ```

2. **Frontend sends request:**
   ```
   DevTools → Network → POST /chat/ 
   Status: 200 ✅
   ```

3. **Data appears in Supabase:**
   ```
   Supabase → Table Editor → chat_history
   You see a new row ✅
   ```

4. **Database query returns data:**
   ```sql
   SELECT * FROM chat_history;
   -- Shows your message ✅
   ```

---

## 📞 What to Check First (In Order)

1. ✅ Table created? (Run SQL if not)
2. ✅ .env configured? (Set SUPABASE_URL and SUPABASE_KEY)
3. ✅ Backend restarted? (Ctrl+C, then `python main.py`)
4. ✅ Frontend sends user_id? (Check Network tab)
5. ✅ Data in database? (Check Table Editor)

**If any one of these fails, data won't save.**

---

**Remember: Data flows through 5 checkpoints. All 5 must succeed or data is lost.**
