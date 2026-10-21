import json
import os
import sys
import subprocess
import argparse

STATE_FILE = os.path.join(os.path.dirname(__file__), '.scratch', 'hr_dispatch_state.json')
DATA_FILE = os.path.join(os.path.dirname(__file__), '.scratch', 'all_hr_outreach_database.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        sys.exit(1)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def copy_to_clipboard(text):
    try:
        # Use PowerShell Set-Clipboard on Windows
        proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard -Value $Input'], stdin=subprocess.PIPE)
        proc.communicate(input=text.encode('utf-8'))
        return True
    except Exception as e:
        return False

def show_contact_card(contact, idx, total, state):
    is_sent = state.get(contact['name'], False)
    status_str = "[DISPATCHED / SENT]" if is_sent else "[PENDING]"
    print("=" * 80)
    print(f" GATEKEEPER {idx}/{total} {status_str} | {contact['company'].upper()}")
    print("=" * 80)
    print(f" Contact Name : {contact['name']}")
    print(f" Position     : {contact['position']}")
    print(f" Target Role  : {contact['job_title']}")
    print(f" Job Req ID   : {contact['job_id']}")
    print(f" Direct Job   : {contact['job_link']}")
    print(f" LinkedIn     : {contact['linkedin_url']}")
    if contact.get('email'):
        print(f" Email        : {contact['email']}")
    print(f" Career Portal: {contact['portal']}")
    print("-" * 80)
    print(" PRE-COMPOSED MESSAGE:")
    print("-" * 80)
    print(contact['message'])
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="HR & Recruiter Master Outreach Dispatcher")
    parser.add_argument('--next', action='store_true', help="Show the next pending contact and copy message to clipboard")
    parser.add_argument('--company', type=str, help="Filter contacts by company (e.g. deloitte, ibm, amazon, kpmg)")
    parser.add_argument('--stats', action='store_true', help="Show overall dispatch metrics and progress")
    parser.add_argument('--mark-sent', type=str, help="Mark a contact as sent by name")
    parser.add_argument('--open', action='store_true', help="Open the interactive HTML console in browser")
    parser.add_argument('--list', action='store_true', help="List all companies and verified gatekeeper counts")

    args = parser.parse_args()
    data = load_data()
    state = load_state()

    if args.open:
        console_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'MASTER_HR_DISPATCH_CONSOLE.html'))
        print(f"Opening {console_path} in default browser...")
        os.system(f'start "" "{console_path}"')
        return

    if args.stats:
        total = len(data)
        sent = sum(1 for d in data if state.get(d['name']))
        pending = total - sent
        pct = (sent / total) * 100 if total else 0
        print("\n" + "=" * 50)
        print(" OMEGA HR DISPATCH PIPELINE METRICS")
        print("=" * 50)
        print(f" Total Verified Gatekeepers : {total}")
        print(f" Messages Dispatched (Sent) : {sent}")
        print(f" Remaining Pending          : {pending}")
        print(f" Completion Percentage      : {pct:.1f}%")
        print("=" * 50 + "\n")
        return

    if args.list:
        by_comp = {}
        for d in data:
            by_comp.setdefault(d['company'], []).append(d)
        print("\n" + "=" * 60)
        print(f" {'COMPANY':<30} | {'RECRUITERS':<10} | {'SENT':<8}")
        print("=" * 60)
        for comp, members in sorted(by_comp.items(), key=lambda x: len(x[1]), reverse=True):
            sent_in_comp = sum(1 for m in members if state.get(m['name']))
            print(f" {comp:<30} | {len(members):<10} | {sent_in_comp:<8}")
        print("=" * 60 + "\n")
        return

    if args.mark_sent:
        target_name = args.mark_sent.strip().lower()
        matched = False
        for d in data:
            if target_name in d['name'].lower():
                state[d['name']] = True
                save_state(state)
                print(f"[OK] Marked '{d['name']}' at {d['company']} as SENT.")
                matched = True
        if not matched:
            print(f"[WARN] No contact matching '{args.mark_sent}' found.")
        return

    if args.company:
        comp_query = args.company.strip().lower()
        filtered = [d for d in data if comp_query in d['company'].lower()]
        if not filtered:
            print(f"No contacts found for company matching '{args.company}'.")
            return
        print(f"\nFound {len(filtered)} contacts for '{args.company}':\n")
        for i, c in enumerate(filtered, 1):
            show_contact_card(c, i, len(filtered), state)
        return

    # Default or --next
    pending_list = [d for d in data if not state.get(d['name'])]
    if not pending_list:
        print("\n[CONGRATULATIONS] All 115 HR contacts have been dispatched!\n")
        return

    next_contact = pending_list[0]
    total = len(data)
    idx = data.index(next_contact) + 1

    show_contact_card(next_contact, idx, total, state)

    copied = copy_to_clipboard(next_contact['message'])
    if copied:
        print("\n[COPIED] Pre-composed message copied to your clipboard!")
    print(f"\nActions:")
    print(f" - Open LinkedIn: {next_contact['linkedin_url']}")
    print(f" - Mark sent: python hr_dispatcher.py --mark-sent \"{next_contact['name']}\"")
    print(f" - Next:      python hr_dispatcher.py --next\n")

if __name__ == '__main__':
    main()
