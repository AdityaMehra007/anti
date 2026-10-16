/**
 * BSU OS (Bengaluru Startup Universe) Interactive Client Application.
 * Handles state, REST API calls, Leaflet mapping, Super Search (Cmd+K),
 * Multi-Agent Copilot rendering, and War Room analytics.
 */

let state = {
  activeTab: 'overview',
  startups: [],
  clusters: [],
  jobs: [],
  events: [],
  watchlist: [],
  alerts: [],
  dailyBrief: null,
  mapInstance: null,
  mapMarkers: []
};

// Initialization on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initKeyboardShortcuts();
  loadInitialData();
});

// Tab Navigation
function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  const activePane = document.getElementById(`tab-${tabId}`);
  if (activePane) activePane.classList.add('active');

  const activeNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
  if (activeNav) activeNav.classList.add('active');

  // Trigger lazy tab loads
  if (tabId === 'map') {
    setTimeout(initOrRefreshMap, 200);
  } else if (tabId === 'startups' && state.startups.length === 0) {
    loadStartups();
  } else if (tabId === 'jobs' && state.jobs.length === 0) {
    loadJobs();
  } else if (tabId === 'events' && state.events.length === 0) {
    loadEvents();
  } else if (tabId === 'warrooms') {
    loadWarRoom('founder');
  } else if (tabId === 'watchlists') {
    loadWatchlist();
  }
}

// Initial Data Loading
async function loadInitialData() {
  try {
    const [commandRes, briefRes, alertsRes, startupsRes] = await Promise.all([
      fetch('/api/war-rooms/command').then(r => r.json()),
      fetch('/api/daily-brief').then(r => r.json()),
      fetch('/api/alerts').then(r => r.json()),
      fetch('/api/startups?limit=5').then(r => r.json()),
      loadWatchlist()
    ]);

    // Populate Command Center KPIs
    document.getElementById('header-bsi-val').textContent = commandRes.bengaluru_startup_index;
    document.getElementById('kpi-bsi').textContent = commandRes.bengaluru_startup_index;
    document.getElementById('side-total-startups').textContent = commandRes.total_tracked_startups;
    document.getElementById('side-total-jobs').textContent = commandRes.total_active_jobs;
    document.getElementById('side-unicorns').textContent = commandRes.total_unicorns;

    const formattedFunding = `$${(commandRes.total_tracked_capital_usd / 1e9).toFixed(1)}B+`;
    document.getElementById('kpi-funding').textContent = formattedFunding;
    document.getElementById('kpi-jobs').textContent = `${commandRes.total_active_jobs} Active`;

    // Render Daily Brief
    renderDailyBrief(briefRes);

    // Render Alerts
    renderAlerts(alertsRes);

    // Render Top Startups Table
    renderTopStartupsTable(startupsRes);

  } catch (err) {
    console.error('Failed to load initial BSU OS data:', err);
  }
}

// Daily Brief Renderer
function renderDailyBrief(brief) {
  const container = document.getElementById('daily-brief-content');
  if (!container || !brief) return;

  document.getElementById('daily-date').textContent = brief.date;

  container.innerHTML = `
    <div style="margin-bottom: 12px;">
      <span class="badge badge-accent">Theme: ${brief.theme}</span>
    </div>
    <div style="margin-bottom: 14px;">
      <div style="font-weight: 700; font-size: 11px; color: var(--accent-cyan); text-transform: uppercase;">⚡ 3 High-Impact Opportunities</div>
      <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: var(--text-secondary);">
        ${brief.opportunities.map(o => `<li>${o}</li>`).join('')}
      </ul>
    </div>
    <div style="margin-bottom: 14px;">
      <div style="font-weight: 700; font-size: 11px; color: var(--accent-violet); text-transform: uppercase;">📈 1 Emerging Trend</div>
      <p style="font-size: 12px; color: var(--text-primary); margin-top: 4px;"><strong>${brief.emerging_trend.title}</strong>: ${brief.emerging_trend.summary}</p>
    </div>
    <div>
      <div style="font-weight: 700; font-size: 11px; color: var(--accent-emerald); text-transform: uppercase;">🎯 Strategic Directives</div>
      <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: var(--text-secondary);">
        ${brief.recommended_actions.map(a => `<li>${a}</li>`).join('')}
      </ul>
    </div>
  `;
}

