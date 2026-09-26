"""
AQUA Continuous Learning Engine (ANTIGRAVITY Ω∞ Mode L)
Dynamically ingests customs circulars, court classification rulings, and statutory updates,
updates the TradeNexus HSCatalog knowledge base, and logs learning audit trails.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
eng_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "06_ENGINEERING"))
if eng_path not in sys.path:
    sys.path.insert(0, eng_path)

from src.hs_engine import HSCatalog


class ContinuousLearningEngine:
    DEFAULT_STORE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "knowledge_store.json"))
    JOURNAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "decision_journal.jsonl"))

    def __init__(self, store_path: Optional[str] = None):
        self.store_path = store_path or self.DEFAULT_STORE_PATH
        self.knowledge_store: Dict[str, Any] = self._load_store()
        self._sync_to_catalog()

    def _load_store(self) -> Dict[str, Any]:
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "rules_learned_count": 0,
            "rules": []
        }

    def _save_store(self):
        self.knowledge_store["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.knowledge_store["rules_learned_count"] = len(self.knowledge_store["rules"])
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_store, f, indent=2)

    def _sync_to_catalog(self):
        """
        Applies persisted learned rules to in-memory HSCatalog.DATABASE.
        """
        existing_codes = {entry["hs_code"]: entry for entry in HSCatalog.DATABASE}
        for rule in self.knowledge_store.get("rules", []):
            code = rule["hs_code"]
            if code in existing_codes:
                # Merge keywords and update tariff
                existing = existing_codes[code]
                for kw in rule.get("keywords", []):
                    if kw not in existing["keywords"]:
                        existing["keywords"].append(kw)
                existing["tariff"] = rule.get("tariff", existing["tariff"])
                existing["cbam"] = rule.get("cbam", existing["cbam"])
                existing["scomet"] = rule.get("scomet", existing["scomet"])
            else:
                entry = {
                    "hs_code": code,
                    "keywords": rule.get("keywords", []),
                    "tariff": rule.get("tariff", 7.5),
                    "cbam": rule.get("cbam", False),
                    "scomet": rule.get("scomet", False)
                }
                HSCatalog.DATABASE.append(entry)
                existing_codes[code] = entry

    def ingest_gazette_notification(
        self,
        source: str,
        hs_code: str,
        keywords: List[str],
        tariff: float,
        cbam: bool,
        scomet: bool,
        legal_basis: str
    ) -> Dict[str, Any]:
        """
        Ingests and compiles a statutory circular or court classification into the knowledge store.
        """
        now = datetime.now(timezone.utc)
        rule_hash = hashlib.sha256(f"{source}{hs_code}{now.isoformat()}".encode("utf-8")).hexdigest()[:12].upper()
        rule_id = f"RULE-{rule_hash}"

        rule_entry = {
            "rule_id": rule_id,
            "source": source,
            "hs_code": hs_code,
            "keywords": [k.lower().strip() for k in keywords],
            "tariff": tariff,
            "cbam": cbam,
            "scomet": scomet,
            "legal_basis": legal_basis,
            "learned_at": now.isoformat()
        }

        # Update or append in knowledge store
        updated = False
        for idx, r in enumerate(self.knowledge_store["rules"]):
            if r["hs_code"] == hs_code:
                # Merge
                for kw in rule_entry["keywords"]:
                    if kw not in r["keywords"]:
                        r["keywords"].append(kw)
                r["tariff"] = tariff
                r["cbam"] = cbam
                r["scomet"] = scomet
                r["legal_basis"] = legal_basis
                r["last_updated"] = now.isoformat()
                updated = True
                break

        if not updated:
            self.knowledge_store["rules"].append(rule_entry)

        self._save_store()
        self._sync_to_catalog()
        self._record_learning_event(rule_entry)

        return {
            "status": "LEARNED",
            "rule_id": rule_id,
            "hs_code": hs_code,
            "active_rules_count": len(HSCatalog.DATABASE),
            "catalog_entry": HSCatalog.classify(keywords[0])
        }

    def _record_learning_event(self, rule: Dict[str, Any]):
        """
        Logs continuous learning event to the decision journal.
        """
        try:
            entry = {
                "timestamp": rule["learned_at"],
                "decision_type": "KNOWLEDGE_COMPOUNDING",
                "mode": "MODE_L_LEARNING",
                "source": rule["source"],
                "hs_code": rule["hs_code"],
                "legal_basis": rule["legal_basis"],
                "impact": f"Added/Updated HS code {rule['hs_code']} with {len(rule['keywords'])} trigger keywords."
            }
            with open(self.JOURNAL_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def get_learning_stats(self) -> Dict[str, Any]:
        return {
            "total_rules_learned": len(self.knowledge_store.get("rules", [])),
            "total_catalog_rules": len(HSCatalog.DATABASE),
            "last_updated": self.knowledge_store.get("last_updated"),
            "learned_rules": self.knowledge_store.get("rules", [])
        }
