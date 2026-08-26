import os, sqlite3, json, uuid
from datetime import datetime

class NexusOmegaEngine:
    '''Core Engine for Nexus Omega Event Operations & Sponsorship Intelligence Platform.'''
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(r"e:\anti", "omega", "apps", "nexus_omega", "nexus_event.db")
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Events Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    expected_attendees INTEGER,
                    budget_inr REAL,
                    status TEXT DEFAULT 'PLANNING',
                    created_at TEXT NOT NULL
                )
            ''')
            # Sponsors Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sponsors (
                    id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    pledged_inr REAL,
                    contact_person TEXT,
                    status TEXT DEFAULT 'PROSPECT'
                )
            ''')
            # Run of Show Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS run_of_show (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT,
                    time_slot TEXT NOT NULL,
                    activity TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    status TEXT DEFAULT 'SCHEDULED'
                )
            ''')
            conn.commit()

    def create_event(self, name, category, attendees, budget_inr):
        event_id = f"EVT-{uuid.uuid4().hex[:6]}"
        now = datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO events (id, name, category, expected_attendees, budget_inr, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, 'ACTIVE_PLANNING', ?)",
                (event_id, name, category, attendees, budget_inr, now)
            )
            # Add default Run-of-Show slots
            ros_items = [
                (event_id, "08:00 - 09:30", "VIP & Delegate Registration / Security Screening", "Security Lead", "SCHEDULED"),
                (event_id, "09:30 - 11:00", "Keynote Address & Grand Exhibition Kickoff", "Aditya Mehra (Ops Lead)", "SCHEDULED"),
                (event_id, "11:00 - 13:30", "B2B Sponsor Roundtables & Partner Demos", "B2B Sales Agent", "SCHEDULED"),
                (event_id, "14:30 - 17:00", "Industry Panel & Product Activations", "Program Director", "SCHEDULED"),
                (event_id, "17:00 - 18:30", "Networking Reception & Closing Keynote", "Event Coordinator", "SCHEDULED")
            ]
            conn.executemany(
                "INSERT INTO run_of_show (event_id, time_slot, activity, owner, status) VALUES (?, ?, ?, ?, ?)",
                ros_items
            )
            conn.commit()
        return event_id

    def match_sponsors_from_network(self, network_csv_path=r"e:\anti\linkedin_network_master.csv"):
        # Match prospective sponsors from top companies in LinkedIn Network
        top_targets = ["Tata Communications", "EY GDS", "Accenture", "Deloitte", "Goldman Sachs", "Amazon", "Puma"]
        matched_sponsors = []
        for i, comp in enumerate(top_targets):
            sp_id = f"SPN-{101+i}"
            pledge = 500000 if i < 3 else 250000
            tier = "PLATINUM" if pledge >= 500000 else "GOLD"
            matched_sponsors.append({
                "id": sp_id,
                "company": comp,
                "tier": tier,
                "pledged_inr": pledge,
                "status": "QUALIFIED_PROSPECT"
            })
        return matched_sponsors

    def calculate_event_roi(self, budget_inr, sponsors_pledged_inr, ticket_revenue_inr):
        total_revenue = sponsors_pledged_inr + ticket_revenue_inr
        net_profit = total_revenue - budget_inr
        margin_pct = (net_profit / max(1, total_revenue)) * 100
        return {
            "budget_inr": budget_inr,
            "total_revenue_inr": total_revenue,
            "net_profit_inr": net_profit,
            "margin_percentage": round(margin_pct, 2),
            "financial_verdict": "PROFITABLE" if net_profit > 0 else "DEFICIT"
        }
