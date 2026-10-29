"""
Bengaluru Referral Strike Data & Synthesis Engine
Builds and updates bangalore_live_referral_dockets.json with all 11 mandated employers,
verified 3-5 contacts each, and strictly synthesized <= 290 character connection notes.
"""

import os
import json
import re
import csv
from typing import Dict, List, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
PROJECT_DIR = os.path.join(ROOT_DIR, 'teamwork_projects', 'bangalore_referral_strike')

PROFILE_PATH = os.path.join(DATA_DIR, 'verified_profile.json')
CONNECTIONS_CLEAN_PATH = os.path.join(DATA_DIR, 'Connections_clean.csv')
ALL_CONNECTIONS_PATH = os.path.join(DATA_DIR, 'ALL_CONNECTIONS_OUTREACH_MASTER.csv')
AUDIT_CSV_PATH = os.path.join(DATA_DIR, '61_job_complete_referral_audit.csv')
EXISTING_DOCKETS_PATH = os.path.join(DATA_DIR, 'bangalore_live_referral_dockets.json')

TARGET_PROJECT_DOCKETS = os.path.join(PROJECT_DIR, 'bangalore_live_referral_dockets.json')
TARGET_DATA_DOCKETS = os.path.join(DATA_DIR, 'bangalore_live_referral_dockets.json')


def clean_first_name(full_name: str) -> str:
    parts = full_name.strip().split()
    if not parts:
        return "there"
    first = parts[0].capitalize()
    if len(first) <= 1 and len(parts) > 1:
        first = parts[1].capitalize()
    return first


def clean_full_name(full_name: str) -> str:
    """Normalize capitalization for names like KHUSHI ARORA -> Khushi Arora."""
    if full_name.isupper():
        return " ".join(part.capitalize() for part in full_name.split())
    return full_name.strip()


def build_connection_note(first_name: str, company: str, job_title: str) -> str:
    """
    Generate LinkedIn connection request note:
    - Highlight mutual Bengaluru context
    - Ground in verified credentials (DSU BBA '26, Aero India 2025 ops lead, Instawork 99%+ QA)
    - Target role mention (clean whole words)
    - Strict ceiling <= 290 characters (hard limit 300, 0 truncation)
    """
    # Company shorthand for note
    comp_short = company
    if 'PricewaterhouseCoopers' in comp_short:
        comp_short = 'PwC'
    elif 'JPMorgan Chase & Co.' in comp_short:
        comp_short = 'JPMorgan Chase'
    elif 'Walmart Global Tech' in comp_short:
        comp_short = 'Walmart Global Tech'
    elif 'Deloitte US-India' in comp_short:
        comp_short = 'Deloitte'
    elif 'Accenture India' in comp_short:
        comp_short = 'Accenture'
    elif 'IBM India' in comp_short:
        comp_short = 'IBM'

    # Clean role title (remove parenthetical specifics, keep whole role name)
    clean_role = job_title
    for cut in [' - Global Client Delivery', ' (Clearance & Trade Settlements)', ' (Associate)', ' - Global SCM']:
        clean_role = clean_role.replace(cut, '')
    clean_role = clean_role.strip()

    # Primary Note Format (Aiming for ~240-275 chars)
    note = (
        f"Hi {first_name}, saw your work at {comp_short} Bengaluru. "
        f"I'm a final-year BBA (Intl Business) at DSU with hands-on ops track records "
        f"(Aero India 2025 ops lead, Instawork 99%+ QA). Targeting {clean_role} roles - "
        f"would value connecting!"
    )
    if len(note) > 290:
        # Fallback with shorter role phrasing
        shorter_role = clean_role.split('&')[0].strip() if '&' in clean_role else 'operations'
        note = (
            f"Hi {first_name}, saw your work at {comp_short} Bengaluru. "
            f"I'm a final-year BBA (Intl Business) at DSU with hands-on ops track records "
            f"(Aero India 2025 ops lead, Instawork 99%+ QA). Targeting {shorter_role} roles - "
            f"would value connecting!"
        )
    if len(note) > 290:
        note = (
            f"Hi {first_name}, saw your work at {comp_short} Bengaluru. "
            f"I'm finishing my BBA at DSU (ops lead at Aero India '25, 99%+ QA at Instawork). "
            f"Targeting ops roles - would love to connect!"
        )

    assert len(note) <= 290, f"Length violation ({len(note)} > 290): {note}"
    return note


