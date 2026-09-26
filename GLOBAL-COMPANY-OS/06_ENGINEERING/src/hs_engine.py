import re

class HSCatalog:
    # Deterministic reference catalog for key Indian export commodities
    DATABASE = [
        {"hs_code": "84821010", "keywords": ["ball bearing", "radial ball bearing", "steel bearing"], "tariff": 7.5, "cbam": False, "scomet": False},
        {"hs_code": "87082900", "keywords": ["auto parts", "motor vehicle body parts", "chassis bracket", "sheet metal stampings", "exhaust manifolds"], "tariff": 10.0, "cbam": False, "scomet": False},
        {"hs_code": "72081000", "keywords": ["hot rolled steel", "steel coil", "iron flat rolled"], "tariff": 12.5, "cbam": True, "scomet": False},
        {"hs_code": "73181500", "keywords": ["fasteners", "high-tensile fasteners", "steel bolts", "threaded screws", "cold extruded pins"], "tariff": 5.0, "cbam": True, "scomet": False},
        {"hs_code": "76011010", "keywords": ["aluminium ingot", "unwrought aluminium", "aluminium alloy"], "tariff": 8.0, "cbam": True, "scomet": False},
        {"hs_code": "76169990", "keywords": ["aluminum articles", "aluminum die-cast parts", "aluminum casting"], "tariff": 7.5, "cbam": True, "scomet": False},
        {"hs_code": "84099990", "keywords": ["engine cylinder blocks", "camshafts", "connecting rod", "cylinder blocks"], "tariff": 7.5, "cbam": False, "scomet": False},
        {"hs_code": "84099190", "keywords": ["electronic throttle bodies", "fuel injection pumps", "carburetors"], "tariff": 7.5, "cbam": False, "scomet": False},
        {"hs_code": "84314990", "keywords": ["mining transmission shafts", "earthmoving equipment assemblies", "transmission shafts"], "tariff": 7.5, "cbam": False, "scomet": True},
        {"hs_code": "85443000", "keywords": ["wiring harness", "electrical wiring harness", "cable sets"], "tariff": 5.0, "cbam": False, "scomet": False},
        {"hs_code": "68138100", "keywords": ["brake linings", "disc pads", "clutch facings", "friction material"], "tariff": 6.5, "cbam": False, "scomet": False},
        {"hs_code": "90292090", "keywords": ["instrument clusters", "speedometers", "tachometers", "telematics control"], "tariff": 6.0, "cbam": False, "scomet": False},
        {"hs_code": "87083000", "keywords": ["transmission housings", "disc brakes", "alloy wheels"], "tariff": 8.5, "cbam": False, "scomet": False},
        {"hs_code": "62052000", "keywords": ["cotton shirt", "men cotton apparel", "woven shirt"], "tariff": 5.0, "cbam": False, "scomet": False},
        {"hs_code": "29022000", "keywords": ["benzene", "pure benzene", "aromatic hydrocarbon"], "tariff": 7.5, "cbam": False, "scomet": True}, # Dual-use SCOMET
        {"hs_code": "85423100", "keywords": ["integrated circuit", "microprocessor", "semiconductor chip"], "tariff": 0.0, "cbam": False, "scomet": True}
    ]

    @classmethod
    def classify(cls, description: str):
        desc_lower = description.lower()
        best_match = None
        highest_score = 0

        for entry in cls.DATABASE:
            score = 0
            for kw in entry["keywords"]:
                if kw in desc_lower:
                    score += 2
                else:
                    for token in kw.split():
                        if token in desc_lower:
                            score += 1
            if score > highest_score:
                highest_score = score
                best_match = entry

        if best_match and highest_score >= 1:
            confidence = min(0.99, 0.70 + (highest_score * 0.1))
            return {
                "hs_code": best_match["hs_code"],
                "confidence": round(confidence, 2),
                "tariff_rate": best_match["tariff"],
                "cbam_applicable": best_match["cbam"],
                "scomet_restricted": best_match["scomet"],
                "reasoning": f"Exact keyword match with official WCO/DGFT catalog index ({highest_score} matches)."
            }
        
        # Fallback category
        return {
            "hs_code": "99999999",
            "confidence": 0.40,
            "tariff_rate": 10.0,
            "cbam_applicable": False,
            "scomet_restricted": False,
            "reasoning": "No high-confidence match found; flagged for manual review."
        }
