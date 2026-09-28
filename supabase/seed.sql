-- ==============================================================================
-- seed.sql
-- Development Seed Data for Supabase
-- ==============================================================================

-- Seed a dummy system profile (if no auth trigger created one yet)
INSERT INTO public.profiles (id, username, full_name, role, metadata)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'system_admin',
    'Antigravity System Admin',
    'admin',
    '{"department": "Core Infrastructure", "verified": true}'::jsonb
)
ON CONFLICT (id) DO NOTHING;

-- Seed sample knowledge documents for testing
INSERT INTO public.knowledge_embeddings (id, user_id, title, content, metadata)
VALUES 
(
    '10000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000001',
    'Supabase Architecture Primer',
    'Supabase combines PostgreSQL, PostgREST, GoTrue, Realtime, and pgvector into a unified developer platform.',
    '{"category": "architecture", "tags": ["database", "postgres", "supabase"]}'::jsonb
),
(
    '10000000-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000001',
    'Row Level Security Guidelines',
    'Always enable RLS on every table. Default deny, explicit allow using auth.uid() or security definer functions.',
    '{"category": "security", "tags": ["rls", "postgres", "security"]}'::jsonb
)
ON CONFLICT (id) DO NOTHING;

-- Seed an initial audit record
INSERT INTO public.audit_logs (user_id, action, details, ip_address)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'SYSTEM_BOOTSTRAP',
    '{"status": "initialized", "version": "1.0.0"}'::jsonb,
    '127.0.0.1'
);