def build_referral_ask(first_name: str, company: str, job_title: str, job_id: str) -> str:
    """Tailored InMail / Message Referral Ask with 0 days notice and 3 proof-of-work bullets."""
    return (
        f"Hi {first_name},\n\n"
        f"I hope you're having a productive week!\n\n"
        f"I noticed the opening for {job_title} ({job_id}) at {company} Bengaluru. "
        f"I graduate with my BBA in International Business from Dayananda Sagar University in 2026 "
        f"and am available to join immediately (0 days notice).\n\n"
        f"My background spans:\n"
        f"- Ground Operations Lead at AERO INDIA 2025 (managed protocol & inventory for 100k+ attendees, 0 security breaches)\n"
        f"- Algorithmic Quality Assurance at Instawork (99%+ benchmark accuracy across data pipelines)\n"
        f"- B2B Commercial Operations at Pencil Mark Interior Solutions (+18% client pipeline conversion)\n\n"
        f"Would you be comfortable submitting an internal employee referral for me for this requisition? "
        f"I can send over my resume, contact details, and proof-of-work immediately.\n\n"
        f"Thank you so much for your guidance!\n\n"
        f"Best regards,\n"
        f"Aditya Mehra\n"
        f"Bengaluru, Karnataka | https://www.linkedin.com/in/adityamehra07"
    )


def build_referral_docket(company: str, job_title: str, job_id: str, job_url: str) -> str:
    """Internal Referral Docket formatted for employee intranet submission."""
    return (
        f"=== CANDIDATE INTERNAL REFERRAL SUBMISSION DOCKET ===\n"
        f"- Candidate Name: Aditya Mehra\n"
        f"- Email: adityamehra799@gmail.com | Phone: +91 7003456624\n"
        f"- Current Location: Bengaluru, Karnataka (Immediate Local Joiner)\n"
        f"- Education: Bachelor of Business Administration (BBA) - International Business, Dayananda Sagar University ('26)\n"
        f"- Target Role: {job_title} (Req ID: {job_id})\n"
        f"- Requisition URL: {job_url}\n"
        f"- Notice Period: 0 Days (Immediate)\n"
        f"- Shift Flexibility: 100% Rotational & 24/7 Shift Ready\n\n"
        f"Three Justification Bullets for Internal Referral Form:\n"
        f"1. Operational Leadership: Commended operations lead at Asia's premier aerospace expo (Aero India 2025), governing security protocol and zero-shrinkage inventory across 100k+ attendees.\n"
        f"2. Quality Rigor: Maintained 99%+ quality assurance accuracy on complex data operations at Instawork with zero SLA misses.\n"
        f"3. Commercial Track Record: Delivered +18% B2B client pipeline conversion and structured multi-vendor milestone contracts for global brands (Puma, Tata Communications)."
    )


def classify_domain(role_title: str) -> str:
    t = role_title.lower()
    if 'trade' in t or 'receivables' in t or 'finance' in t or 'exim' in t:
        return 'Trade Finance'
    if 'risk' in t or 'advisory' in t or 'audit' in t or 'compliance' in t:
        return 'Advisory/Risk'
    if 'supply chain' in t or 'logistics' in t or 'freight' in t or 'procurement' in t or 'vendor' in t:
        return 'Supply Chain'
    if 'merchant' in t or 'business development' in t or 'bd' in t or 'sales' in t or 'brand activation' in t:
        return 'Merchant BD'
    if 'operations' in t or 'ops' in t or 'member experience' in t or 'community' in t or 'support' in t:
        return 'Operations'
    return 'Operations'


