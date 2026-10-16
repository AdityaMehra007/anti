import os
import json
import sqlite3

# Load nodes, workflows, and agents
nodes_path = r"e:\anti\data\n8n_node_catalog.json"
workflows_path = r"e:\anti\data\n8n_active_workflows.json"

nodes = json.load(open(nodes_path, encoding="utf-8"))
workflows = json.load(open(workflows_path, encoding="utf-8"))

# Inspect Agent skills in @n8n/agents
agents_dir = r"e:\anti\n8n-core\packages\@n8n\agents"
agent_files = []
if os.path.exists(agents_dir):
    for root, dirs, fnames in os.walk(agents_dir):
        for fn in fnames:
            if fn.endswith(".ts") and not fn.endswith(".test.ts"):
                rel = os.path.relpath(os.path.join(root, fn), agents_dir).replace("\\", "/")
                agent_files.append(rel)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>n8n Enterprise Automation & Autonomous Agent Command Center</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #090c15;
  --bg-card: rgba(18, 24, 38, 0.7);
  --bg-card-hover: rgba(27, 36, 56, 0.9);
  --border: rgba(255, 255, 255, 0.08);
  --n8n-orange: #ff6d5a;
  --n8n-glow: rgba(255, 109, 90, 0.2);
  --accent-blue: #38bdf8;
  --accent-purple: #c084fc;
  --accent-emerald: #34d399;
  --accent-amber: #fbbf24;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --code-bg: #05070f;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background-image: 
    radial-gradient(circle at 10% 15%, rgba(255, 109, 90, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 90% 85%, rgba(56, 189, 248, 0.06) 0%, transparent 40%);
}}

header {{
  padding: 1.1rem 2.2rem;
  border-bottom: 1px solid var(--border);
  background: rgba(9, 12, 21, 0.88);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}}

.logo-group {{
  display: flex;
  align-items: center;
  gap: 1rem;
}}

.n8n-badge {{
  background: linear-gradient(135deg, #ff6d5a 0%, #ea580c 100%);
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  padding: 0.4rem 0.8rem;
  border-radius: 10px;
  box-shadow: 0 4px 16px var(--n8n-glow);
  letter-spacing: -0.02em;
}}

.title-wrap h1 {{
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #ff6d5a 0%, #38bdf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.title-wrap p {{
  font-size: 0.75rem;
  color: var(--text-dim);
}}

.nav-tabs {{
  display: flex;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.04);
  padding: 0.3rem;
  border-radius: 12px;
  border: 1px solid var(--border);
}}

.tab-btn {{
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.45rem;
}}
.tab-btn:hover {{ color: var(--text); }}
.tab-btn.active {{
  background: var(--n8n-orange);
  color: #fff;
  box-shadow: 0 2px 12px var(--n8n-glow);
}}

.stats-bar {{
  display: flex;
  gap: 1.5rem;
  align-items: center;
}}
.stat-pill {{
  font-size: 0.8rem;
  color: var(--text-muted);
}}
.stat-pill strong {{
  color: var(--n8n-orange);
  font-family: 'JetBrains Mono', monospace;
}}

.container {{
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;
}}

/* Controls */
.controls-row {{
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}}
.search-box {{
  flex: 1;
  min-width: 300px;
  position: relative;
}}
.search-box input {{
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 0.8rem 1rem 0.8rem 2.8rem;
  border-radius: 12px;
  color: var(--text);
  font-family: inherit;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}}
.search-box input:focus {{
  outline: none;
  border-color: var(--n8n-orange);
  box-shadow: 0 0 0 3px var(--n8n-glow);
}}
.search-box svg {{
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
}}

.filter-pills {{
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}}
.pill {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  padding: 0.45rem 0.9rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}}
.pill:hover {{ border-color: rgba(255,255,255,0.2); color: var(--text); }}
.pill.active {{
  background: rgba(255, 109, 90, 0.15);
  border-color: var(--n8n-orange);
  color: var(--n8n-orange);
}}

/* Grid */
.grid-wrap {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.5rem;
}}
.card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  transition: all 0.25s ease;
  backdrop-filter: blur(12px);
}}
.card:hover {{
  border-color: rgba(255, 109, 90, 0.4);
  transform: translateY(-2px);
  background: var(--bg-card-hover);
}}
.card-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}}
.badge {{
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
}}
.badge-orange {{ background: rgba(255, 109, 90, 0.15); color: var(--n8n-orange); }}
.badge-blue {{ background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); }}
.badge-emerald {{ background: rgba(52, 211, 153, 0.15); color: var(--accent-emerald); }}

.card-title {{
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin-top: 0.35rem;
}}
.card-desc {{
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--text-muted);
  max-height: 100px;
  overflow-y: auto;
}}
.card-foot {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.78rem;
  color: var(--text-dim);
}}

/* Workflow Detail Split */
.split-layout {{
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 2rem;
  min-height: 600px;
}}
.sidebar {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 750px;
  overflow-y: auto;
}}
.side-item {{
  padding: 0.85rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}}
