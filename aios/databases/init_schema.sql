-- ==============================================================================
-- ANTIGRAVITY OMEGA: MASTER RELATIONAL SCHEMA (SQLite WAL MODE)
-- ==============================================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

-- 1. SYSTEM METRICS TELEMETRY
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_percent REAL NOT NULL,
    ram_percent REAL NOT NULL,
    ram_free_gb REAL NOT NULL,
    gpu_vram_used_mb REAL,
    disk_c_free_gb REAL NOT NULL,
    disk_e_free_gb REAL NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('HEALTHY', 'WARNING', 'CRITICAL'))
);

CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp);

-- 2. SYSTEM SERVICE REGISTRY
CREATE TABLE IF NOT EXISTS services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    ring INTEGER NOT NULL DEFAULT 0,
    port INTEGER,
    pid INTEGER,
    status TEXT NOT NULL CHECK(status IN ('ONLINE', 'STOPPED', 'ERROR', 'DEGRADED')),
    last_health_check DATETIME,
    error_message TEXT
);

-- 3. UNIFIED AUDIT LOGS
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    category TEXT NOT NULL,
    details TEXT,
    severity TEXT NOT NULL DEFAULT 'INFO' CHECK(severity IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'))
);

CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);

-- 4. UNIFIED TASK REGISTRY
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('AI', 'DEV', 'AUTOMATION', 'BUSINESS', 'RESEARCH', 'MAINTENANCE')),
    priority TEXT NOT NULL CHECK(priority IN ('P0', 'P1', 'P2', 'P3')),
    status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED', 'CANCELLED')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- 5. IDEA & PRODUCT REGISTRY
CREATE TABLE IF NOT EXISTS ideas (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    problem TEXT NOT NULL,
    target_user TEXT,
    proposed_solution TEXT,
    mvp_scope TEXT,
    status TEXT NOT NULL DEFAULT 'BACKLOG' CHECK(status IN ('BACKLOG', 'RESEARCHING', 'VALIDATED', 'BUILDING', 'LAUNCHED', 'REJECTED')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. LIGHTWEIGHT CRM & NETWORK DIRECTORY
CREATE TABLE IF NOT EXISTS crm_contacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    company TEXT,
    role TEXT,
    email TEXT,
    linkedin_url TEXT,
    status TEXT NOT NULL DEFAULT 'LEAD' CHECK(status IN ('LEAD', 'CONTACTED', 'ENGAGED', 'PARTNER', 'ARCHIVED')),
    last_interaction DATETIME,
    notes TEXT
);

-- 7. KNOWLEDGE REPOSITORY & VECTOR INDEX METADATA
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    chunk_count INTEGER DEFAULT 0,
    embedded_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    header TEXT,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    content TEXT NOT NULL,
    terms TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunks_doc ON knowledge_chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_chunks_file ON knowledge_chunks(file_path);


CREATE TABLE IF NOT EXISTS saas_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stack TEXT NOT NULL,
    features TEXT,
    path TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    status TEXT DEFAULT 'active'
);
