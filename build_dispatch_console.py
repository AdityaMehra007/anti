import json

with open('all_accenture_people_master.json', 'r', encoding='utf-8') as f:
    people = json.load(f)

def clean_name(n):
    parts = n.strip().split()
    if not parts:
        return "there"
    first = parts[0].capitalize()
    if len(first) == 1 and len(parts) > 1:
        first = parts[1].capitalize()
    return first

all_target_openings_block = """Top Matched Level 13 Back-Office Requisitions (0–1 Yrs Freshers):

1. Procurement Operations New Associate (Posted 2 Days Ago | Top Fit)
   • Job ID: AIOC-S01664213-1  (Parallel Slot: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay (P2P) Operations New Associate (Posted Yesterday | Fresh Opening)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

3. Sales Operations New Associate (Order Management & Contract Ops — 100% Non-Sales)
   • Job ID: AIOC-S01669615-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1

4. Regulatory Compliance New Associate (KYC & Sanctions Risk Operations)
   • Job ID: AIOC-S01667647-1  (Parallel Slot: AIOC-S01668628-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Regulatory-Compliance-New-Associate_AIOC-S01667647-1

5. Supply Chain Operations New Associate (Vendor Logistics & Shipping Tracking)
   • Job ID: AIOC-S01665657-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Supply-Chain-Operations-New-Associate_AIOC-S01665657-1

6. Trust & Safety New Associate (Policy & Content Operations — Non-Voice)
   • Job ID: AIOC-S01668350-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1

7. Customer Contact Comms New Associate (Digital Messaging & Chat Operations)
   • Job ID: AIOC-S01665940-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Customer-Contact-Comms-Associate-Messaging_AIOC-S01665940-1

8. HR Service Delivery New Associate (Employee Operations)
   • Job ID: AIOC-S01663367-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/HR-Service-Delivery-New-Associate_AIOC-S01663367-1"""

candidate_details = """• Candidate Legal Name: Aditya Mehra
• Email: adityamehra799@gmail.com
• Phone: +91 7003456624
• Degree: BBA in International Business (Dayananda Sagar University, Bengaluru)
• Notice Period: Immediate Joiner (0 Days Notice)
• Shift Flexibility: 100% flexible with 24/7 rotational & night shifts
• Location: Bengaluru (Local resident)"""

data_for_web = []

for i, p in enumerate(people, 1):
    name = p.get('name', 'Accenture Colleague')
    first = clean_name(name)
    title = p.get('title', 'Accenture Professional')
    url = p.get('url', '')
    t_lower = title.lower()

    if any(w in t_lower for w in ['recruiter', 'recruiting', 'talent acquisition', 'talent fulfilment']) or p.get('is_recruiter') == '1' or p.get('classification') == 'RECRUITER':
        category = "Recruiter / Talent Acquisition"
        msg = f"""Hi {first},

Hope you're having a great week!

I am reaching out as a 1st-degree connection regarding entry-level fresher hiring at Accenture Operations Bengaluru. I graduated with a BBA in International Business from Dayananda Sagar University and am available for immediate onboarding (0 Days Notice).

I am eager to be screened for any of these newly posted Level 13 non-sales operations requisitions:

{all_target_openings_block}

Candidate Summary:
{candidate_details}

Could you guide me on the screening process or connect me with the aligned recruiter for any of these requisitions? I have my resume ready for review. Thank you for your time and guidance!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['procurement', 'sourcing', 'supply chain', 'order to cash', 'p2p']):
        category = "Procurement & SCM Peer"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed your work as {title} at Accenture Bengaluru. I recently graduated with a BBA specializing in International Business from Dayananda Sagar University and am looking to start my career in corporate operations.

I saw these fresh Level 13 openings active on Workday:

{all_target_openings_block}

My details for the Workday MyReferrals portal:
{candidate_details}

Could you kindly submit an internal referral for me for any of these openings (Job ID AIOC-S01664213-1 or AIOC-S01670871-1 preferred)? Happy to share my updated resume right away. Would truly appreciate your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['manager', 'lead', 'director', 'head', 'vp']):
        category = "Leadership & Management"
        msg = f"""Dear {first},

I hope you are having a productive week.

I noticed your leadership as {title} at Accenture. I recently graduated with a BBA in International Business from Dayananda Sagar University, Bengaluru, and am seeking an entry-level operational role within Accenture Operations.

I have identified active Level 13 back-office requisitions aligned with my background:

{all_target_openings_block}