.side-item:hover {{ background: rgba(255, 255, 255, 0.05); }}
.side-item.active {{
  background: rgba(255, 109, 90, 0.12);
  border-color: var(--n8n-orange);
}}

.viewer {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
  max-height: 750px;
}}

pre {{
  background: var(--code-bg);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 1.25rem;
  overflow-x: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  line-height: 1.6;
  color: #e2e8f0;
}}

.btn {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}}
.btn-primary {{
  background: var(--n8n-orange);
  color: #fff;
  border: none;
}}
.btn-primary:hover {{
  background: #ff8575;
  box-shadow: 0 4px 16px var(--n8n-glow);
}}
</style>
</head>
<body>

<header>
  <div class="logo-group">
    <div class="n8n-badge">n8n</div>
    <div class="title-wrap">
      <h1>n8n Enterprise Automation & Agent Command Center</h1>
      <p>560 Core & Community Nodes • 14 Production Workflows • @n8n/agents Autonomous SDK</p>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('nodes')">🔌 Node Catalog (560)</button>
    <button class="tab-btn" onclick="switchTab('workflows')">⚡ Active Workflows (14)</button>
    <button class="tab-btn" onclick="switchTab('agents')">🤖 @n8n/agents SDK</button>
  </div>

  <div class="stats-bar">
    <div class="stat-pill">Nodes: <strong>{len(nodes)}</strong></div>
    <div class="stat-pill">Workflows: <strong>{len(workflows)}</strong></div>
    <div class="stat-pill">Agent SDK Files: <strong>{len(agent_files)}</strong></div>
  </div>
</header>

<main class="container">

  <!-- NODES TAB -->
  <section id="tab-nodes" class="tab-section">
    <div class="controls-row">
      <div class="search-box">
        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input type="text" id="node-search" placeholder="Search 560 nodes: AI, Telegram, Slack, Postgres, Webhook, Transform..." oninput="filterNodes()" />
      </div>
      <div class="filter-pills" id="node-group-filters"></div>
    </div>
    <div class="grid-wrap" id="nodes-grid"></div>
  </section>

  <!-- WORKFLOWS TAB -->
  <section id="tab-workflows" class="tab-section" style="display:none;">
    <div style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.35rem; font-weight: 700;">14 Production OMEGA Automation DAGs</h2>
      <p style="color: var(--text-muted); font-size: 0.85rem;">Autonomous operational cycles, financial settlement, threat monitors, and lead generation pipes.</p>
    </div>
    <div class="split-layout">
      <div class="sidebar" id="workflows-list"></div>
      <div class="viewer">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
          <div>
            <h3 id="wf-title" style="font-size: 1.25rem; font-weight: 700;">Workflow Name</h3>
            <span style="font-size: 0.75rem; color: var(--text-dim);" id="wf-file">filename.json</span>
          </div>
          <span class="badge badge-emerald" id="wf-node-count">0 Nodes</span>
        </div>
        <div>
          <h4 style="font-size: 0.85rem; color: var(--n8n-orange); margin-bottom: 0.5rem;">Configured Nodes</h4>
          <div id="wf-nodes-tags" style="display:flex; gap:0.5rem; flex-wrap:wrap;"></div>
        </div>
        <div>
          <h4 style="font-size: 0.85rem; color: var(--accent-blue); margin-bottom: 0.5rem;">Workflow DAG Specification (JSON)</h4>
          <pre><code id="wf-code">// Select workflow</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- AGENTS TAB -->
  <section id="tab-agents" class="tab-section" style="display:none;">
    <div style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.35rem; font-weight: 700;">@n8n/agents Autonomous Architecture</h2>
      <p style="color: var(--text-muted); font-size: 0.85rem;">Inspection of n8n's state-of-the-art native autonomous agent loop: vector stores (Supabase, Pinecone, Qdrant, Postgres), Daytona sandboxed workspaces, tool approvals, and runtime skills.</p>
    </div>
    <div class="split-layout">
      <div class="sidebar" id="agents-file-list"></div>
      <div class="viewer">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
          <div>
            <h3 id="agent-file-title" style="font-size: 1.15rem; font-weight: 700;">Agent Subsystem File</h3>
            <span style="font-size: 0.75rem; color: var(--text-dim);" id="agent-file-path">packages/@n8n/agents/</span>
          </div>
        </div>
        <pre><code id="agent-file-code">// Loading source code...</code></pre>
      </div>
    </div>
  </section>

</main>

<script>
const NODES = {json.dumps(nodes)};
const WORKFLOWS = {json.dumps(workflows)};
const AGENT_FILES = {json.dumps(agent_files)};

let activeGroup = 'All';
let selectedWfIndex = 0;
let selectedAgentFileIndex = 0;

function switchTab(tab) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-section').forEach(s => s.style.display = 'none');
  
  document.getElementById('tab-' + tab).style.display = 'block';
  event.currentTarget.classList.add('active');

  if (tab === 'nodes') renderNodes();
  if (tab === 'workflows') renderWorkflows();
  if (tab === 'agents') renderAgents();
}}