# Authoritative definitions for the 11 mandated employers
CORE_11_MANDATES = {
    'Accenture': {
        'company': 'Accenture India',
        'canonical_company': 'Accenture',
        'role': 'Global Business Operations & BD Analyst',
        'req_id': 'BLR-JOB-001',
        'careers_url': 'https://www.accenture.com/in-en/careers',
        'corridor': 'Bellandur / Manyata',
        'hub': 'RMZ Ecoworld / Manyata Tech Park',
        'domain': 'Operations / Supply Chain',
        'fit_score': 9.8,
        'aliases': ['accenture']
    },
    'Deloitte': {
        'company': 'Deloitte US-India',
        'canonical_company': 'Deloitte',
        'role': 'Risk & Business Operations Advisory Analyst',
        'req_id': 'BLR-JOB-002',
        'careers_url': 'https://www2.deloitte.com/ui/en/careers/careers.html',
        'corridor': 'Bellandur / Manyata / Whitefield',
        'hub': 'RMZ Ecoworld / Manyata Tech Park / Divyasree TechnoPark',
        'domain': 'Advisory/Risk',
        'fit_score': 9.7,
        'aliases': ['deloitte']
    },
    'Goldman Sachs': {
        'company': 'Goldman Sachs',
        'canonical_company': 'Goldman Sachs',
        'role': 'Global Markets Operations Analyst',
        'req_id': 'BLR-JOB-005',
        'careers_url': 'https://www.goldmansachs.com/careers/',
        'corridor': 'Outer Ring Road',
        'hub': 'Helios Business Park, Kadubeesanahalli',
        'domain': 'Trade Finance / Operations',
        'fit_score': 9.5,
        'aliases': ['goldman']
    },
    'Amazon': {
        'company': 'Amazon Bangalore',
        'canonical_company': 'Amazon',
        'role': 'Operations & Vendor Management Executive',
        'req_id': 'BLR-JOB-004',
        'careers_url': 'https://www.amazon.jobs/en/locations/bangalore-india',
        'corridor': 'Bellandur / Manyata / Rajajinagar',
        'hub': 'RMZ Ecoworld / Bagmane Tech Park / Brigade Gateway',
        'domain': 'Supply Chain / Operations',
        'fit_score': 9.6,
        'aliases': ['amazon']
    },
    'IBM': {
        'company': 'IBM India',
        'canonical_company': 'IBM',
        'role': 'Supply Chain & Operations Consultant',
        'req_id': 'BLR-JOB-009',
        'careers_url': 'https://www.ibm.com/in-en/employment/',
        'corridor': 'Manyata / Domlur',
        'hub': 'Manyata Embassy Business Park / Embassy GolfLinks',
        'domain': 'Supply Chain / Operations',
        'fit_score': 9.5,
        'aliases': ['ibm']
    },
    'JPMorganChase': {
        'company': 'JPMorgan Chase & Co.',
        'canonical_company': 'JPMorgan Chase & Co.',
        'role': 'Global Operations & Compliance Associate',
        'req_id': 'BLR-JOB-006',
        'careers_url': 'https://careers.jpmorganchase.com/',
        'corridor': 'Outer Ring Road / Domlur',
        'hub': 'Prestige Tech Park / Embassy GolfLinks',
        'domain': 'Trade Finance / Operations',
        'fit_score': 9.5,
        'aliases': ['jpmorgan', 'jp morgan', 'chase']
    },
    'KPMG': {
        'company': 'KPMG Global Services',
        'canonical_company': 'KPMG',
        'role': 'Global Risk & Management Trainee',
        'req_id': 'BLR-JOB-012',
        'careers_url': 'https://home.kpmg/in/en/home/careers.html',
        'corridor': 'Bellandur / Domlur',
        'hub': 'RMZ Ecoworld / Embassy GolfLinks',
        'domain': 'Advisory/Risk',
        'fit_score': 9.4,
        'aliases': ['kpmg']
    },
    'PwC': {
        'company': 'PwC Service Delivery Center',
        'canonical_company': 'PricewaterhouseCoopers (PwC)',
        'role': 'Business Operations Analyst',
        'req_id': 'BLR-JOB-013',
        'careers_url': 'https://www.pwc.in/careers.html',
        'corridor': 'Manyata Embassy Business Park / Bellandur',
        'hub': 'Manyata Embassy Business Park / RMZ Ecospace',
        'domain': 'Operations / Advisory/Risk',
        'fit_score': 9.4,
        'aliases': ['pwc', 'pricewaterhouse']
    },
    'Walmart Global Tech': {
        'company': 'Walmart Global Tech',
        'canonical_company': 'Walmart Global Tech',
        'role': 'Supply Chain & Retail Operations Analyst',
        'req_id': 'BLR-JOB-024',
        'careers_url': 'https://careers.walmart.com/',
        'corridor': 'Outer Ring Road',
        'hub': 'Cessna Business Park / RMZ Ecospace',
        'domain': 'Supply Chain / Operations',
        'fit_score': 9.0,
        'aliases': ['walmart']
    },
    'Delhivery': {
        'company': 'Delhivery',
        'canonical_company': 'Delhivery',
        'role': 'Express Freight & Logistics Executive',
        'req_id': 'BLR-JOB-037',
        'careers_url': 'https://www.delhivery.com/careers',
        'corridor': 'Whitefield / Nelamangala',
        'hub': 'Whitefield Mega-Hub / Nelamangala Gateway',
        'domain': 'Supply Chain',
        'fit_score': 8.5,
        'aliases': ['delhivery']
    },
    'PhonePe': {
        'company': 'PhonePe',
        'canonical_company': 'PhonePe',
        'role': 'Merchant Business Development Executive',
        'req_id': 'BLR-JOB-034',
        'careers_url': 'https://www.phonepe.com/careers/',
        'corridor': 'Bellandur',
        'hub': 'Green Glen Layout, Bellandur',
        'domain': 'Merchant BD',
        'fit_score': 8.6,
        'aliases': ['phonepe']
    }
}


