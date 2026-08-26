"""
WEB DATA NORMALIZER
Sanitizes raw markdown, standardizes dates, salaries, locations, and skills.
"""
import re
from typing import Dict, Any, List, Optional

class WebDataNormalizer:
    @staticmethod
    def normalize_location(location_str: str) -> str:
        loc = (location_str or "").strip()
        if not loc:
            return "Bengaluru, India"
        lower = loc.lower()
        if "bangalore" in lower or "bengaluru" in lower:
            if "hybrid" in lower:
                return "Bengaluru, India (Hybrid)"
            elif "remote" in lower:
                return "Bengaluru, India (Remote Available)"
            return "Bengaluru, India"
        if "remote" in lower:
            return "Remote"
        if "hyderabad" in lower:
            return "Hyderabad, India"
        if "mumbai" in lower:
            return "Mumbai, India"
        if "pune" in lower:
            return "Pune, India"
        if "delhi" in lower or "ncr" in lower or "gurugram" in lower or "noida" in lower:
            return "Delhi NCR / Gurugram, India"
        return loc

    @staticmethod
    def normalize_work_mode(text: str) -> str:
        lower = text.lower()
        if "hybrid" in lower:
            return "Hybrid"
        if "remote" in lower or "work from home" in lower:
            return "Remote"
        if "on-site" in lower or "onsite" in lower or "office" in lower:
            return "On-site"
        return "Hybrid"

    @staticmethod
    def normalize_salary(salary_str: Optional[str]) -> Optional[str]:
        if not salary_str:
            return None
        clean = re.sub(r"\s+", " ", salary_str.strip())
        return clean

    @staticmethod
    def extract_clean_text_lines(markdown_str: str) -> List[str]:
        if not markdown_str:
            return []
        lines = []
        for line in markdown_str.splitlines():
            cleaned = line.strip(" *#-_\t")
            if cleaned and len(cleaned) > 2:
                lines.append(cleaned)
        return lines
