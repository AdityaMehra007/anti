"""BSU OS (Bengaluru Startup Universe Operating System) Configuration.

Provides core path references, database defaults, mathematical scoring weights,
and cluster definitions for the Bengaluru tech ecosystem.
"""

from pathlib import Path
from typing import Dict, Any

# Base directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATABASE_PATH = BASE_DIR / "bsu_os.db"

# Server configuration
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# Scoring weights (sum to 1.0)
POWER_SCORE_WEIGHTS: Dict[str, float] = {
    "team_pedigree": 0.25,
    "tech_defensibility": 0.25,
    "capital_strength": 0.20,
    "product_velocity": 0.15,
    "market_tailwind": 0.15,
}

CAREER_SCORE_WEIGHTS: Dict[str, float] = {
    "runway_months": 0.25,
    "compensation_tier": 0.20,
    "leadership_caliber": 0.25,
    "learning_velocity": 0.20,
    "culture_sentiment": 0.10,
}

MOMENTUM_SCORE_WEIGHTS: Dict[str, float] = {
    "hiring_velocity": 0.30,
    "funding_recency": 0.30,
    "market_traction": 0.20,
    "product_release_rate": 0.20,
}

# Bengaluru Micro-Clusters Metadata
BENGALURU_CLUSTERS: Dict[str, Dict[str, Any]] = {
    "koramangala": {
        "id": "koramangala",
        "name": "Koramangala",
        "description": "The historic cradle of India's startup renaissance. High density of seed to Series B SaaS, AI, and consumer tech hubs.",
        "lat": 12.9352,
        "lng": 77.6245,
        "zoom": 14,
        "primary_sectors": ["AI / ML", "SaaS", "FinTech", "D2C"],
        "vibe": "Cafe pitches, seed stage labs, high founder density, Third Wave & Blue Tokai deal hubs",
    },
    "hsr_layout": {
        "id": "hsr_layout",
        "name": "HSR Layout",
        "description": "The modern engine of Bengaluru startups. Home to India's most aggressive early and growth stage scale-ups.",
        "lat": 12.9121,
        "lng": 77.6446,
        "zoom": 14,
        "primary_sectors": ["GenAI", "DevTools", "Quick Commerce", "FinTech"],
        "vibe": "Sector 1-7 founder villas, aggressive tech scaling, late-night hackathons",
    },
    "indiranagar": {
        "id": "indiranagar",
        "name": "Indiranagar",
        "description": "VC headquarters, executive networks, design studios, and high-velocity consumer tech brands.",
        "lat": 12.9784,
        "lng": 77.6408,
        "zoom": 14,
        "primary_sectors": ["Consumer Tech", "Venture Capital", "Media", "Design"],
        "vibe": "100ft Road coffee meets Series A-D partner meetings and brand agency war rooms",
    },
    "outer_ring_road": {
        "id": "outer_ring_road",
        "name": "Outer Ring Road (ORR / Bellandur)",
        "description": "The economic powerhouse corridor. Mega-campuses, global tech hubs, unicorns, and high-throughput engineering centers.",
        "lat": 12.9279,
        "lng": 77.6835,
        "zoom": 13,
        "primary_sectors": ["Enterprise SaaS", "GCC Tech", "FinTech", "Logistics Tech"],
        "vibe": "Massive tech parks (Ecospace, Cessna), scale-up headquarters, institutional tech muscle",
    },
    "whitefield": {
        "id": "whitefield",
        "name": "Whitefield",
        "description": "Deep-tech, semiconductor, aerospace, IoT, and high-performance industrial engineering laboratories.",
        "lat": 12.9698,
        "lng": 77.7500,
        "zoom": 13,
        "primary_sectors": ["Deep-Tech", "SpaceTech", "Semiconductors", "Automotive / EV"],
        "vibe": "ITPB, aerospace labs, clean-rooms, massive engineering scale",
    },
    "electronic_city": {
        "id": "electronic_city",
        "name": "Electronic City",
        "description": "Hardware manufacturing, EV powertrains, telecommunications, and advanced materials engineering.",
        "lat": 12.8452,
        "lng": 77.6602,
        "zoom": 13,
        "primary_sectors": ["Hardware", "EV / CleanTech", "Telecom", "Robotics"],
        "vibe": "Hardware prototypes, EV testing tracks, manufacturing plants",
    },
    "cbd_central": {
        "id": "cbd_central",
        "name": "Central Business District (MG Rd / Lavelle Rd)",
        "description": "Premier institutional venture funds, legal/compliance advisory, and corporate innovation centers.",
        "lat": 12.9716,
        "lng": 77.5946,
        "zoom": 14,
        "primary_sectors": ["Venture Capital", "FinTech", "Family Offices", "Private Equity"],
        "vibe": "UB City boardrooms, institutional capital, landmark corporate headquarters",
    },
}
