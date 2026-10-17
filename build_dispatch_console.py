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

candidate_details = """• Candidate Legal Name: Aditya Mehra
• Email: adityamehra007@gmail.com
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

I am eager to be screened for these newly posted Level 13 non-sales operations requisitions:

1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1  (Backup: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

3. Sales Operations New Associate (Order Management — 100% Non-Sales)
   • Job ID: AIOC-S01669615-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1

Candidate Summary:
{candidate_details}

Could you guide me on the screening process or connect me with the aligned recruiter for these requisitions? I have my resume ready for review. Thank you for your time and guidance!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['procurement', 'sourcing', 'supply chain', 'order to cash', 'p2p']):
        category = "Procurement & SCM Peer"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed your work as {title} at Accenture Bengaluru. I recently graduated with a BBA specializing in International Business from Dayananda Sagar University and am looking to start my career in corporate procurement operations.

I saw these fresh Level 13 openings active on Workday:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1  (Backup: AIOC-S01664212-1)
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

My details for the Workday MyReferrals portal:
{candidate_details}

Could you kindly submit a quick referral for me for Job ID AIOC-S01664213-1? Happy to share my updated resume right away. Would truly appreciate your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['manager', 'lead', 'director', 'head', 'vp']):
        category = "Leadership & Management"
        msg = f"""Dear {first},

I hope you are having a productive week.

I noticed your leadership as {title} at Accenture. I recently graduated with a BBA in International Business from Dayananda Sagar University, Bengaluru, and am seeking an entry-level operational role within Accenture Operations.

I have identified active Level 13 back-office requisitions aligned with my background:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

Candidate Summary:
{candidate_details}

I would be honored if you could refer me or direct my profile to the aligned hiring team. I have my resume ready for review. Thank you for your time and guidance!

Sincerely,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    elif any(w in t_lower for w in ['trust', 'safety', 'moderation']):
        category = "Trust & Safety / Quality"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working in Trust & Safety at Accenture Bengaluru. I am a BBA graduate from DSU and an immediate joiner interested in entry-level Trust & Safety / Content Moderation roles.

Could you kindly submit an internal referral for:
• Trust & Safety New Associate (Non-Voice Screen Review)
• Job ID: AIOC-S01668350-1
• Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1

My details for Workday:
{candidate_details}

