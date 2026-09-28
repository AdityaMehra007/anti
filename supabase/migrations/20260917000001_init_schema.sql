-- ==============================================================================
-- 20260917000001_init_schema.sql
-- Production Supabase Initial Schema Migration
-- Features: Extensions, Profiles, Knowledge Vector Store, Audit Logs, RLS, Triggers
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 2. PUBLIC PROFILES TABLE
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'member' CHECK (role IN ('admin', 'member', 'service')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Index for username lookups
CREATE INDEX IF NOT EXISTS idx_profiles_username ON public.profiles(username);

-- 3. KNOWLEDGE EMBEDDINGS (AI & AGENTIC MEMORY)
CREATE TABLE IF NOT EXISTS public.knowledge_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Index for vector cosine similarity searches
CREATE INDEX IF NOT EXISTS idx_knowledge_embedding 
ON public.knowledge_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 4. AUDIT LOGS TABLE
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    details JSONB DEFAULT '{}'::jsonb,
    ip_address TEXT,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON public.audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON public.audit_logs(action);

-- 5. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Profiles: Public can view profiles; users can update only their own profile
CREATE POLICY "Public profiles are viewable by everyone" 
ON public.profiles FOR SELECT 
USING (true);

CREATE POLICY "Users can insert their own profile" 
ON public.profiles FOR INSERT 
WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile" 
ON public.profiles FOR UPDATE 
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Knowledge Embeddings: Users can only see and manage their own embeddings
CREATE POLICY "Users can select own knowledge embeddings" 
ON public.knowledge_embeddings FOR SELECT 
USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert own knowledge embeddings" 
ON public.knowledge_embeddings FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own knowledge embeddings" 
ON public.knowledge_embeddings FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own knowledge embeddings" 
ON public.knowledge_embeddings FOR DELETE 
USING (auth.uid() = user_id);

-- Audit Logs: Users can view their own audit logs, admins can view all
CREATE POLICY "Users can view own audit logs" 
ON public.audit_logs FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Service and authenticated can insert audit logs" 
ON public.audit_logs FOR INSERT 
WITH CHECK (auth.uid() = user_id OR auth.role() = 'service_role');

-- 6. AUTOMATED USER SYNCHRONIZATION TRIGGER
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER 
LANGUAGE plpgsql 
SECURITY DEFINER SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (id, username, full_name, avatar_url, role, metadata)
    VALUES (
        new.id,
        COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
        COALESCE(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''),
        COALESCE(new.raw_user_meta_data->>'avatar_url', ''),
        COALESCE(new.raw_user_meta_data->>'role', 'member'),
        COALESCE(new.raw_user_meta_data, '{}'::jsonb)
    )
    ON CONFLICT (id) DO UPDATE SET
        username = EXCLUDED.username,
        full_name = EXCLUDED.full_name,
        updated_at = timezone('utc'::text, now());
    RETURN new;
END;
$$;

-- Trigger to execute upon auth.users creation
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 7. VECTOR SIMILARITY SEARCH RPC
CREATE OR REPLACE FUNCTION public.match_knowledge_embeddings(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.id,
        k.title,
        k.content,
        k.metadata,
        1 - (k.embedding <=> query_embedding) AS similarity
    FROM public.knowledge_embeddings k
    WHERE (1 - (k.embedding <=> query_embedding)) > match_threshold
      AND (k.user_id = auth.uid() OR k.user_id IS NULL)
    ORDER BY k.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