// Alerts Renderer
function renderAlerts(alerts) {
  const container = document.getElementById('alerts-list');
  if (!container) return;

  container.innerHTML = alerts.slice(0, 4).map(a => `
    <div style="padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span class="badge ${a.severity === 'HIGH' ? 'badge-danger' : 'badge-accent'}">${a.alert_type.toUpperCase()}</span>
        <span style="font-size: 10px; color: var(--text-muted); font-family: var(--font-mono);">${a.created_at.split(' ')[0]}</span>
      </div>
      <div style="font-weight: 600; font-size: 12px; color: var(--text-primary);">${a.headline}</div>
      <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">${a.summary}</div>
    </div>
  `).join('');
}

// Top Startups Table
function renderTopStartupsTable(startups) {
  const tbody = document.getElementById('top-startups-tbody');
  if (!tbody) return;

  tbody.innerHTML = startups.map(s => `
    <tr>
      <td>
        <div style="display: flex; align-items: center; gap: 10px;">
          <img src="${s.logo_url || 'https://via.placeholder.com/32'}" style="width: 28px; height: 28px; border-radius: 4px;" alt="${s.name}"/>
          <strong>${s.name}</strong>
        </div>
      </td>
      <td><span class="badge badge-accent">${s.sector}</span></td>
      <td><span style="font-size: 11px; color: var(--text-muted);">${formatClusterName(s.cluster_id)}</span></td>
      <td><span class="badge ${s.stage === 'Unicorn' ? 'badge-score badge-power' : 'badge-secondary'}">${s.stage}</span></td>
      <td><span class="badge badge-score badge-power">${s.power_score}</span></td>
      <td><span class="badge badge-score badge-career">${s.career_score}</span></td>
      <td style="font-family: var(--font-mono); font-size: 11px;">$${(s.total_funding_usd / 1e6).toFixed(1)}M</td>
      <td>
        <button class="btn btn-sm btn-secondary" onclick="openStartupModal(${s.id})">Deep Dive</button>
      </td>
    </tr>
  `).join('');
}

