# Deployment & Testing Checklist

## Pre-Deployment Verification

### Backend Files ✓
- [x] `services/auth_service.py` - Authentication service created
- [x] `routes/auth.py` - Auth endpoints created
- [x] `routes/history.py` - History endpoints created
- [x] `database.py` - Extended with history methods
- [x] `models.py` - New auth models added
- [x] `main.py` - Routes registered
- [x] `routes/chat.py` - Auto-save integrated

### Frontend Files ✓
- [x] `composables/useChat.ts` - Auth composable created
- [x] `pages/chat.vue` - Auth integrated

### Documentation ✓
- [x] `SUPABASE_ANON_AUTH_IMPLEMENTATION.md` - Full guide
- [x] `SUPABASE_ANON_AUTH_SETUP_QUICK.md` - Quick setup
- [x] `API_ENDPOINTS.md` - API reference
- [x] `IMPLEMENTATION_SUMMARY.md` - Summary
- [x] `ARCHITECTURE_DIAGRAM.md` - Architecture diagrams
- [x] This checklist

## Environment Setup

### Backend Configuration
- [ ] Create `.env` file with:
  ```bash
  SUPABASE_URL=https://your-project.supabase.co
  SUPABASE_KEY=your-anon-public-key
  OPENAI_API_KEY=your-key
  DEBUG=False
  ```
- [ ] Verify all environment variables are set
- [ ] Test local environment: `python main.py`

### Frontend Configuration
- [ ] Create/update `.env` with:
  ```bash
  NUXT_PUBLIC_API_URL=http://localhost:8000
  # or for production:
  NUXT_PUBLIC_API_URL=https://your-backend-url.com
  ```
- [ ] Verify frontend can access backend

### Supabase Setup
- [ ] Log in to Supabase dashboard
- [ ] Create new project or use existing
- [ ] Get SUPABASE_URL and SUPABASE_KEY
- [ ] Go to SQL Editor

## Database Setup

### Create Tables
- [ ] Run SQL in Supabase SQL Editor:
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

  CREATE INDEX idx_user_id ON chat_history(user_id);
  CREATE INDEX idx_session_id ON chat_history(session_id);
  CREATE INDEX idx_created_at ON chat_history(created_at);

  ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

  CREATE POLICY "Users can insert chat messages" ON chat_history
    FOR INSERT WITH CHECK (true);

  CREATE POLICY "Users can read chat messages" ON chat_history
    FOR SELECT USING (true);

  CREATE POLICY "Users can delete chat messages" ON chat_history
    FOR DELETE USING (true);
  ```
- [ ] Verify table created in Data Editor
- [ ] Verify indexes are visible
- [ ] Test INSERT via UI (optional)

### Database Verification
- [ ] Table `chat_history` exists
- [ ] Columns are correct data types
- [ ] Indexes created on user_id, session_id, created_at
- [ ] RLS policies are enabled
- [ ] RLS policies are correct

## Backend Testing

### Unit Tests
- [ ] Test Auth Service:
  ```python
  python -c "from services.auth_service import auth_service; 
  print(auth_service.sign_in_anonymously())"
  ```
- [ ] Test Database Manager:
  ```python
  python -c "from database import db_manager; 
  print(db_manager.is_connected())"
  ```

### API Endpoint Tests
- [ ] Test `/auth/anonymous`: `curl -X POST http://localhost:8000/auth/anonymous`
  - Expected: `{ "success": true, "user_id": "...", ... }`
- [ ] Test `/auth/validate/{session_id}`: After getting session_id
  - Expected: `{ "valid": true, "user_id": "..." }`
- [ ] Test `/chat/`: Send test message
  - Expected: `{ "type": "text", "data": "...", "session_id": "..." }`
- [ ] Test `/history/health`: `curl http://localhost:8000/history/health`
  - Expected: `{ "status": "healthy", "database_connected": true }`

### Database Integration Tests
- [ ] Send message and verify it appears in Supabase
- [ ] Check chat_history table for new rows
- [ ] Verify user_id and session_id are stored
- [ ] Verify timestamp is correct

## Frontend Testing

### Browser Console Tests
```javascript
// Test 1: Authentication
const { signInAnonymously } = useAuthentication()
const auth = await signInAnonymously()
console.log('Auth:', auth) // Should have user_id, session_id, token

// Test 2: Session storage
console.log('Stored:', {
  user_id: sessionStorage.getItem('user_id'),
  session_id: sessionStorage.getItem('session_id'),
  token: sessionStorage.getItem('auth_token')
})

// Test 3: Session validation
const valid = await $fetch('/auth/validate/' + auth.session_id)
console.log('Valid:', valid) // Should be { valid: true, user_id: "..." }

// Test 4: Send message
const response = await $fetch('/chat/', {
  method: 'POST',
  body: {
    message: 'Test message',
    session_id: auth.session_id,
    user_id: auth.user_id
  }
})
console.log('Response:', response)
```

### UI Tests
- [ ] Visit chat page
- [ ] Verify no errors in console
- [ ] Send a message
- [ ] Verify message appears
- [ ] Verify response appears
- [ ] Check localStorage for messages
- [ ] Refresh page
- [ ] Verify messages are restored
- [ ] Send another message
- [ ] Verify history in Supabase

### Cross-Browser Tests
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browser

## Local Development Testing

