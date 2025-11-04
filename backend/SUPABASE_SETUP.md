# Supabase Vector Database Setup Guide

This guide explains how to set up pgvector for semantic caching in your Supabase project.

## Prerequisites
- A Supabase account (free tier works fine)
- Your existing Supabase project linked in `.env`

## Step 1: Enable pgvector Extension

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **SQL Editor** in the left sidebar
4. Click **New Query**
5. Paste and run this SQL:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

Click **Run** to execute the query. You should see a success message.

## Step 2: Create chat_responses Table

Create a new query and paste the following SQL:

```sql
-- Create chat_responses table with vector embeddings
CREATE TABLE IF NOT EXISTS chat_responses (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embeddings are 1536 dimensions
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster vector similarity search
CREATE INDEX IF NOT EXISTS chat_responses_embedding_idx 
ON chat_responses USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for faster text search
CREATE INDEX IF NOT EXISTS chat_responses_query_idx 
ON chat_responses USING GIN (to_tsvector('english', query));
```

Click **Run** to execute.

## Step 3: Create Vector Similarity Search Function

Create a new query and paste:

```sql
-- Create RPC function for vector similarity search
CREATE OR REPLACE FUNCTION match_chat_responses(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.85,
    match_count int DEFAULT 1
)
RETURNS TABLE (
    id bigint,
    query text,
    response text,
    metadata jsonb,
    similarity float
)
LANGUAGE sql STABLE
AS $$
  SELECT
    chat_responses.id,
    chat_responses.query,
    chat_responses.response,
    chat_responses.metadata,
    1 - (chat_responses.embedding <=> query_embedding) as similarity
  FROM chat_responses
  WHERE 1 - (chat_responses.embedding <=> query_embedding) > match_threshold
  ORDER BY chat_responses.embedding <=> query_embedding
  LIMIT match_count;
$$;
```

Click **Run** to execute.

## Step 4: Configure Row Level Security (RLS) - Optional but Recommended

For security, you might want to add RLS policies:

```sql
-- Enable RLS
ALTER TABLE chat_responses ENABLE ROW LEVEL SECURITY;

-- Create policy to allow inserts and selects (adjust as needed)
CREATE POLICY "Allow API to insert and select" ON chat_responses
FOR ALL USING (true) WITH CHECK (true);
```

## Step 5: Verify Setup

Run this query to check if everything is working:

```sql
-- Test query
SELECT id, query, response, created_at 
FROM chat_responses 
LIMIT 5;
```

You should see an empty result (no errors).

## Step 6: Test Vector Search

Once you have some data, you can test the search function:

```sql
-- This will test after your chatbot stores some responses
SELECT * FROM match_chat_responses(
    (SELECT embedding FROM chat_responses LIMIT 1),
    0.85,
    3
) WHERE id > 0;
```

## Troubleshooting

### Extension not found error
- Make sure you ran the `CREATE EXTENSION vector` command first
- You need to be a admin/owner of the database

### Function not found error
- Make sure the `match_chat_responses` function was created successfully
- Check if RLS is preventing access (disable temporarily to test)

### Vector dimension mismatch
- Make sure you're using `text-embedding-3-small` model in your code
- This model outputs 1536-dimensional vectors
- Don't use other embedding models without adjusting the dimension

## Monitoring Usage

To see your stored responses:

```sql
SELECT COUNT(*) as total_responses FROM chat_responses;

-- See recent responses
SELECT query, similarity FROM chat_responses 
ORDER BY created_at DESC 
LIMIT 10;
```

To clean up old data (optional):

```sql
-- Delete responses older than 30 days
DELETE FROM chat_responses 
WHERE created_at < NOW() - INTERVAL '30 days';
```

## Cost Considerations

- **Embedding API calls**: ~$0.02 per 1M tokens (very cheap)
- **Storage**: 1KB per response on average (included in free tier)
- **Vector similarity search**: Free (very fast)

This setup can reduce your OpenAI API costs by 50-70%! 🚀

## Next Steps

1. Your backend is now ready to use the vector store
2. First time you run, it will automatically create embeddings
3. Monitor your Supabase usage in the dashboard
4. The vector store will be populated as users chat with your bot

## Questions?

Check the Supabase docs: https://supabase.com/docs/guides/vector