// Startups Directory Tab
async function loadStartups() {
  const grid = document.getElementById('startups-grid');
  grid.innerHTML = '<div class="loading-spinner">Loading startups...</div>';

  const sector = document.getElementById('filter-sector').value;
  const stage = document.getElementById('filter-stage').value;
  const cluster = document.getElementById('filter-cluster').value;

  let url = '/api/startups?limit=50';
  if (sector) url += `&sector=${encodeURIComponent(sector)}`;
  if (stage) url += `&stage=${encodeURIComponent(stage)}`;
  if (cluster) url += `&cluster_id=${encodeURIComponent(cluster)}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    state.startups = data;
    renderStartupsGrid(data);
  } catch (err) {
    grid.innerHTML = '<div class="loading-spinner">Failed to load startups.</div>';
  }
}

function applyStartupFilters() {
  loadStartups();
}

function renderStartupsGrid(startups) {
  const grid = document.getElementById('startups-grid');
  if (!grid) return;

  if (startups.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px;">No startups found matching your filters.</div>';
    return;
  }

  grid.innerHTML = startups.map(s => `
    <div class="startup-card" onclick="openStartupModal(${s.id})">
      <div>
        <div class="startup-card-top">
          <img src="${s.logo_url || 'https://via.placeholder.com/44'}" class="startup-logo" alt="${s.name}"/>
          <div>
            <div class="startup-name">${s.name}</div>
            <div class="startup-sector">${s.sector} • ${s.sub_sector}</div>
          </div>
        </div>
        <div class="startup-pitch">${s.elevator_pitch}</div>
        <div class="startup-scores-row">
          <span class="badge badge-score badge-power" title="Startup Power Score">⚡ Power: ${s.power_score}</span>
          <span class="badge badge-score badge-career" title="Career Growth Score">💼 Career: ${s.career_score}</span>
        </div>
      </div>
      <div class="startup-meta-row">
        <span>📍 ${formatClusterName(s.cluster_id)}</span>
        <span>${s.stage}</span>
        <span style="font-family: var(--font-mono);">${s.total_funding_usd > 0 ? '$' + (s.total_funding_usd/1e6).toFixed(0) + 'M' : 'Bootstrapped'}</span>
      </div>
    </div>
  `).join('');
}

// Startup Deep-Dive Modal
async function openStartupModal(startupId) {
  const modal = document.getElementById('startup-modal');
  const header = document.getElementById('startup-modal-header');
  const body = document.getElementById('startup-modal-body');

  modal.classList.add('open');
  header.innerHTML = '<h3>Loading Startup Profile...</h3>';
  body.innerHTML = '<div class="loading-spinner">Fetching ground-truth data...</div>';

  try {
    const s = await fetch(`/api/startups/${startupId}`).then(r => r.json());

    header.innerHTML = `
      <div style="display: flex; align-items: center; gap: 14px;">
        <img src="${s.logo_url}" style="width: 48px; height: 48px; border-radius: 8px;" alt="${s.name}"/>
        <div>
          <h2 style="font-size: 20px; font-weight: 800;">${s.name}</h2>
          <p style="font-size: 12px; color: var(--accent-cyan);">${s.sector} • ${s.stage} • Founded ${s.founded_year}</p>
        </div>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-sm btn-secondary" onclick="toggleWatchlist('startup', ${s.id})">⭐ Bookmark</button>
        <button class="btn-close" onclick="closeStartupModal()">✕</button>
      </div>
    `;

    body.innerHTML = `
      <div style="margin-bottom: 18px;">
        <p style="font-size: 13px; line-height: 1.6; color: var(--text-primary);">${s.full_description}</p>
      </div>

      <!-- Quantified Score Matrix -->
      <div class="grid-4" style="margin-bottom: 20px;">
        <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; text-align: center;">
          <div style="font-size: 10px; color: var(--text-muted);">POWER SCORE</div>
          <div style="font-size: 20px; font-weight: 800; color: #c084fc;">${s.power_score}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; text-align: center;">
          <div style="font-size: 10px; color: var(--text-muted);">CAREER SCORE</div>
          <div style="font-size: 20px; font-weight: 800; color: #34d399;">${s.career_score}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; text-align: center;">
          <div style="font-size: 10px; color: var(--text-muted);">HEAT INDEX</div>
          <div style="font-size: 20px; font-weight: 800; color: #f59e0b;">${s.momentum_score}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; text-align: center;">
          <div style="font-size: 10px; color: var(--text-muted);">RISK SCORE</div>
          <div style="font-size: 20px; font-weight: 800; color: #f43f5e;">${s.risk_score}</div>
        </div>
      </div>

      <!-- Founders -->
      <div style="margin-bottom: 20px;">
        <h4 style="font-size: 13px; font-weight: 700; color: var(--accent-cyan); margin-bottom: 8px;">FOUNDER PEDIGREE</h4>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${s.founders.map(f => `
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 6px;">
              <div style="font-weight: 700;">${f.name} — <span style="color: var(--text-secondary); font-size: 12px;">${f.role}</span></div>
              <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">${f.educational_background || ''} • ${f.prior_exits ? 'Prior Exit Verified' : 'First-time founder'}</div>
              <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">${f.bio}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Tech Stack -->
      <div style="margin-bottom: 20px;">
        <h4 style="font-size: 13px; font-weight: 700; color: var(--accent-cyan); margin-bottom: 8px;">VERIFIED TECH STACK</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
          ${s.tech_stack.map(t => `<span class="badge badge-accent">${t}</span>`).join('')}
        </div>
      </div>

      <!-- Open Jobs -->
      <div>
        <h4 style="font-size: 13px; font-weight: 700; color: var(--accent-cyan); margin-bottom: 8px;">ACTIVE OPEN ROLES (${s.open_jobs.length})</h4>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${s.open_jobs.map(j => `
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-weight: 700; font-size: 13px;">${j.title}</div>
                <div style="font-size: 11px; color: var(--text-muted);">${j.department} • Up to ${j.max_salary_lpa} LPA</div>
              </div>
              <button class="btn btn-sm btn-primary" onclick="alert('Applying to ${j.title} via BSU OS ATS connector...')">1-Click Apply</button>
            </div>
          `).join('')}
        </div>
      </div>
    `;

  } catch (err) {
    body.innerHTML = '<div class="loading-spinner">Failed to load startup details.</div>';
  }
}

function closeStartupModal() {
  document.getElementById('startup-modal').classList.remove('open');
}

function closeStartupModalOnBackdrop(e) {
  if (e.target.id === 'startup-modal') closeStartupModal();
}

// Leaflet Map Cluster Engine
async function initOrRefreshMap() {
  if (!state.mapInstance) {
    state.mapInstance = L.map('leaflet-map').setView([12.9716, 77.62], 12);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(state.mapInstance);
  }

  // Load Clusters data
  try {
    const clusters = await fetch('/api/clusters').then(r => r.json());
    state.clusters = clusters;

    // Clear old markers
    state.mapMarkers.forEach(m => state.mapInstance.removeLayer(m));
    state.mapMarkers = [];

    clusters.forEach(c => {
      const circle = L.circleMarker([c.lat, c.lng], {
        radius: 12 + (c.startup_count * 2),
        fillColor: '#06b6d4',
        color: '#8b5cf6',
        weight: 2,
        opacity: 0.9,
        fillOpacity: 0.5
      }).addTo(state.mapInstance);

      circle.bindTooltip(`<strong>${c.name}</strong><br>${c.startup_count} Startups | ${c.active_job_count} Jobs`, {
        direction: 'top',
        className: 'map-tooltip'
      });

      circle.on('click', () => {
        selectCluster(c);
      });

      state.mapMarkers.push(circle);
    });

    if (clusters.length > 0) {
      selectCluster(clusters[0]);
    }

  } catch (err) {
    console.error('Failed to load clusters map:', err);
  }
}

function selectCluster(cluster) {
  document.getElementById('cluster-detail-title').textContent = cluster.name;
  document.getElementById('cluster-detail-vibe').textContent = `"${cluster.vibe}"`;

  const container = document.getElementById('cluster-detail-content');
  container.innerHTML = `
    <div class="grid-2" style="margin-bottom: 14px;">
      <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px;">
        <div style="font-size: 10px; color: var(--text-muted);">FLAGSHIP STARTUPS</div>
        <div style="font-size: 18px; font-weight: 700;">${cluster.startup_count}</div>
      </div>
      <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px;">
        <div style="font-size: 10px; color: var(--text-muted);">ACTIVE ROLES</div>
        <div style="font-size: 18px; font-weight: 700; color: var(--accent-emerald);">${cluster.active_job_count}</div>
      </div>
    </div>
    <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 14px;">
      ${cluster.description}
    </div>
    <div style="margin-bottom: 14px;">
      <div style="font-size: 11px; font-weight: 700; color: var(--accent-cyan); margin-bottom: 6px;">CORE SECTORS</div>
      <div style="display: flex; flex-wrap: wrap; gap: 4px;">
        ${cluster.primary_sectors.map(s => `<span class="badge badge-accent">${s}</span>`).join('')}
      </div>
    </div>
    <div>
      <div style="font-size: 11px; font-weight: 700; color: var(--accent-violet); margin-bottom: 6px;">KEY COMPANIES</div>
      <div style="display: flex; flex-direction: column; gap: 6px;">
        ${cluster.key_startups.map(s => `
          <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 6px 10px; border-radius: 4px; cursor: pointer;" onclick="openStartupModal(${s.id})">
            <span>${s.name}</span>
            <span class="badge badge-score badge-power">${s.power_score}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

// Jobs Tab
async function loadJobs() {
  const container = document.getElementById('jobs-container');
  container.innerHTML = '<div class="loading-spinner">Loading high-growth tech roles...</div>';

  try {
    const jobs = await fetch('/api/jobs').then(r => r.json());
    state.jobs = jobs;

    container.innerHTML = jobs.map(j => `
      <div class="panel" style="margin-bottom: 12px; padding: 18px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <h4 style="font-size: 15px; font-weight: 700;">${j.title}</h4>
            <span class="badge badge-score badge-career">Career Score: ${j.career_score}</span>
          </div>
          <div style="font-size: 12px; color: var(--accent-cyan); margin-bottom: 6px;">
            <strong>${j.startup_name}</strong> • ${formatClusterName(j.location_cluster_id)} • ${j.remote_policy}
          </div>
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px;">
            ${j.skills_required.map(s => `<span class="badge badge-secondary" style="font-size: 10px;">${s}</span>`).join('')}
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 16px; font-weight: 800; font-family: var(--font-mono); color: var(--accent-emerald);">${j.max_salary_lpa} LPA</div>
          <div style="font-size: 10px; color: var(--text-muted); margin-bottom: 8px;">Top 10% Compensation</div>
          <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <button class="btn btn-sm btn-secondary" onclick="toggleWatchlist('job', ${j.id})">⭐ Save</button>
            <button class="btn btn-sm btn-primary" onclick="alert('Applying to ${j.title} at ${j.startup_name}!')">Apply Now</button>
          </div>
        </div>
      </div>
    `).join('');

  } catch (err) {
    container.innerHTML = '<div class="loading-spinner">Failed to load jobs.</div>';
  }
}

// 5 Domain War Rooms
async function loadWarRoom(roomName, btnElement) {
  if (btnElement) {
    document.querySelectorAll('.wr-tab').forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');
  }

  const container = document.getElementById('war-room-display');
  container.innerHTML = '<div class="loading-spinner">Loading War Room Telemetry...</div>';

  try {
    const data = await fetch(`/api/war-rooms/${roomName}`).then(r => r.json());

    if (roomName === 'founder') {
      container.innerHTML = `
        <div class="panel-body">
          <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 8px;">🛡️ FOUNDER WAR ROOM</h3>
          <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 18px;">Competitive radar, investor matching, and talent availability index.</p>
          
          <div class="grid-2" style="margin-bottom: 20px;">
            <div style="background: rgba(255,255,255,0.02); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
              <h4 style="font-size: 12px; color: var(--accent-cyan); font-weight: 700; margin-bottom: 10px;">ACTIVE INVESTOR MATCHES</h4>
              ${data.investor_matches.slice(0, 4).map(i => `
                <div style="margin-bottom: 8px; font-size: 12px;">
                  <strong>${i.name}</strong> (${i.firm_name})<br>
                  <span style="color: var(--text-muted); font-size: 11px;">${i.thesis.slice(0, 90)}...</span>
                </div>
              `).join('')}
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
              <h4 style="font-size: 12px; color: var(--accent-violet); font-weight: 700; margin-bottom: 10px;">TOP TALENT BIDDING WARS</h4>
              ${data.top_talent_bids.slice(0, 4).map(t => `
                <div style="margin-bottom: 8px; font-size: 12px; display: flex; justify-content: space-between;">
                  <span><strong>${t.startup_name}</strong>: ${t.title}</span>
                  <span style="color: var(--accent-emerald); font-family: var(--font-mono);">${t.max_salary_lpa} LPA</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="contract-box">
            <div class="contract-section-title">STRATEGIC DIRECTIVES FOR BENGALURU FOUNDERS</div>
            <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: var(--text-secondary);">
              ${data.strategic_directives.map(d => `<li>${d}</li>`).join('')}
            </ul>
          </div>
        </div>
      `;
    } else if (roomName === 'investor') {
      container.innerHTML = `
        <div class="panel-body">
          <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 8px;">💎 INVESTOR WAR ROOM</h3>
          <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 18px;">Breakout momentum radars and capital deployment velocity.</p>
          
          <h4 style="font-size: 12px; color: var(--accent-cyan); font-weight: 700; margin-bottom: 10px;">HIGH-MOMENTUM BREAKOUT TARGETS</h4>
          <div class="grid-2" style="margin-bottom: 20px;">
            ${data.high_momentum_breakouts.map(b => `
              <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); padding: 12px; border-radius: 6px; cursor: pointer;" onclick="openStartupModal(${b.id})">
                <div style="display: flex; justify-content: space-between;">
                  <strong>${b.name}</strong>
                  <span class="badge badge-score badge-power">Momentum: ${b.momentum_score}</span>
                </div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${b.sector} • ${b.stage} • ${formatClusterName(b.cluster_id)}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    } else {
      container.innerHTML = `
        <div class="panel-body">
          <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 8px;">${data.title.toUpperCase()}</h3>
          <pre style="font-family: var(--font-mono); font-size: 11px; color: var(--text-secondary); white-space: pre-wrap;">${JSON.stringify(data, null, 2)}</pre>
        </div>
      `;
    }

  } catch (err) {
    container.innerHTML = '<div class="loading-spinner">Failed to load War Room telemetry.</div>';
  }
}

// Events Tab
async function loadEvents() {
  const grid = document.getElementById('events-grid');
  grid.innerHTML = '<div class="loading-spinner">Loading ecosystem events...</div>';

  try {
    const events = await fetch('/api/events').then(r => r.json());
    state.events = events;

    grid.innerHTML = events.map(e => `
      <div class="panel" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <span class="badge badge-accent">${e.event_type}</span>
          <span style="font-size: 11px; font-family: var(--font-mono); color: var(--text-muted);">${e.date_time}</span>
        </div>
        <h4 style="font-size: 16px; font-weight: 700; margin-bottom: 4px;">${e.title}</h4>
        <div style="font-size: 12px; color: var(--accent-cyan); margin-bottom: 8px;">📍 ${e.venue_name} (${formatClusterName(e.location_cluster_id)})</div>
        <div style="font-size: 11px; color: var(--text-secondary); margin-bottom: 12px;">Organizer: <strong>${e.organizer}</strong></div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 4px;">
            ${e.tags.map(t => `<span class="badge badge-secondary" style="font-size: 10px;">${t}</span>`).join('')}
          </div>
          <a href="${e.registration_url || '#'}" target="_blank" class="btn btn-sm btn-primary">Register Free</a>
        </div>
      </div>
    `).join('');

  } catch (err) {
    grid.innerHTML = '<div class="loading-spinner">Failed to load events.</div>';
  }
}

// Watchlist
async function loadWatchlist() {
  try {
    const items = await fetch('/api/watchlists').then(r => r.json());
    state.watchlist = items;
    document.getElementById('watchlist-count').textContent = items.length;

    const container = document.getElementById('watchlist-container');
    if (!container) return;

    if (items.length === 0) {
      container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 40px;">No saved items yet. Bookmark startups and jobs to monitor them!</div>';
      return;
    }

    container.innerHTML = items.map(w => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid var(--border-subtle);">
        <div>
          <span class="badge badge-accent">${w.entity_type.toUpperCase()}</span>
          <strong style="margin-left: 8px;">${w.details ? (w.details.name || w.details.title) : 'Entity #' + w.entity_id}</strong>
        </div>
        <button class="btn btn-sm btn-secondary" onclick="toggleWatchlist('${w.entity_type}', ${w.entity_id})">Remove</button>
      </div>
    `).join('');

  } catch (err) {
    console.error('Failed to load watchlist:', err);
  }
}

async function toggleWatchlist(entityType, entityId) {
  const existing = state.watchlist.find(w => w.entity_type === entityType && w.entity_id === entityId);
  if (existing) {
    await fetch(`/api/watchlists/${entityType}/${entityId}`, { method: 'DELETE' });
  } else {
    await fetch('/api/watchlists', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ entity_type: entityType, entity_id: entityId })
    });
  }
  loadWatchlist();
}

// Super Search (Cmd+K / Ctrl+K)
function initKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearchModal();
    } else if (e.key === 'Escape') {
      closeSearchModal();
      closeCopilotModal();
      closeStartupModal();
    }
  });
}

