import os, csv, re

class DataEngine:
    """Reproducible Data Cleaning, Normalization and Deduplication Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def clean_string(self, text):
        if not text: return ""
        return re.sub(r"\s+", " ", str(text).strip())

    def deduplicate_rows(self, rows, key_field):
        seen = set()
        unique = []
        for r in rows:
            val = r.get(key_field, "").strip().lower()
            if val and val in seen:
                continue
            if val: seen.add(val)
            unique.append(r)
        return unique, len(rows) - len(unique)
