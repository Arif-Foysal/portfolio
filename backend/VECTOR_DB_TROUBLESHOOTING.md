# Vector Database Troubleshooting Guide

## Common Issues & Solutions

### Issue 0: Pydantic Enum Validation Error ⭐ FIXED

**What it means:**
```
Error in semantic caching: 1 validation error for ChatResponse
type
  Input should be 'text', 'projects_list', 'skills_list', 'education_list', 
  'experience_list', 'achievements_list' or 'contact_info' 
  [type=enum, input_value='education', input_type=str]
```

**Root Cause:**
- Stored response had invalid enum value: `"type": "education"` 
- Expected valid enum: `"type": "education_list"` (note the `_list` suffix)

**Solution (Already Applied ✅):**
- Updated `store_response()` to use correct MessageType enum values
- Added safe type conversion in chatbot service
- Valid enum values: `text`, `projects_list`, `skills_list`, `education_list`, `experience_list`, `achievements_list`, `contact_info`

**What to do:**
1. The fix is already applied
2. Optional: Clear old responses:
```sql
DELETE FROM chat_responses;
```
3. Restart backend and chat normally
4. New responses will use correct enum values

### Issue 1: "Expecting value: line 1 column 1 (char 0)" Error

**What it means:**
```
Error in semantic caching: Expecting value: line 1 column 1 (char 0)
```

This error occurs when the code tries to parse JSON but receives an empty string or non-JSON data.

**Root Cause:**
- Old responses were stored as plain text instead of JSON
- The retrieval code expects JSON format: `{ "type": "text", "data": "response" }`

**Solution (Already Applied ✅):**
- Updated `store_response()` to wrap all responses in JSON format
- Updated `_get_semantic_cached_response()` with fallback JSON parsing
- Gracefully handles both old (plain text) and new (JSON) response formats

**What to do:**
1. The fix is already applied to your code
2. Clear old responses from Supabase (optional):
```sql
DELETE FROM chat_responses;
```
3. New responses will be stored correctly as JSON

### Issue 2: Vector Search Returns No Results

**What it means:**
```
Found 0 similar responses for query: where did you complete your graduation...
```

This is **normal** behavior:
- First time asking → no similar responses exist yet
- Similarity threshold too high (>0.85)
- Question is genuinely unique

**Solution:**
- This is expected on first run
- After a few conversations, similar questions will start finding cached responses
- If most queries return 0 results, lower the threshold:

```python
# In chatbot.py, line ~193
similar_responses = await self.vector_store.search_similar_responses(
    message, 
    limit=1, 
    threshold=0.80  # Lower from 0.85 to find more loose matches
)
```

### Issue 3: Embeddings Generation Fails

**Error:**
```
Error generating embedding: ...
```

**Causes:**
- OPENAI_API_KEY not set or invalid
- OpenAI API rate limit exceeded
- Network connectivity issue

**Solution:**
1. Verify `.env` file has valid `OPENAI_API_KEY`:
```bash
echo $OPENAI_API_KEY  # Should not be empty
```

2. Check OpenAI API key is valid:
   - Go to https://platform.openai.com/account/api-keys
   - Regenerate if needed

3. Check rate limits:
   - Go to https://platform.openai.com/account/billing/overview
   - Ensure account has sufficient credits

### Issue 4: Supabase Connection Fails

**Error:**
```
⚠ Vector store initialization failed: ...
```

**Causes:**
- SUPABASE_URL or SUPABASE_KEY not set
- Database credentials invalid
- Network connectivity issue

**Solution:**
1. Verify `.env` file has correct values:
```bash
cat .env | grep SUPABASE
# Should show:
# SUPABASE_URL=https://xxx.supabase.co
# SUPABASE_KEY=eyJxxx...
```

2. Test Supabase connection manually:
```bash
curl https://your-supabase-url.supabase.co/rest/v1/chat_responses?select=count \
  -H "apikey: your-supabase-key"
```

3. If still failing, run Supabase setup again:
   - Follow instructions in `SUPABASE_SETUP.md`
   - Verify all 4 SQL queries executed successfully

### Issue 5: Table Does Not Exist Error

**Error:**
```
relation "chat_responses" does not exist
```

**Cause:**
- SQL setup queries from `SUPABASE_SETUP.md` were not executed

**Solution:**
1. Go to Supabase Dashboard → SQL Editor
2. Copy-paste and run all queries from `SUPABASE_SETUP.md` Step 1-3:
   - Enable pgvector extension
   - Create chat_responses table
   - Create match_chat_responses function

3. Verify table exists:
```sql
SELECT * FROM chat_responses LIMIT 1;
```

### Issue 6: RPC Function Not Found

**Error:**
```
function "match_chat_responses" does not exist
```

**Cause:**
- SQL query to create the RPC function wasn't executed (Step 3 in `SUPABASE_SETUP.md`)