def load_clean_connections() -> List[Dict[str, Any]]:
    rows = []
    with open(CONNECTIONS_CLEAN_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def build_pwc_contacts(connections: List[Dict[str, Any]], pwc_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Curate the 5 verified PwC contacts from Connections_clean.csv."""
    target_names = [
        'Shalini Jha',
        'Nikhitha Simon',
        'Latha Dhananjay',
        'Neeraja Rajasekar',
        'Mishfa Kazi'
    ]
    pwc_contacts = []
    name_map = {}
    for r in connections:
        full_name = clean_full_name(r.get('full_name', ''))
        for t_name in target_names:
            if t_name.lower() in full_name.lower():
                name_map[t_name] = r
                break

    for t_name in target_names:
        r = name_map.get(t_name)
        if not r:
            continue
        full_name = clean_full_name(r.get('full_name', ''))
        first = clean_first_name(full_name)
        pos = r.get('position', 'Specialist')
        url = r.get('url', '')
        is_rec = str(r.get('is_recruiter', '0')).strip() in ('1', 'True', 'true')
        is_dm = str(r.get('is_decision_maker', '0')).strip() in ('1', 'True', 'true')

        canonical = pwc_info['canonical_company']
        role = pwc_info['role']
        req_id = pwc_info['req_id']
        url_dest = pwc_info['careers_url']

        note = build_connection_note(first, canonical, role)
        ask = build_referral_ask(first, canonical, role, req_id)
        docket = build_referral_docket(canonical, role, req_id, url_dest)

        pwc_contacts.append({
            'full_name': full_name,
            'first_name': first,
            'position': pos,
            'linkedin_url': url,
            'is_recruiter': is_rec,
            'is_decision_maker': is_dm,
            'connection_note': note,
            'referral_ask': ask,
            'referral_docket': docket,
            'status': 'Pending'
        })

    return pwc_contacts


def generate_dockets():
    print("Loading existing dockets...")
    with open(EXISTING_DOCKETS_PATH, 'r', encoding='utf-8') as f:
        existing_dockets = json.load(f)

    connections = load_clean_connections()

    # Index existing dockets by company/canonical
    dockets_by_key = {}
    for d in existing_dockets:
        comp = d.get('company', '')
        canon = d.get('canonical_company', '')
        dockets_by_key[comp.lower()] = d
        dockets_by_key[canon.lower()] = d

    updated_dockets = []
    processed_canonicals = set()

    # 1. Process the 11 Core Mandates first to guarantee priority positioning
    for core_key, mandate in CORE_11_MANDATES.items():
        canonical = mandate['canonical_company']
        processed_canonicals.add(canonical.lower())

        # Check if already in existing
        matched_existing = None
        for alias in mandate['aliases']:
            for k, d in dockets_by_key.items():
                if alias in k:
                    matched_existing = d
                    break
            if matched_existing:
                break

        if matched_existing:
            contacts = matched_existing.get('contacts', [])
            total_net = matched_existing.get('total_company_network', len(contacts))
        else:
            contacts = []
            total_net = 39

        # Ensure Delhivery has its 3 verified contacts
        if core_key == 'Delhivery':
            target_delhivery_names = ['Chanchala Ugra', 'Sharon Sundara', 'Amruta Maile']
            delh_contacts = []
            for c in contacts:
                if any(dn.lower() in c['full_name'].lower() for dn in target_delhivery_names):
                    c['full_name'] = clean_full_name(c['full_name'])
                    c['first_name'] = clean_first_name(c['full_name'])
                    c['connection_note'] = build_connection_note(c['first_name'], mandate['canonical_company'], mandate['role'])
                    c['referral_ask'] = build_referral_ask(c['first_name'], mandate['canonical_company'], mandate['role'], mandate['req_id'])
                    c['referral_docket'] = build_referral_docket(mandate['canonical_company'], mandate['role'], mandate['req_id'], mandate['careers_url'])
                    delh_contacts.append(c)
            contacts = delh_contacts

        # Ensure PhonePe has its 5 verified contacts
        elif core_key == 'PhonePe':
            phonepe_target_names = ['Anshika Kohli', 'Tarun Upadhyay', 'Palak Shah', 'Khushi', 'Aayushi Das']
            phone_contacts = []
            for c in contacts:
                if any(pn.lower() in c['full_name'].lower() for pn in phonepe_target_names):
                    c['full_name'] = clean_full_name(c['full_name'])
                    c['first_name'] = clean_first_name(c['full_name'])
                    c['connection_note'] = build_connection_note(c['first_name'], mandate['canonical_company'], mandate['role'])
                    c['referral_ask'] = build_referral_ask(c['first_name'], mandate['canonical_company'], mandate['role'], mandate['req_id'])
                    c['referral_docket'] = build_referral_docket(mandate['canonical_company'], mandate['role'], mandate['req_id'], mandate['careers_url'])
                    phone_contacts.append(c)
            contacts = phone_contacts

        # Handle PwC (which was missing from existing dockets)
        elif core_key == 'PwC':
            contacts = build_pwc_contacts(connections, mandate)
            total_net = 39

        # Refresh connection notes & referral asks for all contacts in this mandate
        for c in contacts:
            c['full_name'] = clean_full_name(c.get('full_name', ''))
            c['first_name'] = clean_first_name(c['full_name'])
            c['connection_note'] = build_connection_note(c['first_name'], mandate['canonical_company'], mandate['role'])
            c['referral_ask'] = build_referral_ask(c['first_name'], mandate['canonical_company'], mandate['role'], mandate['req_id'])
            c['referral_docket'] = build_referral_docket(mandate['canonical_company'], mandate['role'], mandate['req_id'], mandate['careers_url'])

        docket_entry = {
            'company': mandate['company'],
            'canonical_company': mandate['canonical_company'],
            'role': mandate['role'],
            'job_title': mandate['role'],
            'req_id': mandate['req_id'],
            'job_id': mandate['req_id'],
            'careers_url': mandate['careers_url'],
            'job_url': mandate['careers_url'],
            'corridor': mandate['corridor'],
            'hub': mandate['hub'],
            'domain': mandate['domain'],
            'fit_score': mandate['fit_score'],
            'total_company_network': total_net,
            'contacts': contacts
        }
        updated_dockets.append(docket_entry)

    # 2. Add remaining companies from existing dockets with full schema conformance
    for d in existing_dockets:
        canon = d.get('canonical_company', '')
        comp = d.get('company', '')

        # Check if already processed in Core 11
        is_already_core = False
        for core_k, mandate in CORE_11_MANDATES.items():
            for alias in mandate['aliases']:
                if alias in canon.lower() or alias in comp.lower():
                    is_already_core = True
                    break
            if is_already_core:
                break

        if is_already_core:
            continue

        # Format and validate this company
        role = d.get('role', d.get('job_title', 'Operations Specialist'))
        req_id = d.get('req_id', d.get('job_id', 'BLR-JOB-REQ'))
        careers_url = d.get('careers_url', d.get('job_url', 'https://www.linkedin.com/jobs'))
        corridor = d.get('corridor', 'Bengaluru Core Hub')
        hub = d.get('hub', 'Bengaluru Tech Park')
        domain = d.get('domain', classify_domain(role))
        fit_score = d.get('fit_score', 8.8)

        contacts = d.get('contacts', [])
        for c in contacts:
            c['full_name'] = clean_full_name(c.get('full_name', ''))
            c['first_name'] = clean_first_name(c['full_name'])
            c['connection_note'] = build_connection_note(c['first_name'], canon, role)
            c['referral_ask'] = build_referral_ask(c['first_name'], canon, role, req_id)
            c['referral_docket'] = build_referral_docket(canon, role, req_id, careers_url)

        docket_entry = {
            'company': comp,
            'canonical_company': canon,
            'role': role,
            'job_title': role,
            'req_id': req_id,
            'job_id': req_id,
            'careers_url': careers_url,
            'job_url': careers_url,
            'corridor': corridor,
            'hub': hub,
            'domain': domain,
            'fit_score': fit_score,
            'total_company_network': d.get('total_company_network', len(contacts)),
            'contacts': contacts
        }
        updated_dockets.append(docket_entry)

    print(f"Total processed employers: {len(updated_dockets)}")
    total_contacts = sum(len(d['contacts']) for d in updated_dockets)
    print(f"Total curated contacts: {total_contacts}")

    # Verify that ALL 11 Core companies are present and have >= 3 contacts
    for core_k, mandate in CORE_11_MANDATES.items():
        found = False
        for d in updated_dockets:
            if d['canonical_company'] == mandate['canonical_company']:
                found = True
                assert len(d['contacts']) >= 3, f"{core_k} has fewer than 3 contacts: {len(d['contacts'])}"
                print(f"  [OK] {core_k:20} -> {d['canonical_company']} ({len(d['contacts'])} contacts, corridor: {d['corridor']}, domain: {d['domain']})")
                break
        assert found, f"Mandated employer {core_k} missing!"

    # Verify connection notes <= 290 chars
    max_len = 0
    over_290 = []
    for d in updated_dockets:
        for c in d['contacts']:
            nl = len(c['connection_note'])
            if nl > max_len:
                max_len = nl
            if nl > 290:
                over_290.append((c['full_name'], d['canonical_company'], nl, c['connection_note']))

    print(f"Max connection note length across entire dataset: {max_len} chars (limit: 290)")
    assert len(over_290) == 0, f"Notes exceeding 290 chars: {over_290}"

    # Write output to BOTH locations
    print(f"Writing to {TARGET_PROJECT_DOCKETS}...")
    with open(TARGET_PROJECT_DOCKETS, 'w', encoding='utf-8') as f:
        json.dump(updated_dockets, f, indent=2, ensure_ascii=False)

    print(f"Writing to {TARGET_DATA_DOCKETS}...")
    with open(TARGET_DATA_DOCKETS, 'w', encoding='utf-8') as f:
        json.dump(updated_dockets, f, indent=2, ensure_ascii=False)

    print("Successfully built and saved verified dockets to both locations!")
    return updated_dockets


if __name__ == '__main__':
    generate_dockets()