function openSearchModal() {
  const modal = document.getElementById('search-modal');
  modal.classList.add('open');
  const input = document.getElementById('super-search-input');
  setTimeout(() => input.focus(), 50);
}

function closeSearchModal() {
  document.getElementById('search-modal').classList.remove('open');
}

function closeSearchModalOnBackdrop(e) {
  if (e.target.id === 'search-modal') closeSearchModal();
}

let searchDebounceTimer = null;
function handleSuperSearchInput(e) {
  clearTimeout(searchDebounceTimer);
  const q = e.target.value.trim();
  const resultsArea = document.getElementById('search-results-area');

  if (q.length < 2) {
    resultsArea.innerHTML = '<div class="search-placeholder-msg">Type at least 2 characters...</div>';
    return;
  }

  searchDebounceTimer = setTimeout(async () => {
    resultsArea.innerHTML = '<div class="loading-spinner">Searching ecosystem...</div>';
    try {
      const data = await fetch(`/api/search?q=${encodeURIComponent(q)}`).then(r => r.json());
      renderSearchResults(data);
    } catch (err) {
      resultsArea.innerHTML = '<div class="loading-spinner">Error searching ecosystem.</div>';
    }
  }, 200);
}

function renderSearchResults(data) {
  const resultsArea = document.getElementById('search-results-area');
  const allResults = [];

  (data.startups || []).forEach(s => allResults.push({ ...s, type: 'Startup' }));
  (data.founders || []).forEach(f => allResults.push({ ...f, type: 'Founder' }));
  (data.investors || []).forEach(i => allResults.push({ ...i, type: 'Investor' }));
  (data.jobs || []).forEach(j => allResults.push({ ...j, type: 'Job' }));
  (data.clusters || []).forEach(c => allResults.push({ ...c, type: 'Cluster' }));

  if (allResults.length === 0) {
    resultsArea.innerHTML = '<div class="search-placeholder-msg">No results matching query.</div>';
    return;
  }

  resultsArea.innerHTML = allResults.map(r => `
    <div class="search-result-item" onclick="handleSearchResultClick('${r.type}', ${r.id || 0}, '${r.slug || r.id || ''}')">
      <div>
        <span class="badge ${r.type === 'Startup' ? 'badge-score badge-power' : 'badge-accent'}" style="font-size: 10px;">${r.type}</span>
        <strong style="margin-left: 8px;">${r.name || r.title || r.firm_name}</strong>
        <span style="font-size: 11px; color: var(--text-muted); margin-left: 6px;">${r.sector || r.department || r.startup_name || ''}</span>
      </div>
      <span style="font-size: 11px; color: var(--accent-cyan);">Select →</span>
    </div>
  `).join('');
}