**Solution:**
1. Copy the RPC function SQL from `SUPABASE_SETUP.md` Step 3
2. Paste into Supabase SQL Editor
3. Click Run
4. Verify it works:
```sql
SELECT * FROM match_chat_responses(
    (SELECT embedding FROM chat_responses LIMIT 1),
    0.85,
    1
);
```

### Issue 7: Dimension Mismatch

**Error:**
```
vector dimension mismatch: expected 1536 but got ...
```

**Cause:**
- Using wrong embedding model
- Mismatch between model output dimensions and table definition

**Solution:**
- Verify you're using `text-embedding-3-small` (which outputs 1536 dimensions)
- Do NOT use other models like:
  - `text-embedding-3-large` (3072 dimensions) ❌
  - `text-davinci-003` (not an embedding model) ❌

### Issue 8: Responses Not Being Stored

**What it means:**
```
Stored response for query: ...
# But nothing appears in Supabase
```

**Causes:**
- Supabase RLS policies blocking writes
- Write permissions not configured

**Solution:**
1. Check RLS is disabled or permissive:
```sql
-- In Supabase SQL Editor
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'chat_responses';
-- Should show: (chat_responses, t) - meaning RLS is enabled

-- Disable RLS for testing:
ALTER TABLE chat_responses DISABLE ROW LEVEL SECURITY;
```

2. Or create an RLS policy that allows writes:
```sql
CREATE POLICY "Allow all" ON chat_responses
  FOR ALL USING (true) WITH CHECK (true);
```

## Monitoring & Debugging

### Check Database Health

```sql
-- How many responses are stored?
SELECT COUNT(*) FROM chat_responses;

-- See recent responses
SELECT query, created_at FROM chat_responses 
ORDER BY created_at DESC LIMIT 10;

-- Check for errors in responses
SELECT COUNT(*) FROM chat_responses 
WHERE response IS NULL OR response = '';

-- Calculate average similarity (for tuning threshold)
SELECT AVG(1 - (e1.embedding <=> e2.embedding)) as avg_similarity
FROM chat_responses e1
CROSS JOIN chat_responses e2
WHERE e1.id != e2.id
LIMIT 100;
```

### Enable Debug Logging

In `backend/services/chatbot.py`, add debug prints:

```python
async def _get_semantic_cached_response(self, message: str, session_id: str):
    # ... existing code ...
    print(f"DEBUG: Searching for similar responses to: {message}")
    similar_responses = await self.vector_store.search_similar_responses(message, limit=1, threshold=0.85)
    print(f"DEBUG: Found {len(similar_responses)} similar responses")
    # ... rest of code ...
```

### Check OpenAI Embedding Costs

Go to https://platform.openai.com/account/billing/overview

Look for:
- `text-embedding-3-small`: Should be very cheap (~$0.02 per 1M tokens)
- This is the cheapest embedding model available

## Performance Optimization

### If searches are slow:

1. Check if indexes exist:
```sql
SELECT * FROM pg_indexes WHERE tablename = 'chat_responses';
```

2. Recreate indexes if needed:
```sql
CREATE INDEX IF NOT EXISTS chat_responses_embedding_idx 
ON chat_responses USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

3. Increase list parameter for better speed (accuracy tradeoff):
```sql
-- Lists = 100 is balanced (default)
-- Lists = 50  = faster search, less accurate
-- Lists = 200 = slower search, more accurate
```

### If embedding generation is slow:

1. Check OpenAI API status: https://status.openai.com/
2. Consider batching multiple embeddings in one request
3. Cache embeddings for very common questions

## Data Cleanup

### Clear all responses and start fresh:

```sql
DELETE FROM chat_responses;
-- Or for Supabase:
TRUNCATE TABLE chat_responses RESTART IDENTITY;
```

### Remove responses older than 30 days:

```sql
DELETE FROM chat_responses 
WHERE created_at < NOW() - INTERVAL '30 days';
```

### Keep only top 1000 most recent responses:

```sql
DELETE FROM chat_responses 
WHERE id NOT IN (
    SELECT id FROM chat_responses 
    ORDER BY created_at DESC 
    LIMIT 1000
);
```

## Still Having Issues?

1. **Check logs:** Look for detailed error messages in backend output
2. **Verify setup:** Re-run SUPABASE_SETUP.md Step 2-3
3. **Test components separately:**
   - Test OpenAI embedding API directly
   - Test Supabase connection directly
   - Test vector search manually
4. **Check documentation:** https://supabase.com/docs/guides/vector

## Next Steps

After fixing the issue:

1. ✅ Clear old responses: `DELETE FROM chat_responses;`
2. ✅ Restart backend
3. ✅ Send a test message - should see "Stored response for query..."
4. ✅ Send a similar question - should see "Found X similar responses..."
5. ✅ Monitor costs in OpenAI dashboard

---

**Version:** 2.0 (Updated with JSON response format fix)
**Last Updated:** 2025-11-04
