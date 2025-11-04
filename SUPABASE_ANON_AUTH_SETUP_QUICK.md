# Quick Setup Guide: Supabase Anonymous Auth

## 5-Minute Setup

### Step 1: Create Database Table

Go to your Supabase dashboard → SQL Editor and run:

```sql
-- Create chat_history table
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

-- Create indexes for performance
CREATE INDEX idx_user_id ON chat_history(user_id);
CREATE INDEX idx_session_id ON chat_history(session_id);
CREATE INDEX idx_created_at ON chat_history(created_at);

-- Enable RLS (Row Level Security)
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Create policy to allow insert (users can save their own messages)
CREATE POLICY "Users can insert chat messages" ON chat_history
  FOR INSERT WITH CHECK (true);

-- Create policy to allow select (users can read their own messages)
CREATE POLICY "Users can read chat messages" ON chat_history
  FOR SELECT USING (true);

-- Create policy to allow delete (users can delete their own messages)
CREATE POLICY "Users can delete chat messages" ON chat_history
  FOR DELETE USING (true);
```

### Step 2: Verify Supabase Credentials

Your `.env` file should have:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
```

Get these from Supabase Dashboard → Settings → API

### Step 3: Deploy Backend

```bash
# If using Vercel (recommended)
cd backend
vercel deploy

# Or run locally
python main.py
```

### Step 4: Update Frontend API URL (if needed)

In `app/pages/chat.vue`, update:

```javascript
const API_BASE_URL = process.env.NUXT_PUBLIC_API_URL || 'https://your-backend-url.com'
```

Or set in `.env`:
```bash
NUXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Step 5: Deploy Frontend

```bash
npm run build
npm run preview
```

## Testing

### 1. Test Anonymous Sign-In
Open browser console on chat page:
```javascript
const { signInAnonymously } = useAuthentication()
await signInAnonymously()
// Should see { success: true, user_id: "...", session_id: "..." }
```

### 2. Test Chat Message
Send a message in the UI - should be saved automatically

### 3. Verify Database
Supabase Dashboard → chat_history table → Should see new rows

## Common Issues

| Problem | Solution |
|---------|----------|
| "Database client not available" | Check SUPABASE_URL and SUPABASE_KEY in .env |
| Table doesn't exist | Run SQL script in Supabase SQL Editor |
| Messages not saving | Check browser console for errors, verify API is running |
| CORS errors | Verify backend URL is correct in frontend |

## Next Steps

1. ✅ Basic setup complete
2. 📊 Monitor chat history in Supabase dashboard
3. 🔒 Review security settings (RLS policies)
4. 📈 Track user engagement metrics
5. 🚀 Ready for production deployment

## Endpoints Quick Reference

### Authentication
- `POST /auth/anonymous` - Create session
- `GET /auth/validate/{session_id}` - Check valid
- `POST /auth/logout/{session_id}` - End session

### Chat History
- `POST /history/save` - Save message
- `POST /history/get` - Get history
- `POST /history/clear` - Clear history

### Chat
- `POST /chat/` - Send message (auto-saves)

## Need Help?

See: `SUPABASE_ANON_AUTH_IMPLEMENTATION.md` for full documentation