Candidate Summary:
{candidate_details}

I would be honored if you could refer me or direct my profile to the aligned hiring team for any of these openings. I have my resume ready for review. Thank you for your time and guidance!

Sincerely,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    elif any(w in t_lower for w in ['trust', 'safety', 'moderation']):
        category = "Trust & Safety / Quality"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working in Trust & Safety at Accenture Bengaluru. I am a BBA graduate from DSU and an immediate joiner interested in entry-level operations and Trust & Safety roles.

I have shortlisted these active Level 13 non-sales requisitions on Workday:

{all_target_openings_block}

My details for Workday MyReferrals:
{candidate_details}

Could you kindly submit an internal referral for me for Job ID AIOC-S01668350-1 or whichever requisition you prefer? I have my resume ready to share right away. Thank you so much for your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    else:
        category = "Operations / Engineering Peer"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working at Accenture Bengaluru. I am a fellow Bengaluru graduate (BBA in International Business from DSU) looking to start my career at Accenture in an entry-level back-office operations role.

Could you help me with a quick internal referral for any of these active Level 13 non-sales requisitions on Workday (whichever is easiest for you to refer):

{all_target_openings_block}

My details for Workday MyReferrals:
{candidate_details}

I have my resume ready to share immediately. Would truly appreciate your referral!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra799@gmail.com"""

    data_for_web.append({
        'id': i,
        'name': name,
        'title': title,
        'category': category,
        'url': url,
        'message': msg
    })

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Accenture 116 Outreach Console — Aditya Mehra</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
<style>
  body { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  .navbar { background: #131c2e; border-bottom: 1px solid #1e293b; }
  .card-contact { background: #131c2e; border: 1px solid #1e293b; border-radius: 12px; margin-bottom: 16px; transition: all 0.2s; }
  .card-contact:hover { border-color: #4f46e5; transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.6); }
  .card-contact.sent { border-color: #10b981 !important; background: #0e1e24 !important; }
  .badge-recruiter { background: #ec4899; color: #fff; font-size: 0.75rem; }
  .badge-procurement { background: #10b981; color: #fff; font-size: 0.75rem; }
  .badge-leadership { background: #f59e0b; color: #fff; font-size: 0.75rem; }
  .badge-peer { background: #3b82f6; color: #fff; font-size: 0.75rem; }
  .badge-trust { background: #8b5cf6; color: #fff; font-size: 0.75rem; }
  .badge-sent { background: #059669; color: #fff; font-size: 0.75rem; }
  .msg-box { background: #070a12; border: 1px solid #1e293b; border-radius: 8px; padding: 12px; font-size: 0.8rem; color: #cbd5e1; max-height: 200px; overflow-y: auto; white-space: pre-wrap; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; line-height: 1.45; }
  .btn-dispatch { background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color: #fff; border: none; font-weight: 500; }
  .btn-dispatch:hover { background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%); color: #fff; }
  .btn-copy { background: #1e293b; color: #e2e8f0; border: 1px solid #334155; font-weight: 500; }
  .btn-copy:hover { background: #334155; color: #fff; }
  .btn-copied { background: #10b981 !important; color: #fff !important; border-color: #059669 !important; }
  .stats-box { background: #131c2e; border: 1px solid #1e293b; border-radius: 10px; padding: 14px; text-align: center; }
  .req-pill { background: #1e293b; border: 1px solid #334155; border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; text-decoration: none; color: #94a3b8; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s; }
  .req-pill:hover { background: #334155; color: #fff; border-color: #6366f1; }
  .progress-bar-custom { height: 8px; border-radius: 4px; background: #1e293b; overflow: hidden; }
  .progress-fill { height: 100%; background: linear-gradient(90deg, #4f46e5, #10b981); transition: width 0.3s; }
</style>
</head>
<body>

<nav class="navbar navbar-dark sticky-top px-4 py-3">
  <div class="container-fluid d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center gap-3">
      <span class="navbar-brand mb-0 h1 fw-bold"><i class="bi bi-shield-check text-success me-2"></i>Accenture 116 High-Precision Outreach Console</span>
      <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50 px-2 py-1">100% Verified Job IDs (HTTP 200)</span>
    </div>
    <div class="d-flex align-items-center gap-3">
      <a href="file:///e:/anti/resumes_pdf/Aditya_Mehra_Resume_001_accenture_india.pdf" target="_blank" class="btn btn-outline-light btn-sm">
        <i class="bi bi-file-earmark-pdf me-1 text-danger"></i>Open Accenture ATS Resume PDF
      </a>
      <span class="text-secondary small">Candidate: <strong class="text-white">Aditya Mehra</strong> (+91 7003456624)</span>
    </div>
  </div>
</nav>

<div class="container-fluid py-4 px-4">

  <!-- Verified Workday Links Quick Bar -->
  <div class="card p-3 mb-4" style="background: #131c2e; border: 1px solid #1e293b;">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-2">
      <span class="text-secondary small fw-bold text-uppercase"><i class="bi bi-link-45deg text-primary me-1"></i>Quick Verify Requisition Links:</span>
      <div class="d-flex flex-wrap gap-2">
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1" target="_blank" class="req-pill">
          <span class="badge bg-success" style="font-size:0.65rem">NEW (2D)</span> AIOC-S01664213-1 (Procurement Ops)
        </a>
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1" target="_blank" class="req-pill">
          <span class="badge bg-success" style="font-size:0.65rem">NEW (1D)</span> AIOC-S01670871-1 (P2P Ops)
        </a>
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1" target="_blank" class="req-pill">
          <span class="badge bg-info" style="font-size:0.65rem">NON-SALES</span> AIOC-S01669615-1 (Sales Ops / Order)
        </a>
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Regulatory-Compliance-New-Associate_AIOC-S01667647-1" target="_blank" class="req-pill">
          <span class="badge bg-warning text-dark" style="font-size:0.65rem">KYC</span> AIOC-S01667647-1 (Compliance)
        </a>
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Supply-Chain-Operations-New-Associate_AIOC-S01665657-1" target="_blank" class="req-pill">
          <span class="badge bg-secondary" style="font-size:0.65rem">SCM</span> AIOC-S01665657-1 (Supply Chain)
        </a>
        <a href="https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1" target="_blank" class="req-pill">
          <span class="badge bg-purple text-white" style="background:#8b5cf6; font-size:0.65rem">POLICY</span> AIOC-S01668350-1 (Trust & Safety)
        </a>
      </div>
    </div>
  </div>

  <!-- Metric Badges & Progress -->
  <div class="row g-3 mb-3">
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-white mb-0" id="totalCount">116</div><div class="text-secondary small">Total Contacts</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold mb-0" style="color: #ec4899;">46</div><div class="text-secondary small">Recruiters & HR</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-success mb-0">3</div><div class="text-secondary small">Procurement Peers</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-warning mb-0">6</div><div class="text-secondary small">Managers & Leads</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-primary mb-0">61</div><div class="text-secondary small">Ops & Tech Peers</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-success mb-0" id="sentCount">0</div><div class="text-secondary small" id="sentLabel">Sent (0%)</div></div></div>
  </div>

  <!-- Progress Bar -->
  <div class="progress-bar-custom mb-4">
    <div class="progress-fill" id="progressBar" style="width: 0%;"></div>
  </div>

  <!-- Filter Controls -->
  <div class="card p-3 mb-4" style="background: #131c2e; border: 1px solid #1e293b;">
    <div class="row g-3">
      <div class="col-md-5">
        <input type="text" id="searchInput" class="form-control bg-dark text-white border-secondary" placeholder="Search name, job title, or keyword...">
      </div>
      <div class="col-md-4">
        <select id="categoryFilter" class="form-select bg-dark text-white border-secondary">
          <option value="ALL">All Categories (116)</option>
          <option value="Recruiter">Recruiters & Talent Acquisition (46)</option>
          <option value="Procurement">Procurement & SCM Peers (3)</option>
          <option value="Leadership">Leadership & Management (6)</option>
          <option value="Trust">Trust & Safety (3)</option>
          <option value="Peer">Operations & Tech Peers (58)</option>
        </select>
      </div>
      <div class="col-md-3 d-flex gap-2">
        <button class="btn btn-outline-secondary w-50" onclick="resetFilters()">Reset</button>
        <button class="btn btn-outline-danger w-50" onclick="clearProgress()">Clear Sent</button>
      </div>
    </div>
  </div>

  <div id="contactsContainer" class="row g-3"></div>
</div>

<script>
const peopleData = """ + json.dumps(data_for_web) + """;

let sentList = JSON.parse(localStorage.getItem('accenture_sent_list') || '[]');

function updateStats() {
  document.getElementById('sentCount').innerText = sentList.length;
  const pct = Math.round((sentList.length / peopleData.length) * 100);
  document.getElementById('sentLabel').innerText = `Sent (${pct}%)`;
  document.getElementById('progressBar').style.width = pct + '%';
}

function getBadge(cat) {
  if (cat.includes('Recruiter')) return '<span class="badge badge-recruiter">Recruiter / TA</span>';
  if (cat.includes('Procurement')) return '<span class="badge badge-procurement">Procurement SCM</span>';
  if (cat.includes('Leadership')) return '<span class="badge badge-leadership">Manager / Lead</span>';
  if (cat.includes('Trust')) return '<span class="badge badge-trust">Trust & Safety</span>';
  return '<span class="badge badge-peer">Operations / Tech</span>';
}

function renderContacts(list) {
  const container = document.getElementById('contactsContainer');
  container.innerHTML = '';
  if (list.length === 0) {
    container.innerHTML = '<div class="col-12 text-center py-5 text-secondary">No contacts matched your search.</div>';
    return;
  }
  list.forEach(p => {
    const isSent = sentList.includes(p.id);
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-6';
    col.innerHTML = `
      <div class="card card-contact p-3 h-100 d-flex flex-column justify-content-between ${isSent ? 'sent' : ''}" id="card-${p.id}">
        <div>
          <div class="d-flex justify-content-between align-items-start mb-2">
            <span class="text-secondary small">#${p.id}</span>
            <div class="d-flex gap-1 align-items-center">
              ${isSent ? '<span class="badge badge-sent"><i class="bi bi-check2"></i> SENT</span>' : ''}
              ${getBadge(p.category)}
            </div>
          </div>
          <h5 class="fw-bold mb-1 text-white">${p.name}</h5>
          <div class="text-secondary small mb-3 text-truncate" title="${p.title}">${p.title}</div>
          <div class="msg-box mb-3" id="msg-${p.id}">${p.message}</div>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-dispatch btn-sm flex-grow-1" onclick="dispatchDirect(${p.id})">
            <i class="bi bi-lightning-charge-fill me-1"></i>Copy & Open Chat
          </button>
          <button class="btn btn-copy btn-sm" id="btn-copy-${p.id}" onclick="copyMessage(${p.id})">
            <i class="bi bi-clipboard me-1"></i>Copy
          </button>
          <a href="${p.url}" target="_blank" class="btn btn-outline-primary btn-sm" onclick="markSent(${p.id})">
            <i class="bi bi-linkedin"></i>
          </a>
        </div>
      </div>
    `;
    container.appendChild(col);
  });
  updateStats();
}

function markSent(id) {
  if (!sentList.includes(id)) {
    sentList.push(id);
    localStorage.setItem('accenture_sent_list', JSON.stringify(sentList));
    const card = document.getElementById('card-' + id);
    if (card) card.classList.add('sent');
    updateStats();
  }
}

function copyMessage(id) {
  const p = peopleData.find(x => x.id === id);
  if (!p) return;
  navigator.clipboard.writeText(p.message).then(() => {
    markSent(id);
    const btn = document.getElementById('btn-copy-' + id);
    if (btn) {
      btn.classList.add('btn-copied');
      btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Copied!';
      setTimeout(() => {
        btn.classList.remove('btn-copied');
        btn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy';
      }, 2000);
    }
  });
}

function dispatchDirect(id) {
  const p = peopleData.find(x => x.id === id);
  if (!p) return;
  navigator.clipboard.writeText(p.message).then(() => {
    markSent(id);
    window.open(p.url, '_blank');
  });
}

function clearProgress() {
  if (confirm('Reset your sent status tracking?')) {
    sentList = [];
    localStorage.removeItem('accenture_sent_list');
    renderContacts(peopleData);
  }
}

function filterData() {
  const search = document.getElementById('searchInput').value.toLowerCase();
  const cat = document.getElementById('categoryFilter').value;
  const filtered = peopleData.filter(p => {
    const matchSearch = p.name.toLowerCase().includes(search) || p.title.toLowerCase().includes(search);
    const matchCat = cat === 'ALL' || p.category.includes(cat);
    return matchSearch && matchCat;
  });
  renderContacts(filtered);
}

document.getElementById('searchInput').addEventListener('input', filterData);
document.getElementById('categoryFilter').addEventListener('change', filterData);

function resetFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('categoryFilter').value = 'ALL';
  renderContacts(peopleData);
}

renderContacts(peopleData);
</script>
</body>
</html>
"""

with open('accenture_116_dispatch_console.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated super-enhanced accenture_116_dispatch_console.html successfully!")