function handleSearchResultClick(type, id, slug) {
  closeSearchModal();
  if (type === 'Startup' && id) {
    openStartupModal(id);
  } else if (type === 'Job') {
    switchTab('jobs');
  } else if (type === 'Cluster') {
    switchTab('map');
  } else {
    switchTab('startups');
  }
}

// AI Copilot Modal
function openCopilotModal() {
  document.getElementById('copilot-modal').classList.add('open');
  setTimeout(() => document.getElementById('copilot-input').focus(), 50);
}

function closeCopilotModal() {
  document.getElementById('copilot-modal').classList.remove('open');
}

function closeCopilotModalOnBackdrop(e) {
  if (e.target.id === 'copilot-modal') closeCopilotModal();
}

function handleCopilotKey(e) {
  if (e.key === 'Enter') submitCopilotQuery();
}

function sendPresetQuery(preset) {
  document.getElementById('copilot-input').value = preset;
  submitCopilotQuery();
}

async function submitCopilotQuery() {
  const input = document.getElementById('copilot-input');
  const query = input.value.trim();
  if (!query) return;

  const chatArea = document.getElementById('copilot-chat-area');

  // Append user bubble
  chatArea.innerHTML += `
    <div class="copilot-msg user-msg">
      <p>${query}</p>
    </div>
  `;
  input.value = '';

  // Append loading bot bubble
  const botId = `bot-${Date.now()}`;
  chatArea.innerHTML += `
    <div class="copilot-msg bot-msg" id="${botId}">
      <span class="loading-spinner">Routing to specialized ecosystem agents...</span>
    </div>
  `;
  chatArea.scrollTop = chatArea.scrollHeight;

  try {
    const res = await fetch('/api/copilot/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query })
    });
    const c = await res.json();

    const targetBotMsg = document.getElementById(botId);
    targetBotMsg.innerHTML = `
      <div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
        💡 Verdict: ${c.verdict}
      </div>

      <div class="contract-box">
        <div class="contract-section-title">Verified Ground-Truth Evidence (Section 197)</div>
        <ul style="padding-left: 18px; margin: 4px 0 8px 0; font-size: 12px; color: var(--text-secondary);">
          ${c.evidence.map(e => `<li>${e}</li>`).join('')}
        </ul>

        <div class="contract-section-title">Strategic Value & Alignment</div>
        <p style="font-size: 12px; color: var(--text-secondary); margin: 4px 0 8px 0;">${c.why_it_matters}</p>

        <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
          <span style="font-size: 11px; font-weight: 700;">FIT SCORE:</span>
          <div style="flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 999px; overflow: hidden;">
            <div style="width: ${c.fit_score}%; height: 100%; background: var(--accent-cyan);"></div>
          </div>
          <span style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--accent-cyan);">${c.fit_score}/100</span>
        </div>

        <div class="contract-section-title">Recommended Action</div>
        <p style="font-size: 12px; color: var(--accent-emerald); font-weight: 600; margin: 4px 0 8px 0;">➜ ${c.recommended_action}</p>

        <div class="contract-section-title">Downside Risks & Friction</div>
        <ul style="padding-left: 18px; margin-top: 4px; font-size: 11px; color: var(--accent-rose);">
          ${c.risk_factors.map(r => `<li>${r}</li>`).join('')}
        </ul>
      </div>
    `;
    chatArea.scrollTop = chatArea.scrollHeight;

  } catch (err) {
    const targetBotMsg = document.getElementById(botId);
    if (targetBotMsg) targetBotMsg.innerHTML = 'Error retrieving copilot analysis.';
  }
}

// Recompute scores trigger
async function recomputeScores() {
  try {
    const res = await fetch('/api/recompute-scores', { method: 'POST' });
    const data = await res.json();
    alert(`Successfully recomputed quantified scores for ${data.recomputed_count} startups!`);
    loadInitialData();
  } catch (err) {
    alert('Failed to recompute scores.');
  }
}

// Helpers
function formatClusterName(clusterId) {
  const map = {
    'koramangala': 'Koramangala',
    'hsr_layout': 'HSR Layout',
    'indiranagar': 'Indiranagar',
    'outer_ring_road': 'Outer Ring Road (ORR)',
    'whitefield': 'Whitefield',
    'electronic_city': 'Electronic City',
    'cbd_central': 'Central Business District'
  };
  return map[clusterId] || clusterId;
}
