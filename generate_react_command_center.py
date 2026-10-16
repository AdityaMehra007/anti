#!/usr/bin/env python3
"""
Generates the ReactJS Interview Command Center Web Application
Features: Flashcards, Instant Fuzzy Search, Mock Interview Simulator, Code Previews, and Progress Tracking.
"""

import json
from pathlib import Path

DATA_PATH = Path(r"e:\anti\data\react_interview_questions.json")
OUT_HTML = Path(r"e:\anti\react_interview_command_center.html")

def generate():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    minified_json = json.dumps(questions, separators=(',', ':'))

    total_count = len(questions)
    hooks_count = sum(1 for q in questions if q["category"] == "React Hooks")
    vdom_count = sum(1 for q in questions if q["category"] == "Virtual DOM, Fiber & Reconciliation")
    perf_count = sum(1 for q in questions if q["category"] == "Performance Optimization")
    redux_count = sum(1 for q in questions if q["category"] == "Redux & State Management")
    r18_count = sum(1 for q in questions if q["category"] == "React 18 / 19 & Server Components")
    code_count = sum(1 for q in questions if q["has_code"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>React.js Interview Command Center & Master Flashcards</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <!-- Marked.js for markdown rendering -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: rgba(19, 27, 46, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(28, 39, 66, 0.95);
      --react-blue: #61dafb;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.25);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --code-bg: #0d1117;
      --mastered: #22c55e;
      --review: #f59e0b;
      --badge-senior: #ef4444;
      --badge-mid: #3b82f6;
      --badge-junior: #10b981;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at 15% 15%, #131b2e 0%, #060911 85%);
      color: var(--text);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }}

    .title-group {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .react-logo {{
      width: 48px;
      height: 48px;
      animation: spin 20s linear infinite;
    }}

    @keyframes spin {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}

    .title-group h1 {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #fff 40%, #61dafb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .title-group p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-top: 2px;
    }}

    .stats-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}

    .stat-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 14px 16px;
      transition: all 0.2s;
    }}

    .stat-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(97, 218, 251, 0.3);
    }}

    .stat-card .label {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .stat-card .val {{
      font-size: 1.6rem;
      font-weight: 800;
      margin-top: 4px;
      color: var(--react-blue);
    }}

    /* View Switcher */
    .view-nav {{
      display: flex;
      gap: 8px;
      background: rgba(19, 27, 46, 0.6);
      padding: 6px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      margin-bottom: 24px;
      max-width: 600px;
    }}

    .nav-btn {{
      flex: 1;
      padding: 10px 16px;
      text-align: center;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s;
    }}

    .nav-btn.active {{
      background: #0284c7;
      color: #fff;
      box-shadow: 0 0 14px var(--accent-glow);
    }}

    /* Control Panel */
    .control-panel {{
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 18px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .search-input-wrap {{
      position: relative;
      width: 100%;
    }}

    .search-input {{
      width: 100%;
      background: rgba(11, 15, 25, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 10px;
      padding: 12px 16px 12px 42px;
      color: var(--text);
      font-size: 1rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--react-blue);
      box-shadow: 0 0 0 3px rgba(97, 218, 251, 0.25);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }}

    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .pill {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s;
    }}

    .pill:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }}

    .pill.active {{
      background: #0284c7;
      color: #fff;
      border-color: #0284c7;
      box-shadow: 0 0 10px rgba(2, 132, 199, 0.4);
    }}

    /* Flashcard View */
    .flashcard-container {{
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .flashcard {{
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 18px;
      padding: 32px;
      min-height: 380px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
      transition: all 0.2s;
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}

    .q-number {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--react-blue);
    }}

    .flashcard-q {{
      font-size: 1.45rem;
      font-weight: 700;
      line-height: 1.35;
      color: #fff;
      margin-bottom: 24px;
    }}

    .flashcard-answer-box {{
      background: rgba(13, 17, 23, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 24px;
      margin-top: 16px;
      display: none;
      line-height: 1.6;
      max-height: 520px;
      overflow-y: auto;
    }}

    .flashcard-answer-box.visible {{
      display: block;
    }}

    .flashcard-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 24px;
    }}

    .btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #fff;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .btn:hover {{
      background: rgba(255, 255, 255, 0.16);
    }}

    .btn-primary {{
      background: #0284c7;
      border-color: #0284c7;
    }}
    .btn-primary:hover {{
      background: #0369a1;
    }}

    .btn-success {{
      background: rgba(34, 197, 94, 0.2);
      border-color: #22c55e;
      color: #4ade80;
    }}
    .btn-success:hover {{
      background: rgba(34, 197, 94, 0.3);
    }}

    .btn-warning {{
      background: rgba(245, 158, 11, 0.2);
      border-color: #f59e0b;
      color: #fbbf24;
    }}
    .btn-warning:hover {{
      background: rgba(245, 158, 11, 0.3);
    }}

    /* Browse Grid View */
    .browse-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 16px;
    }}

    .q-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s;
      cursor: pointer;
    }}

    .q-card:hover {{
      background: var(--card-hover);
      border-color: rgba(97, 218, 251, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }}

    .q-card.mastered {{
      border-left: 4px solid var(--mastered);
    }}
    .q-card.need-review {{
      border-left: 4px solid var(--review);
    }}

    .q-card-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #f1f5f9;
      margin-bottom: 8px;
      line-height: 1.4;
    }}

    .q-preview {{
      font-size: 0.86rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 14px;
    }}

    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }}

    .badge {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .badge-diff-senior {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
    .badge-diff-mid {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .badge-diff-junior {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .badge-code {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-cat {{ background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }}

    /* Modal for Full Question */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: none;
      justify-content: center;
      align-items: center;
      padding: 24px;
      z-index: 999;
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-content {{
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 18px;
      width: 100%;
      max-width: 900px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 32px;
      position: relative;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }}

    .close-btn {{
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #fff;
      font-size: 1.2rem;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    /* Markdown Code Blocks */
    pre {{
      background: var(--code-bg);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 16px;
      overflow-x: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      margin: 14px 0;
    }}
    code {{
      font-family: 'JetBrains Mono', monospace;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.88em;
    }}
    pre code {{
      background: transparent;
      padding: 0;
    }}

    .pagination {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      margin: 32px 0 16px;
    }}

    @media (max-width: 768px) {{
      .browse-grid {{ grid-template-columns: 1fr; }}
      body {{ padding: 14px; }}
    }}
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="title-group">
      <svg class="react-logo" viewBox="-11.5 -10.23174 23 20.46348">
        <circle cx="0" cy="0" r="2.05" fill="#61dafb"/>
        <g stroke="#61dafb" stroke-width="1" fill="none">
          <ellipse rx="11" ry="4.2"/>
          <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
          <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
        </g>
      </svg>
      <div>
        <h1>React.js Interview Command Center</h1>
        <p>Synchronized from sudheerj/reactjs-interview-questions &bull; 444+ Master Questions & Answers</p>
      </div>
    </div>
    <div style="display: flex; gap: 8px;">
      <a href="data/react_interview_questions.csv" download class="btn">&#128196; Download CSV</a>
      <a href="data/react_interview_top_50.json" download class="btn">&#9733; Top 50 Senior JSON</a>
    </div>
  </header>

  <!-- Metrics Overview -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="label">Total Questions</div>
      <div class="val">{total_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">React Hooks</div>
      <div class="val" style="color: #38bdf8;">{hooks_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Virtual DOM & Fiber</div>
      <div class="val" style="color: #a855f7;">{vdom_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Performance & Memo</div>
      <div class="val" style="color: #f59e0b;">{perf_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Redux & State</div>
      <div class="val" style="color: #ec4899;">{redux_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">With Code Snippets</div>
      <div class="val" style="color: #34d399;">{code_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">My Mastered</div>
      <div class="val" id="stat-mastered" style="color: var(--mastered);">0</div>
    </div>
  </div>

  <!-- View Switcher -->
  <div class="view-nav">
    <div class="nav-btn active" id="tab-browse" onclick="switchView('browse')">📖 Browse & Search</div>
    <div class="nav-btn" id="tab-flashcards" onclick="switchView('flashcards')">🎴 Flashcard Mode</div>
    <div class="nav-btn" id="tab-top50" onclick="switchView('top50')">⚡ Top 50 Senior</div>
  </div>

  <!-- Controls Panel -->
  <div class="control-panel">
    <div class="search-input-wrap">
      <span class="search-icon">&#128269;</span>
      <input type="text" id="search-input" class="search-input" placeholder="Search React questions, hooks, fiber, lifecycle, performance, code...">
    </div>

    <div class="filter-pills">
      <div class="pill active" data-cat="all" onclick="setCategoryFilter('all', this)">All ({total_count})</div>
      <div class="pill" data-cat="React Hooks" onclick="setCategoryFilter('React Hooks', this)">⚓ Hooks ({hooks_count})</div>
      <div class="pill" data-cat="Virtual DOM, Fiber & Reconciliation" onclick="setCategoryFilter('Virtual DOM, Fiber & Reconciliation', this)">⚡ Fiber & VDOM ({vdom_count})</div>
      <div class="pill" data-cat="Performance Optimization" onclick="setCategoryFilter('Performance Optimization', this)">🚀 Performance ({perf_count})</div>
      <div class="pill" data-cat="Redux & State Management" onclick="setCategoryFilter('Redux & State Management', this)">📦 Redux ({redux_count})</div>
      <div class="pill" data-cat="React 18 / 19 & Server Components" onclick="setCategoryFilter('React 18 / 19 & Server Components', this)">🌐 React 18/19 ({r18_count})</div>
      <div class="pill" data-code="true" onclick="toggleCodeFilter(this)">💻 Code Only ({code_count})</div>
      <div class="pill" data-diff="Senior / Staff" onclick="toggleDiffFilter('Senior / Staff', this)">🔴 Senior Only</div>
      <div class="pill" data-status="review" onclick="toggleReviewOnly(this)">⚠️ Needs Review</div>
    </div>

    <div style="display: flex; justify-content: space-between; font-size: 0.88rem; color: var(--text-muted);">
      <span id="results-count">Showing {total_count} questions</span>
      <span id="page-nav-info">Page 1 of 1</span>
    </div>
  </div>

  <!-- Browse Grid View -->
  <div id="browse-view">
    <div class="browse-grid" id="questions-grid"></div>
    <div class="pagination">
      <button class="btn" id="prev-btn" onclick="changePage(-1)">Previous</button>
      <span id="page-indicator" style="color: var(--text-muted); font-weight: 600;">1 / 1</span>
      <button class="btn" id="next-btn" onclick="changePage(1)">Next</button>
    </div>
  </div>

  <!-- Flashcard View -->
  <div id="flashcard-view" style="display: none;">
    <div class="flashcard-container">
      <div class="flashcard">
        <div>
          <div class="card-top">
            <span class="q-number" id="fc-number">Q1 / {total_count}</span>
            <div id="fc-badges"></div>
          </div>
          <div class="flashcard-q" id="fc-title">What is React?</div>
          <button class="btn btn-primary" id="fc-toggle-btn" onclick="toggleFlashcardAnswer()">Reveal Answer 👁️</button>
          <div class="flashcard-answer-box" id="fc-answer"></div>
        </div>

        <div class="flashcard-controls">
          <div style="display: flex; gap: 8px;">
            <button class="btn" onclick="prevFlashcard()">← Previous</button>
            <button class="btn btn-primary" onclick="nextFlashcard()">Next →</button>
            <button class="btn" onclick="randomFlashcard()">🎲 Random</button>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-warning" onclick="markCardStatus('review')">⚠️ Review Later</button>
            <button class="btn btn-success" onclick="markCardStatus('mastered')">✅ Mastered</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>

<!-- Modal for full answer in Browse Mode -->
<div class="modal-overlay" id="answer-modal" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <button class="close-btn" onclick="closeModal()">&times;</button>
    <div id="modal-badges" style="margin-bottom: 12px;"></div>
    <h2 id="modal-title" style="color: #61dafb; margin-bottom: 16px; font-size: 1.4rem;"></h2>
    <div id="modal-body" style="line-height: 1.6; color: #e2e8f0;"></div>
    <div style="margin-top: 24px; display: flex; justify-content: flex-end; gap: 10px;">
      <button class="btn btn-warning" id="modal-review-btn">⚠️ Review Later</button>
      <button class="btn btn-success" id="modal-master-btn">✅ Mastered</button>
    </div>
  </div>
</div>

<script id="raw-questions" type="application/json">
{minified_json}
</script>

<script>
  const ALL_QUESTIONS = JSON.parse(document.getElementById('raw-questions').textContent);
  let activeCategory = 'all';
  let codeOnly = false;
  let activeDifficulty = null;
  let reviewOnly = false;
  let top50Mode = false;
  let searchQuery = '';
  let currentPage = 1;
  const PAGE_SIZE = 36;
  let currentFlashcardIdx = 0;
  let activeFlashcardList = [...ALL_QUESTIONS];

  // Local storage tracking
  function getProgress() {{
    try {{
      return JSON.parse(localStorage.getItem('react_interview_progress') || '{{}}');
    }} catch(e) {{
      return {{}};
    }}
  }}

  function setProgress(id, status) {{
    const p = getProgress();
    if (status === 'none') {{
      delete p[id];
    }} else {{
      p[id] = status;
    }}
    localStorage.setItem('react_interview_progress', JSON.stringify(p));
    updateMasteredCounter();
    renderBrowseGrid();
  }}

  function updateMasteredCounter() {{
    const p = getProgress();
    const count = Object.values(p).filter(v => v === 'mastered').length;
    document.getElementById('stat-mastered').innerText = count;
  }}

  function switchView(view) {{
    document.querySelectorAll('.view-nav .nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('browse-view').style.display = 'none';
    document.getElementById('flashcard-view').style.display = 'none';

    if (view === 'browse') {{
      top50Mode = false;
      document.getElementById('tab-browse').classList.add('active');
      document.getElementById('browse-view').style.display = 'block';
      applyFilters();
    }} else if (view === 'flashcards') {{
      document.getElementById('tab-flashcards').classList.add('active');
      document.getElementById('flashcard-view').style.display = 'block';
      activeFlashcardList = getFilteredQuestions();
      currentFlashcardIdx = 0;
      loadFlashcard(currentFlashcardIdx);
    }} else if (view === 'top50') {{
      top50Mode = true;
      document.getElementById('tab-top50').classList.add('active');
      document.getElementById('browse-view').style.display = 'block';
      applyFilters();
    }}
  }}

  function setCategoryFilter(cat, elem) {{
    activeCategory = cat;
    document.querySelectorAll('.filter-pills .pill[data-cat]').forEach(p => p.classList.remove('active'));
    elem.classList.add('active');
    currentPage = 1;
    applyFilters();
  }}

  function toggleCodeFilter(elem) {{
    codeOnly = !codeOnly;
    elem.classList.toggle('active', codeOnly);
    currentPage = 1;
    applyFilters();
  }}

  function toggleDiffFilter(diff, elem) {{
    if (activeDifficulty === diff) {{
      activeDifficulty = null;
      elem.classList.remove('active');
    }} else {{
      activeDifficulty = diff;
      elem.classList.add('active');
    }}
    currentPage = 1;
    applyFilters();
  }}

  function toggleReviewOnly(elem) {{
    reviewOnly = !reviewOnly;
    elem.classList.toggle('active', reviewOnly);
    currentPage = 1;
    applyFilters();
  }}

  document.getElementById('search-input').addEventListener('input', (e) => {{
    searchQuery = e.target.value.toLowerCase().trim();
    currentPage = 1;
    applyFilters();
  }});

  function getFilteredQuestions() {{
    const progress = getProgress();
    return ALL_QUESTIONS.filter(q => {{
      if (top50Mode) {{
        if (q.difficulty !== 'Senior / Staff' && q.difficulty !== 'Mid-Level') return false;
      }}
      if (activeCategory !== 'all' && q.category !== activeCategory) return false;
      if (codeOnly && !q.has_code) return false;
      if (activeDifficulty && q.difficulty !== activeDifficulty) return false;
      if (reviewOnly && progress[q.id] !== 'review') return false;

      if (searchQuery) {{
        const haystack = `${{q.id}} ${{q.title}} ${{q.category}} ${{q.answer_preview}}`.toLowerCase();
        if (!haystack.includes(searchQuery)) return false;
      }}
      return true;
    }});
  }}

  function renderBrowseGrid() {{
    const filtered = getFilteredQuestions();
    const container = document.getElementById('questions-grid');
    const total = filtered.length;
    const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

    document.getElementById('results-count').innerText = `Showing ${{total}} questions`;
    document.getElementById('page-nav-info').innerText = `Page ${{currentPage}} of ${{totalPages}}`;
    document.getElementById('page-indicator').innerText = `${{currentPage}} / ${{totalPages}}`;
    document.getElementById('prev-btn').disabled = currentPage <= 1;
    document.getElementById('next-btn').disabled = currentPage >= totalPages;

    const startIdx = (currentPage - 1) * PAGE_SIZE;
    const pageItems = filtered.slice(startIdx, startIdx + PAGE_SIZE);
    const progress = getProgress();

    container.innerHTML = pageItems.map(q => {{
      const st = progress[q.id] || 'none';
      let diffClass = 'badge-diff-junior';
      if (q.difficulty === 'Senior / Staff') diffClass = 'badge-diff-senior';
      else if (q.difficulty === 'Mid-Level') diffClass = 'badge-diff-mid';

      return `
        <div class="q-card ${{st === 'mastered' ? 'mastered' : st === 'review' ? 'need-review' : ''}}" onclick="openModal(${{q.id}})">
          <div>
            <div class="badges">
              <span class="badge badge-cat">#${{q.id}} &bull; ${{q.category}}</span>
              <span class="badge ${{diffClass}}">${{q.difficulty}}</span>
              ${{q.has_code ? '<span class="badge badge-code">💻 Code</span>' : ''}}
              ${{st === 'mastered' ? '<span class="badge" style="background:#22c55e;color:#fff;">Mastered</span>' : ''}}
              ${{st === 'review' ? '<span class="badge" style="background:#f59e0b;color:#fff;">Review</span>' : ''}}
            </div>
            <div class="q-card-title">${{escapeHtml(q.title)}}</div>
            <div class="q-preview">${{escapeHtml(q.answer_preview)}}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.06); padding-top:10px; font-size:0.8rem; color:var(--text-muted);">
            <span>Click to view full answer &rarr;</span>
          </div>
        </div>
      `;
    }}).join('');
  }}

  function changePage(delta) {{
    currentPage += delta;
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
    renderBrowseGrid();
  }}

  function applyFilters() {{
    renderBrowseGrid();
    activeFlashcardList = getFilteredQuestions();
  }}

  // Modal logic
  function openModal(id) {{
    const q = ALL_QUESTIONS.find(item => item.id === id);
    if (!q) return;

    let diffClass = 'badge-diff-junior';
    if (q.difficulty === 'Senior / Staff') diffClass = 'badge-diff-senior';
    else if (q.difficulty === 'Mid-Level') diffClass = 'badge-diff-mid';

    document.getElementById('modal-badges').innerHTML = `
      <span class="badge badge-cat">#${{q.id}} &bull; ${{q.category}}</span>
      <span class="badge ${{diffClass}}">${{q.difficulty}}</span>
      ${{q.has_code ? '<span class="badge badge-code">💻 Code Snippet Included</span>' : ''}}
    `;
    document.getElementById('modal-title').innerText = q.title;
    document.getElementById('modal-body').innerHTML = marked.parse(q.answer_markdown);

    const progress = getProgress();
    document.getElementById('modal-review-btn').onclick = () => {{ setProgress(q.id, 'review'); closeModal(); }};
    document.getElementById('modal-master-btn').onclick = () => {{ setProgress(q.id, 'mastered'); closeModal(); }};

    document.getElementById('answer-modal').classList.add('active');
  }}

  function closeModal(e) {{
    document.getElementById('answer-modal').classList.remove('active');
  }}

  // Flashcards Logic
  function loadFlashcard(idx) {{
    if (!activeFlashcardList.length) {{
      document.getElementById('fc-title').innerText = "No questions match your current filters.";
      document.getElementById('fc-answer').classList.remove('visible');
      return;
    }}
    const q = activeFlashcardList[idx];
    document.getElementById('fc-number').innerText = `Question ${{idx + 1}} of ${{activeFlashcardList.length}} (Ref #${{q.id}})`;
    document.getElementById('fc-title').innerText = q.title;

    let diffClass = 'badge-diff-junior';
    if (q.difficulty === 'Senior / Staff') diffClass = 'badge-diff-senior';
    else if (q.difficulty === 'Mid-Level') diffClass = 'badge-diff-mid';

    document.getElementById('fc-badges').innerHTML = `
      <span class="badge badge-cat">${{q.category}}</span>
      <span class="badge ${{diffClass}}">${{q.difficulty}}</span>
      ${{q.has_code ? '<span class="badge badge-code">💻 Code</span>' : ''}}
    `;

    document.getElementById('fc-answer').innerHTML = marked.parse(q.answer_markdown);
    document.getElementById('fc-answer').classList.remove('visible');
    document.getElementById('fc-toggle-btn').innerText = "Reveal Answer 👁️";
  }}

  function toggleFlashcardAnswer() {{
    const box = document.getElementById('fc-answer');
    const isVis = box.classList.toggle('visible');
    document.getElementById('fc-toggle-btn').innerText = isVis ? "Hide Answer 🙈" : "Reveal Answer 👁️";
  }}

  function nextFlashcard() {{
    if (!activeFlashcardList.length) return;
    currentFlashcardIdx = (currentFlashcardIdx + 1) % activeFlashcardList.length;
    loadFlashcard(currentFlashcardIdx);
  }}

  function prevFlashcard() {{
    if (!activeFlashcardList.length) return;
    currentFlashcardIdx = (currentFlashcardIdx - 1 + activeFlashcardList.length) % activeFlashcardList.length;
    loadFlashcard(currentFlashcardIdx);
  }}

  function randomFlashcard() {{
    if (!activeFlashcardList.length) return;
    currentFlashcardIdx = Math.floor(Math.random() * activeFlashcardList.length);
    loadFlashcard(currentFlashcardIdx);
  }}

  function markCardStatus(status) {{
    if (!activeFlashcardList.length) return;
    const q = activeFlashcardList[currentFlashcardIdx];
    setProgress(q.id, status);
    nextFlashcard();
  }}

  function escapeHtml(str) {{
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }}

  // Initial render
  updateMasteredCounter();
  renderBrowseGrid();
</script>

</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[✓] Successfully generated {OUT_HTML} ({len(html):,} bytes)!")

if __name__ == "__main__":
    generate()