// Nodes
const groups = ['All', 'transform', 'trigger', 'input', 'output', 'utility'];

function initNodeFilters() {{
  const container = document.getElementById('node-group-filters');
  groups.forEach(g => {{
    const pill = document.createElement('button');
    pill.className = 'pill' + (g === 'All' ? ' active' : '');
    pill.textContent = g.toUpperCase();
    pill.onclick = (e) => {{
      document.querySelectorAll('#node-group-filters .pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeGroup = g;
      renderNodes();
    }};
    container.appendChild(pill);
  }});
}}

function renderNodes() {{
  const query = document.getElementById('node-search').value.toLowerCase();
  const grid = document.getElementById('nodes-grid');
  grid.innerHTML = '';

  const filtered = NODES.filter(n => {{
    const matchG = activeGroup === 'All' || n.group.toLowerCase().includes(activeGroup.toLowerCase());
    const matchQ = n.displayName.toLowerCase().includes(query) || n.name.toLowerCase().includes(query) || n.description.toLowerCase().includes(query);
    return matchG && matchQ;
  }});

  filtered.slice(0, 90).forEach(n => {{
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div>
        <div class="card-head">
          <span class="badge badge-orange">${{n.group || 'Utility'}}</span>
          <span style="font-size:0.75rem; color:var(--text-dim); font-family:'JetBrains Mono'">${{n.name}}</span>
        </div>
        <div class="card-title">${{n.displayName}}</div>
        <div class="card-desc" style="margin-top:0.5rem;">${{n.description || 'Core n8n integration node.'}}</div>
      </div>
      <div class="card-foot">
        <span>${{n.file.split('/').slice(-2).join('/')}}</span>
        <button class="btn" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="copyNodeName('${{n.name}}')">Copy ID</button>
      </div>
    `;
    grid.appendChild(card);
  }});
}}

function filterNodes() {{
  renderNodes();
}}

function copyNodeName(name) {{
  navigator.clipboard.writeText(name);
  alert('Copied node ID: ' + name);
}}

// Workflows
function renderWorkflows() {{
  const list = document.getElementById('workflows-list');
  list.innerHTML = '';

  WORKFLOWS.forEach((w, idx) => {{
    const item = document.createElement('div');
    item.className = 'side-item' + (idx === selectedWfIndex ? ' active' : '');
    item.innerHTML = `
      <div style="font-weight:700; font-size:0.92rem; color:var(--text);">${{w.name}}</div>
      <div style="font-size:0.75rem; color:var(--text-dim);">${{w.nodes_count}} Nodes • ${{w.filename}}</div>
    `;
    item.onclick = () => {{
      selectedWfIndex = idx;
      renderWorkflows();
      displayWorkflowDetails();
    }};
    list.appendChild(item);
  }});
  displayWorkflowDetails();
}}

function displayWorkflowDetails() {{
  const w = WORKFLOWS[selectedWfIndex];
  document.getElementById('wf-title').textContent = w.name;
  document.getElementById('wf-file').textContent = 'workflows/' + w.filename;
  document.getElementById('wf-node-count').textContent = w.nodes_count + ' Nodes';

  const tags = document.getElementById('wf-nodes-tags');
  tags.innerHTML = '';
  w.nodes.forEach(n => {{
    const t = document.createElement('span');
    t.className = 'badge badge-blue';
    t.textContent = n;
    tags.appendChild(t);
  }});

  document.getElementById('wf-code').textContent = JSON.stringify(w.raw, null, 2);
}}

// Agents
function renderAgents() {{
  const list = document.getElementById('agents-file-list');
  list.innerHTML = '';

  AGENT_FILES.forEach((f, idx) => {{
    const item = document.createElement('div');
    item.className = 'side-item' + (idx === selectedAgentFileIndex ? ' active' : '');
    item.innerHTML = `
      <div style="font-weight:600; font-size:0.85rem; color:var(--text);">${{f.split('/').pop()}}</div>
      <div style="font-size:0.72rem; color:var(--text-dim);">${{f}}</div>
    `;
    item.onclick = () => {{
      selectedAgentFileIndex = idx;
      renderAgents();
      loadAgentFile();
    }};
    list.appendChild(item);
  }});
  loadAgentFile();
}}

function loadAgentFile() {{
  const f = AGENT_FILES[selectedAgentFileIndex];
  document.getElementById('agent-file-title').textContent = f.split('/').pop();
  document.getElementById('agent-file-path').textContent = 'packages/@n8n/agents/' + f;
  document.getElementById('agent-file-code').textContent = '// Path: packages/@n8n/agents/' + f + '\\n// Inspecting file from local n8n-core repository';
}}

// Init
initNodeFilters();
renderNodes();
</script>
</body>
</html>
'''

out_file = r"e:\anti\n8n_command_center.html"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated n8n_command_center.html successfully ({len(html_content)} bytes)!")
