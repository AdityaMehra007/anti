import json

questions = json.load(open(r'e:\anti\data\react_interview_questions.json', encoding='utf-8'))
coding = json.load(open(r'e:\anti\data\react_full_coding_suite.json', encoding='utf-8'))

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>React Mastery & Interview Command Center</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg-dark: #0a0e17;
  --bg-card: rgba(18, 24, 38, 0.7);
  --bg-card-hover: rgba(26, 35, 54, 0.9);
  --border: rgba(255, 255, 255, 0.08);
  --border-focus: rgba(97, 218, 251, 0.5);
  --react-blue: #61dafb;
  --react-glow: rgba(97, 218, 251, 0.15);
  --accent-purple: #a855f7;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --code-bg: #05070d;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  background-color: var(--bg-dark);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background-image: 
    radial-gradient(circle at 15% 10%, rgba(97, 218, 251, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 85% 80%, rgba(168, 85, 247, 0.06) 0%, transparent 40%);
}

header {
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(10, 14, 23, 0.85);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.react-logo {
  animation: spin 20s linear infinite;
  width: 34px;
  height: 34px;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

.title-wrap h1 {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #61dafb 0%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.title-wrap p {
  font-size: 0.75rem;
  color: var(--text-dim);
}

.nav-tabs {
  display: flex;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.04);
  padding: 0.3rem;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.tab-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.45rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.tab-btn:hover { color: var(--text-main); }
.tab-btn.active {
  background: var(--react-blue);
  color: #0a0e17;
  box-shadow: 0 2px 12px rgba(97, 218, 251, 0.3);
}

.stats-bar {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.stat-pill {
  font-size: 0.78rem;
  color: var(--text-muted);
}
.stat-pill strong {
  color: var(--react-blue);
  font-family: 'JetBrains Mono', monospace;
}

.container {
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;
}

/* Controls */
.controls-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}
.search-box {
  flex: 1;
  min-width: 280px;
  position: relative;
}
.search-box input {
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 0.8rem 1rem 0.8rem 2.8rem;
  border-radius: 12px;
  color: var(--text-main);
  font-family: inherit;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}
.search-box input:focus {
  outline: none;
  border-color: var(--react-blue);
  box-shadow: 0 0 0 3px var(--react-glow);
}
.search-box svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
}

.filter-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.pill {
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  padding: 0.45rem 0.9rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pill:hover { border-color: rgba(255,255,255,0.2); color: var(--text-main); }
.pill.active {
  background: rgba(97, 218, 251, 0.12);
  border-color: var(--react-blue);
  color: var(--react-blue);
}

/* Flashcard View */
.flashcard-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 820px;
  margin: 0 auto;
  gap: 1.5rem;
}
.flashcard {
  width: 100%;
  min-height: 440px;
  perspective: 1000px;
  cursor: pointer;
}
.flashcard-inner {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 440px;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}
.flashcard.flipped .flashcard-inner {
  transform: rotateY(180deg);
}
.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  border-radius: 20px;
  border: 1px solid var(--border);
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.card-back {
  transform: rotateY(180deg);
  overflow-y: auto;
  justify-content: flex-start;
  gap: 1.25rem;
  background: rgba(14, 20, 32, 0.95);
}

.card-badge {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--react-blue);
  background: rgba(97, 218, 251, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  align-self: flex-start;
}
.card-q {
  font-size: 1.45rem;
  font-weight: 700;
  line-height: 1.4;
  margin: 2rem 0;
}
.flip-hint {
  font-size: 0.8rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.card-ans-text {
  font-size: 0.95rem;
  line-height: 1.65;
  color: #cbd5e1;
}

.flashcard-nav {
  display: flex;
  gap: 1rem;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}
.btn {
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-main);
  padding: 0.7rem 1.4rem;
  border-radius: 10px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}
.btn-primary {
  background: var(--react-blue);
  color: #0a0e17;
  border: none;
}
.btn-primary:hover {
  background: #7ee0fb;
  box-shadow: 0 4px 16px rgba(97, 218, 251, 0.4);
}
.btn-success {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.3);
  color: var(--accent-emerald);
}
.btn-success:hover {
  background: rgba(16, 185, 129, 0.25);
}

/* Grid View */
.grid-wrap {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 1.5rem;
}
.q-card {
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
}
.q-card:hover {
  border-color: rgba(97, 218, 251, 0.3);
  transform: translateY(-2px);
  background: var(--bg-card-hover);
}
.q-card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}
.q-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--react-blue);
  background: rgba(97, 218, 251, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}
