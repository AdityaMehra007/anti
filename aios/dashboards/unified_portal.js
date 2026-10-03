/**
 * ANTIGRAVITY OMEGA — Unified Executive Subsystem Portal & Health Poller
 * Coordinates all 5 enterprise subsystems in a single-pane HUD.
 */

const SUBSYSTEMS = {
  aios: {
    id: 'aios',
    name: 'AIOS Core Gateway',
    port: 8090,
    healthUrl: 'http://localhost:8090/v1/health',
    status: 'checking'
  },
  tradenexus: {
    id: 'tradenexus',
    name: 'TradeNexus B2B Engine',
    port: 8000,
    healthUrl: 'http://localhost:8000/api/health',
    status: 'checking'
  },
  n8n: {
    id: 'n8n',
    name: 'n8n Automation Engine',
    port: 5678,
    healthUrl: 'http://localhost:5678/healthz',
    status: 'checking'
  },
  plane: {
    id: 'plane',
    name: 'Plane CE Workspaces',
    port: 80,
    healthUrl: 'http://localhost/api/instances/',
    status: 'checking'
  },
  career: {
    id: 'career',
    name: 'HR 1781 Contacts',
    port: null,
    healthUrl: null,
    status: 'ready'
  },
  strike300: {
    id: 'strike300',
    name: 'Target 300 Job Strike',
    port: null,
    healthUrl: null,
    status: 'ready'
  },
  workforce: {
    id: 'workforce',
    name: '7,656 Agents & 3,790 Skills',
    port: null,
    healthUrl: null,
    status: 'ready'
  },
  strike10000: {
    id: 'strike10000',
    name: '10,000 Global Strike',
    port: null,
    healthUrl: null,
    status: 'ready'
  }
};

let activeTab = 'aios';

function switchTab(tabId) {
  activeTab = tabId;
  const tabs = ['aios', 'tradenexus', 'plane', 'career', 'strike300', 'strike10000', 'workforce', 'n8n'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tabBtn-${t}`);
    const panel = document.getElementById(`tabPanel-${t}`);
    if (btn) {
      if (t === tabId) {
        btn.classList.add('nav-tab-active');
      } else {
        btn.classList.remove('nav-tab-active');
      }
    }
    if (panel) {
      panel.style.display = (t === tabId) ? 'block' : 'none';
    }
  });
}

async function checkSubsystemHealth(subKey) {
  const sub = SUBSYSTEMS[subKey];
  if (!sub.healthUrl) {
    updateSubsystemBadge(subKey, 'online', 'ONLINE (LOCAL)');
    return true;
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);

  try {
    const res = await fetch(sub.healthUrl, {
      method: 'GET',
      mode: 'cors',
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (res.ok || res.status === 200 || res.status === 401 || res.status === 403) {
      // 401/403 means server is running and actively rejecting unauthed, still alive
      updateSubsystemBadge(subKey, 'online', `PORT :${sub.port}`);
      sub.status = 'online';
      return true;
    } else {
      updateSubsystemBadge(subKey, 'offline', `ERROR :${res.status}`);
      sub.status = 'offline';
      return false;
    }
  } catch (err) {
    clearTimeout(timeoutId);
    updateSubsystemBadge(subKey, 'offline', 'OFFLINE');
    sub.status = 'offline';
    return false;
  }
}

function updateSubsystemBadge(subKey, status, text) {
  const badge = document.getElementById(`badge-${subKey}`);
  if (!badge) return;
  badge.className = status === 'online' ? 'status-pill status-online' : 'status-pill status-offline';
  badge.innerText = text;
}

async function pollSubsystems() {
  for (const key of Object.keys(SUBSYSTEMS)) {
    await checkSubsystemHealth(key);
  }
}

// Attach to window
window.SUBSYSTEMS = SUBSYSTEMS;
window.switchTab = switchTab;
window.checkSubsystemHealth = checkSubsystemHealth;
window.pollSubsystems = pollSubsystems;

document.addEventListener('DOMContentLoaded', () => {
  pollSubsystems();
  setInterval(pollSubsystems, 10000);
});