I have my resume ready to share right away. Thank you so much for your support!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

    else:
        category = "Operations / Engineering Peer"
        msg = f"""Hi {first},

Hope you're doing well!

I noticed you're working at Accenture Bengaluru. I am a fellow Bengaluru graduate (BBA in International Business from DSU) looking to start my career at Accenture in an entry-level back-office operations role.

Could you help me with a quick internal referral for:
1. Procurement Operations New Associate (Posted 2 Days Ago)
   • Job ID: AIOC-S01664213-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1

2. Procure to Pay Operations New Associate (Posted Yesterday)
   • Job ID: AIOC-S01670871-1
   • Link: https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1

My details for Workday MyReferrals:
{candidate_details}

I have my resume ready to share immediately. Would truly appreciate your referral!

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com"""

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
  body { background-color: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  .navbar { background: #1e293b; border-bottom: 1px solid #334155; }
  .card-contact { background: #1e293b; border: 1px solid #334155; border-radius: 12px; margin-bottom: 16px; transition: all 0.2s; }
  .card-contact:hover { border-color: #6366f1; transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
  .badge-recruiter { background: #ec4899; color: #fff; }
  .badge-procurement { background: #10b981; color: #fff; }
  .badge-leadership { background: #f59e0b; color: #fff; }
  .badge-peer { background: #3b82f6; color: #fff; }
  .badge-trust { background: #8b5cf6; color: #fff; }
  .msg-box { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #cbd5e1; max-height: 180px; overflow-y: auto; white-space: pre-wrap; font-family: monospace; }
  .btn-copy { background: #6366f1; color: #fff; border: none; }
  .btn-copy:hover { background: #4f46e5; color: #fff; }
  .stats-box { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 14px; text-align: center; }
</style>
</head>
<body>
<nav class="navbar navbar-dark sticky-top px-4 py-3">
  <div class="container-fluid d-flex justify-content-between align-items-center">
    <span class="navbar-brand mb-0 h1 fw-bold"><i class="bi bi-send-fill text-primary me-2"></i>Accenture 116 Outreach Command Center</span>
    <span class="text-secondary small">Candidate: <strong class="text-white">Aditya Mehra</strong> | BBA International Business</span>
  </div>
</nav>

<div class="container-fluid py-4 px-4">
  <div class="row g-3 mb-4">
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-white mb-0" id="totalCount">116</div><div class="text-secondary small">Total Contacts</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-pink mb-0" style="color: #ec4899;">46</div><div class="text-secondary small">Recruiters & HR</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-success mb-0">3</div><div class="text-secondary small">Procurement Peers</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-warning mb-0">6</div><div class="text-secondary small">Managers & Leads</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-primary mb-0">61</div><div class="text-secondary small">Ops & Tech Peers</div></div></div>
    <div class="col-md-2"><div class="stats-box"><div class="h3 fw-bold text-info mb-0" id="sentCount">0</div><div class="text-secondary small">Sent / Progress</div></div></div>
  </div>

  <div class="card p-3 mb-4" style="background: #1e293b; border: 1px solid #334155;">
    <div class="row g-3">
      <div class="col-md-5">
        <input type="text" id="searchInput" class="form-control bg-dark text-white border-secondary" placeholder="Search name, title, or keyword (e.g., recruiter, procurement, manager)...">
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
        <button class="btn btn-outline-secondary w-100" onclick="resetFilters()">Reset</button>
      </div>
    </div>
  </div>

  <div id="contactsContainer" class="row g-3"></div>
</div>

<script>
const peopleData = """ + json.dumps(data_for_web) + """;

function getBadge(cat) {
  if (cat.includes('Recruiter')) return '<span class="badge badge-recruiter">Recruiter</span>';
  if (cat.includes('Procurement')) return '<span class="badge badge-procurement">Procurement SCM</span>';
  if (cat.includes('Leadership')) return '<span class="badge badge-leadership">Manager</span>';
  if (cat.includes('Trust')) return '<span class="badge badge-trust">Trust & Safety</span>';
  return '<span class="badge badge-peer">Operations</span>';
}

function renderContacts(list) {
  const container = document.getElementById('contactsContainer');
  container.innerHTML = '';
  if (list.length === 0) {
    container.innerHTML = '<div class="col-12 text-center py-5 text-secondary">No contacts matched your search.</div>';
    return;
  }
  list.forEach(p => {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4';
    col.innerHTML = `
      <div class="card card-contact p-3 h-100 d-flex flex-column justify-content-between">
        <div>
          <div class="d-flex justify-content-between align-items-start mb-2">
            <span class="text-secondary small">#${p.id}</span>
            ${getBadge(p.category)}
          </div>
          <h5 class="fw-bold mb-1 text-white">${p.name}</h5>
          <div class="text-secondary small mb-3 text-truncate" title="${p.title}">${p.title}</div>
          <div class="msg-box mb-3" id="msg-${p.id}">${p.message}</div>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-copy btn-sm flex-grow-1" onclick="copyMessage(${p.id})">
            <i class="bi bi-clipboard me-1"></i>Copy Message
          </button>
          <a href="${p.url}" target="_blank" class="btn btn-outline-primary btn-sm">
            <i class="bi bi-linkedin me-1"></i>Open Chat
          </a>
        </div>
      </div>
    `;
    container.appendChild(col);
  });
}

function copyMessage(id) {
  const p = peopleData.find(x => x.id === id);
  if (!p) return;
  navigator.clipboard.writeText(p.message).then(() => {
    alert('Copied personalized message for ' + p.name + ' to clipboard!');
  });
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

print("Generated accenture_116_dispatch_console.html successfully!")
