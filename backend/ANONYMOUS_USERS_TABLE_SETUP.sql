-- SQL to create the anonymous_users table in Supabase
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS anonymous_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_uuid UUID NOT NULL UNIQUE,
    supabase_user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    is_anonymous BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_active TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_anonymous_users_client_uuid ON anonymous_users(client_uuid);
CREATE INDEX IF NOT EXISTS idx_anonymous_users_supabase_id ON anonymous_users(supabase_user_id);
CREATE INDEX IF NOT EXISTS idx_anonymous_users_last_active ON anonymous_users(last_active);

-- Enable Row Level Security
ALTER TABLE anonymous_users ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS (adjust as needed for your security requirements)
CREATE POLICY "Allow all operations for anonymous users" ON anonymous_users
    FOR ALL USING (true);

-- Add a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for automatic updated_at updates
CREATE TRIGGER update_anonymous_users_updated_at 
    BEFORE UPDATE ON anonymous_users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE anonymous_users IS 'Stores mapping between client UUIDs and Supabase anonymous user IDs for reconnection';
COMMENT ON COLUMN anonymous_users.client_uuid IS 'Client-side generated UUID for reconnection across sessions';
COMMENT ON COLUMN anonymous_users.supabase_user_id IS 'Reference to the actual Supabase auth user ID';
COMMENT ON COLUMN anonymous_users.is_anonymous IS 'Flag to indicate this is an anonymous user';
COMMENT ON COLUMN anonymous_users.last_active IS 'Timestamp of last user activity for cleanup purposes';
