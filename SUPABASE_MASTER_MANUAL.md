# Supabase Master Architecture & Operations Manual

This repository hosts a production-grade, turn-key **Supabase** infrastructure and client integration suite. It supports local self-hosting via Docker Compose as well as connecting to any Supabase Cloud instance.

---

## 1. Architecture Overview

Supabase is an open-source Firebase alternative built on top of enterprise PostgreSQL:

| Component | Technology | Default Port / Route | Description |
|---|---|---|---|
| **API Gateway** | Kong | `:8000` / `:8443` | Reverse proxy and ingress router for all Supabase microservices |
| **Studio UI** | Next.js | `:3000` | Web administration console (table editor, SQL runner, auth manager) |
| **REST API** | PostgREST | `:8000/rest/v1` | Instant auto-generated OpenAPI REST endpoints from PostgreSQL schema |
| **Auth** | GoTrue | `:8000/auth/v1` | JWT user management, OAuth social logins, and passwordless auth |
| **Realtime** | Elixir Phoenix | `:8000/realtime/v1` | WebSocket server for database changes and presence broadcasting |
| **Storage** | Storage API | `:8000/storage/v1` | Object storage with fine-grained Postgres RLS authorization |
| **Database** | PostgreSQL 15 | `:5432` | Relational engine with `uuid-ossp`, `pgcrypto`, and `pgvector` |

---

## 2. Quick Start: Local Self-Hosting

### Launching the Stack
Run the Windows batch launcher from the repository root:
```cmd
START_SUPABASE.bat
```
Or via PowerShell:
```powershell
.\START_SUPABASE.ps1 -Action up
```

### Stopping the Stack
```powershell
.\START_SUPABASE.ps1 -Action down
```

### Viewing Logs
```powershell
.\START_SUPABASE.ps1 -Action logs
```

---

## 3. Database Schema & Security (Row Level Security)

Initial migrations are maintained under `supabase/migrations/`:
- [`20260917000001_init_schema.sql`](file:///e:/anti/supabase/migrations/20260917000001_init_schema.sql)
- Seed data: [`supabase/seed.sql`](file:///e:/anti/supabase/seed.sql)

### Row Level Security (RLS) Rules:
1. **Always enable RLS**: Every newly created table must execute `ALTER TABLE <name> ENABLE ROW LEVEL SECURITY;`.
2. **Profiles Table**: Automatically synchronized on new user signups via `on_auth_user_created` trigger.
3. **Knowledge Embeddings (`pgvector`)**: Stores AI agent memories with 1536-dimensional embeddings and IVFFlat index.

### Vector Similarity Search:
Execute semantic matching using the pre-installed RPC:
```sql
SELECT * FROM match_knowledge_embeddings(
    query_embedding := '[0.012, -0.043, ...]'::vector(1536),
    match_threshold := 0.75,
    match_count := 5
);
```

---

## 4. Multi-Language SDK Clients

### Python Client (`supabase_client.py`)
Zero-dependency client operating out of the box with standard library HTTP:

```python
import supabase_client

client = supabase_client.get_client()

# Query rows
profiles = client.select("profiles", select="id,username,role")

# Insert row
new_log = client.insert("audit_logs", {
    "action": "DOCUMENT_UPLOAD",
    "details": {"doc": "manual.pdf"}
})

# Call RPC function
results = client.rpc("match_knowledge_embeddings", {
    "query_embedding": [...],
    "match_threshold": 0.7
})
```

### Node.js Client (`supabase_client.js`)
Zero-dependency client leveraging native Node.js `fetch`:

```javascript
const { createClient } = require('./supabase_client');
const client = createClient();

async function run() {
  const { data, error } = await client.select('profiles');
  console.log('Profiles:', data);
}
run();
```

---

## 5. Connecting to Supabase Cloud

To redirect clients to a hosted Supabase Cloud project instead of local Docker:
1. Set the following environment variables in your shell or `.env`:
   ```env
   SUPABASE_URL=https://<your-project-ref>.supabase.co
   SUPABASE_ANON_KEY=<your-project-anon-key>
   SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
   ```
2. The clients (`supabase_client.py` and `supabase_client.js`) will automatically pick up the cloud URL and keys.

---

## 6. Control Center & Diagnostics

Launch the interactive control center in any browser:
- [`SUPABASE_CONTROL_CENTER.html`](file:///e:/anti/SUPABASE_CONTROL_CENTER.html)

Or run the automated diagnostic verification suite from terminal:
```powershell
python scripts/verify_supabase.py --dry-run
```