### Backend
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
# Should see: "Starting Portfolio Backend API..."
# Check endpoints: curl http://localhost:8000/auth/health
```

### Frontend
```bash
npm run dev
# Should see: "✔ Nitro built in ..."
# Open: http://localhost:3000
```

### Full Integration
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Can authenticate anonymously
- [ ] Can send messages
- [ ] Messages saved to DB
- [ ] History retrieves correctly
- [ ] No CORS errors

## Production Deployment

### Backend Deployment (Vercel)
```bash
cd backend
vercel deploy --prod
```
- [ ] Verify deploy successful
- [ ] Get production URL
- [ ] Update frontend API_BASE_URL
- [ ] Test endpoints: `curl https://your-backend.vercel.app/auth/health`

### Frontend Deployment (Vercel)
```bash
npm run build
vercel deploy --prod
```
- [ ] Verify build successful
- [ ] Verify API calls to production backend
- [ ] Test chat functionality
- [ ] Verify messages saved to DB

### Environment Variables (Production)
- [ ] Set SUPABASE_URL
- [ ] Set SUPABASE_KEY
- [ ] Set OPENAI_API_KEY
- [ ] Set DEBUG=False
- [ ] Set NUXT_PUBLIC_API_URL to production backend

## Post-Deployment Verification

### Health Checks
- [ ] `GET /auth/health` returns "healthy"
- [ ] `GET /chat/health` returns "healthy"
- [ ] `GET /history/health` returns "healthy"
- [ ] Frontend loads without errors

### Functionality Tests
- [ ] Anonymous sign-in works
- [ ] Chat messages send and receive
- [ ] Messages saved to database
- [ ] Chat history retrieves correctly
- [ ] Session refresh works (wait 20+ min)
- [ ] Old sessions cleanup works

### Performance Tests
- [ ] Auth response: < 100ms
- [ ] Chat response: < 500ms
- [ ] History load: < 500ms
- [ ] No console errors

### Security Tests
- [ ] HTTPS enforced (production)
- [ ] CORS headers correct
- [ ] Session tokens valid
- [ ] Rate limiting works (send 15+ messages/min)
- [ ] No sensitive data in localStorage

## Monitoring & Maintenance

### Weekly Tasks
- [ ] Check error logs
- [ ] Monitor performance metrics
- [ ] Verify all health checks passing
- [ ] Test manual message sending

### Monthly Tasks
- [ ] Review database size
- [ ] Check for expired sessions
- [ ] Audit security policies
- [ ] Test backup/restore

### Quarterly Tasks
- [ ] Run full integration tests
- [ ] Review and update documentation
- [ ] Test disaster recovery
- [ ] Performance optimization review

## Troubleshooting Guide

### Issue: "Database client not available"
**Checklist:**
- [ ] SUPABASE_URL is set in .env
- [ ] SUPABASE_KEY is set in .env
- [ ] Supabase project is active
- [ ] Network connectivity is OK
- [ ] API keys are correct

**Resolution:**
```bash
# Verify credentials
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Test Supabase connection
curl -H "apikey: $SUPABASE_KEY" https://$SUPABASE_URL/rest/v1/
```

### Issue: "Failed to authenticate"
**Checklist:**
- [ ] Backend is running
- [ ] /auth/anonymous endpoint is accessible
- [ ] CORS is configured correctly
- [ ] No firewall blocking requests

**Resolution:**
```bash
# Test endpoint
curl -X POST http://localhost:8000/auth/anonymous

# Check CORS headers
curl -i -X OPTIONS http://localhost:8000/chat/
```

### Issue: "Messages not saving"
**Checklist:**
- [ ] chat_history table exists
- [ ] user_id is being passed to /chat/
- [ ] Database connection is working
- [ ] RLS policies are correct

**Resolution:**
```sql
-- Check if table exists
SELECT * FROM information_schema.tables 
WHERE table_name = 'chat_history';

-- Check RLS policies
SELECT * FROM pg_policies 
WHERE tablename = 'chat_history';

-- Test insert
INSERT INTO chat_history 
(user_id, session_id, message, response) 
VALUES ('test-user', 'test-session', 'test', 'test');
```

### Issue: "CORS errors"
**Checklist:**
- [ ] Frontend URL is in CORS_ORIGINS
- [ ] Backend CORS middleware is configured
- [ ] Preflight OPTIONS requests are allowed

**Resolution in `main.py`:**
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend.com",
    "*"  # Allow all (only for development)
]
```

## Rollback Plan

If issues occur in production:

1. **Revert Frontend**
   ```bash
   vercel rollback --prod
   # or redeploy previous version
   ```

2. **Revert Backend**
   ```bash
   vercel rollback --prod
   # or redeploy previous version
   ```

3. **Restore Database**
   - Use Supabase backup
   - Or restore from SQL script

4. **Communication**
   - Notify users
   - Update status page
   - Document incident

## Sign-Off

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Performance acceptable
- [ ] Security verified
- [ ] Team review completed
- [ ] Production deployment approved
- [ ] Monitoring configured
- [ ] Backup verified

## Go-Live Checklist

- [ ] Backend deployed to production
- [ ] Frontend deployed to production
- [ ] All health checks green
- [ ] Database connected and verified
- [ ] Monitoring and alerts configured
- [ ] Support team trained
- [ ] Documentation accessible
- [ ] Rollback plan in place

---

**Status:** [ ] Not Started  [ ] In Progress  [ ] Complete

**Deployment Date:** _______________

**Deployed By:** _______________

**Verified By:** _______________

---

**Last Updated:** November 2024
