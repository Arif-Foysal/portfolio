# Quick Start: Supabase Chat History Setup

**TL;DR - Do This First:**

## ⚡ 5-Minute Setup

### 1️⃣ Create the Database Table

Go to [Supabase Dashboard](https://app.supabase.com) → **SQL Editor** → Paste & Run:

```sql
CREATE TABLE IF NOT EXISTS chat_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  session_id TEXT,
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  message_type VARCHAR(50) DEFAULT 'text',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);

ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anonymous access" ON chat_history
  FOR ALL USING (true) WITH CHECK (true);
```

✅ **Done!**

### 2️⃣ Set Environment Variables

Create/Update `backend/.env`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=your-openai-key
```

Get these from: Supabase Dashboard → **Settings → API**

✅ **Done!**

### 3️⃣ Restart Backend

```bash
cd backend
python main.py
```

Look for: `✅ Supabase client initialized successfully`

✅ **Done!**

### 4️⃣ Test It

1. Open chat page
2. Send a message
3. Go to Supabase → **Table Editor** → **chat_history**
4. See your message? ✅ **Success!**

---

## 🆘 Data Still Not Saving?

Run this diagnostic script:

```bash
cd backend
python verify_supabase_setup.py
```

**It will show you exactly what's wrong!**

---

## 📋 Common Issues

| Issue | Fix |
|-------|-----|
| "table does not exist" | Run SQL from Step 1 |
| "credentials not found" | Set `.env` variables (Step 2) |
| "RLS policy" error | Already fixed in SQL above |
| "CORS error" | Supabase Settings → API → CORS |
| Works locally, not on Vercel | Set env vars on Vercel |

---

## 🔍 How to Verify It's Working

### In Supabase Dashboard:

1. Go to **Table Editor**
2. Click **chat_history**
3. Send a message in the chat
4. Refresh the page
5. See new rows appear? ✅

### In Browser DevTools:

1. Open **Network** tab
2. Send a message
3. Find `POST /chat/` request
4. Check **Payload** has `user_id` ✅
5. Should show success ✅

---

## 📞 Need Help?

**Check this file:** [`SUPABASE_DATA_NOT_SAVING_FIX.md`](./SUPABASE_DATA_NOT_SAVING_FIX.md)

It has complete troubleshooting for every error!

---

**Last Updated:** November 2024
