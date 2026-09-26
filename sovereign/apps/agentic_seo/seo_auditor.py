import re, json
from datetime import datetime

class AgenticSEOEngine:
    '''Multi-Agent Technical SEO & Content Optimization Engine.'''
    def __init__(self):
        self.target_keywords = ["international business analyst", "supply chain consulting", "bengaluru management analyst"]

    def audit_content(self, text_content, target_keyword):
        words = re.findall(r"\w+", text_content.lower())
        total_words = len(words)
        kw_count = text_content.lower().count(target_keyword.lower())
        density = (kw_count / max(1, total_words)) * 100

        recommendations = []
        if density < 0.5:
            recommendations.append(f"Increase keyword prominence for '{target_keyword}' (Current density: {density:.2f}%).")
        elif density > 3.0:
            recommendations.append(f"Keyword stuffing risk for '{target_keyword}' (Current density: {density:.2f}%).")
        else:
            recommendations.append("Keyword density is in optimal range (1.0% - 2.5%).")

        return {
            "total_words": total_words,
            "keyword": target_keyword,
            "keyword_count": kw_count,
            "density_percentage": round(density, 2),
            "recommendations": recommendations,
            "audited_at": datetime.now().isoformat()
        }