.q-title {
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.45;
  color: var(--text-main);
  margin-top: 0.5rem;
}
.q-body {
  font-size: 0.88rem;
  line-height: 1.6;
  color: var(--text-muted);
  max-height: 180px;
  overflow-y: auto;
  padding-right: 0.5rem;
}
.q-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* Projects & Code View */
.projects-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  min-height: 600px;
}
.projects-sidebar {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 750px;
  overflow-y: auto;
}
.proj-item {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.proj-item:hover {
  background: rgba(255, 255, 255, 0.05);
}
.proj-item.active {
  background: rgba(97, 218, 251, 0.12);
  border-color: var(--react-blue);
}
.proj-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-main);
}
.proj-desc {
  font-size: 0.75rem;
  color: var(--text-dim);
}

.proj-viewer {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
  max-height: 750px;
}
.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
}
.file-selector {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.file-tab {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  cursor: pointer;
}
.file-tab.active {
  background: var(--react-blue);
  color: #0a0e17;
  font-weight: 600;
}

pre {
  background: var(--code-bg);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 1.25rem;
  overflow-x: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  color: #e2e8f0;
}
code {
  font-family: 'JetBrains Mono', monospace;
}

/* Custom Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

/* Responsive */
@media (max-width: 900px) {
  .projects-layout { grid-template-columns: 1fr; }
  .grid-wrap { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<header>
  <div class="logo-group">
    <svg class="react-logo" viewBox="-11.5 -10.23174 23 20.46348">
      <circle cx="0" cy="0" r="2.05" fill="#61dafb"/>
      <g stroke="#61dafb" stroke-width="1" fill="none">
        <ellipse rx="11" ry="4.2"/>
        <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
        <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
      </g>
    </svg>
    <div class="title-wrap">
      <h1>React Interview & Coding Command Center</h1>
      <p>444 Questions • 13 Interactive Mini-Apps • 8 Custom Hooks • 4 Diagnostic Labs</p>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchView('flashcards')">
      🎴 Flashcards
    </button>
    <button class="tab-btn" onclick="switchView('browse')">
      📚 Browse Catalog
    </button>
    <button class="tab-btn" onclick="switchView('top50')">
      ⭐ Senior Top 50
    </button>
    <button class="tab-btn" onclick="switchView('projects')">
      💻 13 Coding Apps
    </button>
    <button class="tab-btn" onclick="switchView('hooks')">
      ⚡ 8 Custom Hooks
    </button>
    <button class="tab-btn" onclick="switchView('labs')">
      🔬 4 Diagnostic Labs
    </button>
  </div>

  <div class="stats-bar">
    <div class="stat-pill">Mastered: <strong id="stat-mastered">0</strong> / 444</div>
    <div class="stat-pill">Confidence: <strong id="stat-pct">0%</strong></div>
  </div>
</header>

<main class="container">

  <!-- FLASHCARDS VIEW -->
  <section id="view-flashcards" class="view-section">
    <div class="controls-row">
      <div class="filter-pills" id="fc-category-filters"></div>
      <button class="btn" onclick="shuffleCards()">🔀 Shuffle</button>
    </div>

    <div class="flashcard-wrap">
      <div class="flashcard" id="active-flashcard" onclick="toggleFlip()">
        <div class="flashcard-inner">
          <div class="card-face card-front">
            <div>
              <span class="card-badge" id="fc-category">Category</span>
              <div class="q-title" id="fc-question" style="font-size: 1.5rem; margin-top: 1.5rem;">Loading question...</div>
            </div>
            <div class="flip-hint">
              <span>Click or press <strong>Space</strong> to reveal answer</span>
            </div>
          </div>
          <div class="card-face card-back">
            <span class="card-badge" id="fc-back-category">Answer</span>
            <div class="card-ans-text" id="fc-answer">Answer text...</div>
          </div>
        </div>
      </div>

      <div class="flashcard-nav">
        <button class="btn" onclick="prevCard()">← Previous</button>
        <div style="display:flex; gap: 0.5rem;">
          <button class="btn btn-success" onclick="toggleMasteredCurrent()" id="btn-master-toggle">Mark Mastered</button>
        </div>
        <button class="btn btn-primary" onclick="nextCard()">Next →</button>
      </div>
      <div style="color: var(--text-dim); font-size: 0.8rem;" id="fc-counter">Card 1 of 444</div>
    </div>
  </section>

  <!-- BROWSE CATALOG VIEW -->
  <section id="view-browse" class="view-section" style="display:none;">
    <div class="controls-row">
      <div class="search-box">
        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input type="text" id="browse-search" placeholder="Search questions, concepts, hooks, redux, reconciliation..." oninput="filterBrowse()" />
      </div>
      <div class="filter-pills" id="browse-category-filters"></div>
    </div>
    <div class="grid-wrap" id="browse-grid"></div>
  </section>

  <!-- SENIOR TOP 50 VIEW -->
  <section id="view-top50" class="view-section" style="display:none;">
    <div style="margin-bottom: 2rem;">
      <h2 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Staff & Senior Frontend High-Signal Questions</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem;">Curated selection covering React Fiber, reconciliation architecture, synthetic event pooling, concurrency, SSR streaming, and high-performance patterns.</p>
    </div>
    <div class="grid-wrap" id="top50-grid"></div>
  </section>

  <!-- 13 CODING PROJECTS VIEW -->
  <section id="view-projects" class="view-section" style="display:none;">
    <div style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.4rem; font-weight: 700;">13 Battle-Tested Machine Coding Projects</h2>
      <p style="color: var(--text-muted); font-size: 0.85rem;">Full source files, component architectures, and specifications for classic machine-coding rounds.</p>
    </div>
    <div class="projects-layout">
      <div class="projects-sidebar" id="projects-list"></div>
      <div class="proj-viewer">
        <div class="viewer-header">
          <div>
            <h3 id="pv-title" style="font-size: 1.2rem; font-weight: 700;">Project Name</h3>
            <span style="font-size: 0.75rem; color: var(--text-dim);" id="pv-path">coding-projects/</span>
          </div>
          <div class="file-selector" id="pv-file-selector"></div>
        </div>
        <div id="pv-readme-box" style="font-size: 0.9rem; line-height: 1.6; color: var(--text-muted);"></div>
        <div>
          <h4 style="font-size: 0.85rem; color: var(--react-blue); margin-bottom: 0.5rem;" id="pv-code-header">Source Code</h4>
          <pre><code id="pv-code">// Select a file to inspect</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- 8 CUSTOM HOOKS VIEW -->
  <section id="view-hooks" class="view-section" style="display:none;">
    <div style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.4rem; font-weight: 700;">8 Essential Production React Hooks</h2>
      <p style="color: var(--text-muted); font-size: 0.85rem;">Clean implementations and test harnesses for usePrevious, useDebounce, useThrottle, useFetch, and more.</p>
    </div>
    <div class="projects-layout">
      <div class="projects-sidebar" id="hooks-list"></div>
      <div class="proj-viewer">
        <div class="viewer-header">
          <h3 id="hv-title" style="font-size: 1.2rem; font-weight: 700;">Hook Implementation</h3>
          <div class="file-selector">
            <button class="file-tab active" id="hv-tab-hook" onclick="showHookTab('hook')">Hook Implementation (.ts)</button>
            <button class="file-tab" id="hv-tab-demo" onclick="showHookTab('demo')">Interactive Demo (App.tsx)</button>
          </div>
        </div>
        <pre><code id="hv-code">// Select a hook to inspect</code></pre>
      </div>
    </div>
  </section>

  <!-- 4 DIAGNOSTIC LABS VIEW -->
  <section id="view-labs" class="view-section" style="display:none;">
    <div style="margin-bottom: 1.5rem;">
      <h2 style="font-size: 1.4rem; font-weight: 700;">4 Diagnostic Coding Exercises (Problem vs Solution)</h2>
      <p style="color: var(--text-muted); font-size: 0.85rem;">Debug real-world React traps: state batching, stale useEffect closures, useCallback memoization breakdowns, and custom hook abstractions.</p>
    </div>
    <div class="projects-layout">
      <div class="projects-sidebar" id="labs-list"></div>
      <div class="proj-viewer">
        <div class="viewer-header">
          <h3 id="lv-title" style="font-size: 1.2rem; font-weight: 700;">Exercise</h3>
          <div class="file-selector">
            <button class="file-tab active" id="lv-tab-prob" onclick="showLabTab('prob')" style="border-color: var(--accent-rose); color: var(--accent-rose);">Problem (Buggy Code)</button>
            <button class="file-tab" id="lv-tab-sol" onclick="showLabTab('sol')" style="border-color: var(--accent-emerald); color: var(--accent-emerald);">Verified Solution</button>
          </div>
        </div>
        <pre><code id="lv-code">// Select a diagnostic lab to inspect</code></pre>
      </div>
    </div>
  </section>

</main>

<script>
const QUESTIONS = ''' + json.dumps(questions) + ''';
const CODING = ''' + json.dumps(coding) + ''';

// State
let masteredIds = new Set(JSON.parse(localStorage.getItem('react_mastered_ids') || '[]'));
let activeCategory = 'All';
let currentCardIndex = 0;
let filteredCards = [...QUESTIONS];
let selectedProjectIndex = 0;
let selectedProjectFile = '';
let selectedHookIndex = 0;
let currentHookView = 'hook';
let selectedLabIndex = 0;
let currentLabView = 'prob';

function saveMastered() {
  localStorage.setItem('react_mastered_ids', JSON.stringify([...masteredIds]));
  updateStats();
}

function updateStats() {
  const mCount = masteredIds.size;
  document.getElementById('stat-mastered').textContent = mCount;
  const pct = Math.round((mCount / QUESTIONS.length) * 100);
  document.getElementById('stat-pct').textContent = pct + '%';
}

function switchView(viewName) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.view-section').forEach(sec => sec.style.display = 'none');
  
  const targetSec = document.getElementById('view-' + viewName);
  if (targetSec) targetSec.style.display = 'block';

  // Mark tab active
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(t => {
    if (t.getAttribute('onclick').includes(viewName)) t.classList.add('active');
  });

  if (viewName === 'browse') renderBrowse();
  if (viewName === 'top50') renderTop50();
  if (viewName === 'projects') renderProjects();
  if (viewName === 'hooks') renderHooks();
  if (viewName === 'labs') renderLabs();
}

// Categories
const categories = ['All', ...new Set(QUESTIONS.map(q => q.category))];

function initCategories() {
  const fcCont = document.getElementById('fc-category-filters');
  const brCont = document.getElementById('browse-category-filters');
  
  categories.forEach(cat => {
    const p1 = document.createElement('button');
    p1.className = 'pill' + (cat === 'All' ? ' active' : '');
    p1.textContent = cat;
    p1.onclick = () => filterByCategory(cat, p1, 'fc');
    fcCont.appendChild(p1);

    const p2 = document.createElement('button');
    p2.className = 'pill' + (cat === 'All' ? ' active' : '');
    p2.textContent = cat;
    p2.onclick = () => filterByCategory(cat, p2, 'browse');
    brCont.appendChild(p2);
  });
}

function filterByCategory(cat, pillEl, view) {
  activeCategory = cat;
  pillEl.parentElement.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  pillEl.classList.add('active');
  
  if (view === 'fc') {
    filteredCards = cat === 'All' ? [...QUESTIONS] : QUESTIONS.filter(q => q.category === cat);
    currentCardIndex = 0;
    renderFlashcard();
  } else {
    renderBrowse();
  }
}

// Flashcard Controls
function renderFlashcard() {
  if (filteredCards.length === 0) return;
  const q = filteredCards[currentCardIndex];
  document.getElementById('fc-category').textContent = q.category;
  document.getElementById('fc-back-category').textContent = q.category + ' • #' + q.number;
  document.getElementById('fc-question').textContent = q.question;
  document.getElementById('fc-answer').innerHTML = formatMarkdown(q.answer);
  document.getElementById('fc-counter').textContent = `Card ${currentCardIndex + 1} of ${filteredCards.length}`;
  
  const card = document.getElementById('active-flashcard');
  card.classList.remove('flipped');

  const mBtn = document.getElementById('btn-master-toggle');
  if (masteredIds.has(q.number)) {
    mBtn.textContent = '✓ Mastered';
    mBtn.classList.add('btn-primary');
    mBtn.classList.remove('btn-success');
  } else {
    mBtn.textContent = 'Mark Mastered';
    mBtn.classList.add('btn-success');
    mBtn.classList.remove('btn-primary');
  }
}

function toggleFlip() {
  document.getElementById('active-flashcard').classList.toggle('flipped');
}

function nextCard() {
  if (currentCardIndex < filteredCards.length - 1) {
    currentCardIndex++;
    renderFlashcard();
  }
}

function prevCard() {
  if (currentCardIndex > 0) {
    currentCardIndex--;
    renderFlashcard();
  }
}

function shuffleCards() {
  filteredCards.sort(() => Math.random() - 0.5);
  currentCardIndex = 0;
  renderFlashcard();
}

function toggleMasteredCurrent() {
  const q = filteredCards[currentCardIndex];
  if (masteredIds.has(q.number)) {
    masteredIds.delete(q.number);
  } else {
    masteredIds.add(q.number);
  }
  saveMastered();
  renderFlashcard();
}

// Keyboard shortcuts for flashcard
window.addEventListener('keydown', (e) => {
  if (document.getElementById('view-flashcards').style.display !== 'none') {
    if (e.code === 'Space') {
      e.preventDefault();
      toggleFlip();
    } else if (e.code === 'ArrowRight') {
      nextCard();
    } else if (e.code === 'ArrowLeft') {
      prevCard();
    }
  }
});

// Browse & Top 50
function renderBrowse() {
  const query = document.getElementById('browse-search').value.toLowerCase();
  const grid = document.getElementById('browse-grid');
  grid.innerHTML = '';

  const filtered = QUESTIONS.filter(q => {
    const matchCat = activeCategory === 'All' || q.category === activeCategory;
    const matchQ = q.question.toLowerCase().includes(query) || q.answer.toLowerCase().includes(query);
    return matchCat && matchQ;
  });

  filtered.slice(0, 80).forEach(q => {
    grid.appendChild(createQCard(q));
  });
}

function filterBrowse() {
  renderBrowse();
}

function renderTop50() {
  const grid = document.getElementById('top50-grid');
  grid.innerHTML = '';
  // Top senior questions: reconciliation, fiber, lifecycle, hooks, context, state batching
  const topQuestions = QUESTIONS.filter(q => 
    q.question.toLowerCase().includes('fiber') ||
    q.question.toLowerCase().includes('reconcil') ||
    q.question.toLowerCase().includes('virtual dom') ||
    q.question.toLowerCase().includes('synthetic') ||
    q.question.toLowerCase().includes('batching') ||
    q.question.toLowerCase().includes('usememo') ||
    q.question.toLowerCase().includes('usecallback') ||
    q.question.toLowerCase().includes('suspense') ||
    q.question.toLowerCase().includes('server side') ||
    q.question.toLowerCase().includes('next.js')
  ).slice(0, 50);

  topQuestions.forEach(q => {
    grid.appendChild(createQCard(q, true));
  });
}

function createQCard(q, highlight = false) {
  const card = document.createElement('div');
  card.className = 'q-card';
  if (highlight) card.style.borderColor = 'rgba(168, 85, 247, 0.4)';

  const isMastered = masteredIds.has(q.number);

  card.innerHTML = `
    <div>
      <div class="q-card-head">
        <span class="q-num">#${q.number}</span>
        <span style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;">${q.category}</span>
      </div>
      <div class="q-title">${q.question}</div>
    </div>
    <div class="q-body">${formatMarkdown(q.answer)}</div>
    <div class="q-foot">
      <button class="btn" style="padding: 0.35rem 0.7rem; font-size: 0.75rem;" onclick="studyCardSpecific(${q.number})">Practice 🎴</button>
      <button class="btn ${isMastered ? 'btn-primary' : 'btn-success'}" style="padding: 0.35rem 0.7rem; font-size: 0.75rem;" onclick="toggleMasteredGrid(${q.number}, this)">
        ${isMastered ? '✓ Mastered' : 'Mark Mastered'}
      </button>
    </div>
  `;
  return card;
}

function studyCardSpecific(num) {
  const idx = filteredCards.findIndex(q => q.number === num);
  if (idx !== -1) {
    currentCardIndex = idx;
    switchView('flashcards');
    renderFlashcard();
  }
}

function toggleMasteredGrid(num, btn) {
  if (masteredIds.has(num)) {
    masteredIds.delete(num);
    btn.textContent = 'Mark Mastered';
    btn.className = 'btn btn-success';
  } else {
    masteredIds.add(num);
    btn.textContent = '✓ Mastered';
    btn.className = 'btn btn-primary';
  }
  saveMastered();
}

// 13 Projects
function renderProjects() {
  const list = document.getElementById('projects-list');
  list.innerHTML = '';
  CODING.projects.forEach((p, idx) => {
    const item = document.createElement('div');
    item.className = 'proj-item' + (idx === selectedProjectIndex ? ' active' : '');
    item.innerHTML = `
      <div class="proj-name">${idx + 1}. ${p.name}</div>
      <div class="proj-desc">${Object.keys(p.files).length} source files</div>
    `;
    item.onclick = () => {
      selectedProjectIndex = idx;
      renderProjects();
      displayProjectDetails();
    };
    list.appendChild(item);
  });
  displayProjectDetails();
}

function displayProjectDetails() {
  const p = CODING.projects[selectedProjectIndex];
  document.getElementById('pv-title').textContent = p.name;
  document.getElementById('pv-path').textContent = `coding-projects/${p.name}`;
  
  // File selector
  const sel = document.getElementById('pv-file-selector');
  sel.innerHTML = '';
  const fileKeys = Object.keys(p.files);
  if (!selectedProjectFile || !fileKeys.includes(selectedProjectFile)) {
    selectedProjectFile = fileKeys.find(f => f.includes('App.')) || fileKeys[0] || '';
  }

  fileKeys.forEach(f => {
    const btn = document.createElement('button');
    btn.className = 'file-tab' + (f === selectedProjectFile ? ' active' : '');
    btn.textContent = f.split('/').pop();
    btn.title = f;
    btn.onclick = () => {
      selectedProjectFile = f;
      displayProjectDetails();
    };
    sel.appendChild(btn);
  });

  document.getElementById('pv-code-header').textContent = `File: ${selectedProjectFile}`;
  document.getElementById('pv-code').textContent = p.files[selectedProjectFile] || '// Empty file';
  
  const rmBox = document.getElementById('pv-readme-box');
  if (p.readme) {
    rmBox.innerHTML = `<strong>Overview:</strong><br>` + formatMarkdown(p.readme.slice(0, 500));
    rmBox.style.display = 'block';
  } else {
    rmBox.style.display = 'none';
  }
}

// 8 Hooks
function renderHooks() {
  const list = document.getElementById('hooks-list');
  list.innerHTML = '';
  CODING.hooks.forEach((h, idx) => {
    const item = document.createElement('div');
    item.className = 'proj-item' + (idx === selectedHookIndex ? ' active' : '');
    item.innerHTML = `
      <div class="proj-name">${h.name}</div>
      <div class="proj-desc">Hook & Live Sandbox App</div>
    `;
    item.onclick = () => {
      selectedHookIndex = idx;
      renderHooks();
      displayHookDetails();
    };
    list.appendChild(item);
  });
  displayHookDetails();
}

function displayHookDetails() {
  const h = CODING.hooks[selectedHookIndex];
  document.getElementById('hv-title').textContent = h.name;
  const codeEl = document.getElementById('hv-code');
  if (currentHookView === 'hook') {
    codeEl.textContent = h.hook_code || '// No hook code';
  } else {
    codeEl.textContent = h.demo_code || '// No demo code';
  }
}

function showHookTab(tab) {
  currentHookView = tab;
  document.getElementById('hv-tab-hook').classList.toggle('active', tab === 'hook');
  document.getElementById('hv-tab-demo').classList.toggle('active', tab === 'demo');
  displayHookDetails();
}

// 4 Diagnostic Labs
function renderLabs() {
  const list = document.getElementById('labs-list');
  list.innerHTML = '';
  CODING.exercises.forEach((l, idx) => {
    const item = document.createElement('div');
    item.className = 'proj-item' + (idx === selectedLabIndex ? ' active' : '');
    item.innerHTML = `
      <div class="proj-name">${l.name}</div>
      <div class="proj-desc">Problem vs Verified Solution</div>
    `;
    item.onclick = () => {
      selectedLabIndex = idx;
      renderLabs();
      displayLabDetails();
    };
    list.appendChild(item);
  });
  displayLabDetails();
}

function displayLabDetails() {
  const l = CODING.exercises[selectedLabIndex];
  document.getElementById('lv-title').textContent = l.name;
  const codeEl = document.getElementById('lv-code');
  if (currentLabView === 'prob') {
    codeEl.textContent = l.problem || '// No problem file found';
  } else {
    codeEl.textContent = l.solution || '// No solution file found';
  }
}

function showLabTab(tab) {
  currentLabView = tab;
  document.getElementById('lv-tab-prob').classList.toggle('active', tab === 'prob');
  document.getElementById('lv-tab-sol').classList.toggle('active', tab === 'sol');
  displayLabDetails();
}

// Markdown formatter
function formatMarkdown(txt) {
  if (!txt) return '';
  return txt
    .replace(/```([a-z]*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.08); padding:0.1rem 0.3rem; border-radius:4px;">$1</code>')
    .replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>');
}

// Init
initCategories();
updateStats();
renderFlashcard();
</script>
</body>
</html>
'''

with open(r'e:\anti\react_interview_command_center.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Successfully generated unified react_interview_command_center.html!')
