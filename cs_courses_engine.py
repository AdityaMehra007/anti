"""
CS Courses Engine - Ingestion, Relational Indexing, and Search Engine
for Developer-Y/cs-video-courses repository.

Provides:
- Deterministic parsing of courses from raw README markdown
- SQLite storage with FTS5 full-text search indexing
- JSON export and domain/university statistics aggregation
- Career roadmap synthesis and prerequisites resolution
"""

import os
import re
import json
import sqlite3
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent
DATA_DIR = WORKSPACE_ROOT / "data"
DB_PATH = DATA_DIR / "cs_video_courses.db"
JSON_PATH = DATA_DIR / "cs_video_courses.json"
README_PATH = DATA_DIR / "raw_cs_video_courses_readme.md"

# Universal institution catalog and pattern bindings
INSTITUTION_RULES = [
    ("MIT", [r"\bMIT\b", r"Massachusetts Institute of Technology"]),
    ("Stanford", [r"\bStanford\b"]),
    ("UC Berkeley", [r"\bBerkeley\b", r"\bUC Berkeley\b", r"\bUCB\b"]),
    ("Carnegie Mellon (CMU)", [r"\bCMU\b", r"Carnegie Mellon"]),
    ("Harvard", [r"\bHarvard\b"]),
    ("Caltech", [r"\bCaltech\b", r"California Institute of Technology"]),
    ("Cornell", [r"\bCornell\b", r"Cornell Tech"]),
    ("Princeton", [r"\bPrinceton\b"]),
    ("Columbia", [r"\bColumbia\b"]),
    ("University of Washington", [r"\bUW\b", r"University of Washington", r"UW Madison"]),
    ("UIUC", [r"\bUIUC\b", r"University of Illinois"]),
    ("Georgia Tech", [r"\bGatech\b", r"Georgia Tech"]),
    ("Oxford", [r"\bOxford\b"]),
    ("Cambridge", [r"\bCambridge\b"]),
    ("ETH Zurich", [r"ETH Zurich", r"\bETH\b"]),
    ("TUM (Munich)", [r"\bTUM\b", r"Technical University of Munich", r"Munich"]),
    ("UT Austin", [r"UT Austin", r"University of Texas"]),
    ("University of Toronto", [r"University of Toronto", r"\bUofT\b"]),
    ("University of Waterloo", [r"Waterloo"]),
    ("UBC", [r"\bUBC\b", r"University of British Columbia"]),
    ("UNSW", [r"\bUNSW\b", r"New South Wales"]),
    ("IIT (Indian Institutes of Technology)", [r"\bIIT\b", r"NPTEL", r"IIT Kanpur", r"IIT Kharagpur", r"IIT Bombay", r"IIT Madras", r"IIT Delhi"]),
    ("UCSD", [r"\bUCSD\b", r"UC San Diego"]),
    ("UCLA", [r"\bUCLA\b"]),
    ("NYU", [r"\bNYU\b", r"New York University", r"Courant"]),
    ("Brown", [r"\bBrown University\b", r"\bBrown\b"]),
    ("Yale", [r"\bYale\b"]),
    ("TU Delft", [r"TU Delft"]),
    ("University of Bonn", [r"Bonn"]),
    ("Virginia Tech", [r"Virginia Tech"]),
    ("EPFL", [r"\bEPFL\b"]),
    ("Purdue", [r"\bPurdue\b"]),
    ("Edinburgh", [r"Edinburgh"]),
    ("University of Michigan", [r"University of Michigan", r"\bUMich\b"]),
    ("Penn State", [r"Penn State"]),
    ("UPenn", [r"UPenn", r"University of Pennsylvania"]),
    ("UC Davis", [r"UC Davis"]),
    ("UC Santa Barbara (UCSB)", [r"UCSB", r"UC Santa Barbara"]),
    ("University of Utah", [r"University of Utah"]),
    ("Johns Hopkins", [r"Johns Hopkins", r"\bJHU\b"]),
    ("UMass", [r"UMass", r"University of Massachusetts"]),
    ("Northwestern", [r"Northwestern"]),
    ("Duke", [r"\bDuke\b"]),
    ("University of Chicago", [r"University of Chicago", r"\bUChicago\b"]),
    ("Rice University", [r"Rice University"]),
]

COURSE_CODE_REGEX = re.compile(
    r"\b([A-Z]{2,6}\s*(?:[A-Z]{1,4})?\s*\d{1,4}[A-Z]?(?:/\d{1,4}[A-Z]*)?|\d{1,2}\.\w+|\d{2}-\d{3}(?:/\d{3})?)\b"
)
YEAR_REGEX = re.compile(
    r"\b((?:Spring|Fall|Autumn|Winter|Summer)\s+20\d{2}|20\d{2}(?:-20\d{2})?)\b",
    re.IGNORECASE,
)
MARKDOWN_LINK_REGEX = re.compile(r"\[(.*?)\]\((.*?)\)")


def slugify(text: str) -> str:
    """Normalize text into a clean URL-safe slug."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def determine_level(code: str, category: str, title: str) -> str:
    """Classify course into academic level based on course number and content."""
    title_lower = title.lower()
    cat_lower = category.lower()

    if "phd" in title_lower or "doctoral" in title_lower or "research" in title_lower:
        return "Graduate / Research"

    # Extract digits from course code
    digits = re.findall(r"\d+", code)
    if digits:
        val = int(digits[0])
        # MIT style: 6.001 is intro, 6.046 is core, 6.824 is advanced grad
        if "." in code:
            parts = code.split(".")
            if len(parts) > 1:
                sub_digits = re.findall(r"\d+", parts[1])
                if sub_digits:
                    sub_val = int(sub_digits[0])
                    if sub_val < 30:
                        return "Introductory (L1)"
                    elif sub_val < 50:
                        return "Core Intermediate (L2)"
                    elif sub_val < 80:
                        return "Advanced (L3)"
                    else:
                        return "Graduate / Mastery (L4)"

        # Standard university numbering (100 = Freshman, 200 = Soph, 300 = Junior, 400 = Senior, 500+ = Grad)
        if val < 100 or val in [101, 106, 110, 142, 150, 151, 600, 6000]:
            return "Introductory (L1)"
        elif val < 300:
            return "Core Intermediate (L2)"
        elif val < 600:
            return "Advanced (L3)"
        else:
            return "Graduate / Mastery (L4)"

    if "intro" in title_lower or "introduction" in cat_lower or "fundamental" in title_lower:
        return "Introductory (L1)"
    elif "advanced" in title_lower or "distributed" in title_lower or "deep" in title_lower:
        return "Advanced (L3)"

    return "Core Intermediate (L2)"


def parse_course_line(
    raw_line: str, category: str, subcategory: str, line_num: int
) -> Optional[Dict[str, Any]]:
    """Parse a single markdown bullet line into a structured course dictionary."""
    line = raw_line.strip()
    if line.startswith("- "):
        line = line[2:].strip()

    links = MARKDOWN_LINK_REGEX.findall(line)
    if not links and not ("http://" in line or "https://" in line):
        return None

    # Primary text representation
    text_repr = line
    if links and line.startswith("["):
        text_repr = links[0][0]
    elif "|" in line:
        text_repr = line.split("|")[0].strip()

    # Extract Course Code
    code_match = COURSE_CODE_REGEX.search(text_repr)
    course_code = code_match.group(1).strip() if code_match else ""

    # Match Institution
    matched_institution = "Other Universities & Labs"
    for uni_name, patterns in INSTITUTION_RULES:
        if any(re.search(p, line, re.IGNORECASE) for p in patterns):
            matched_institution = uni_name
            break

    # Match Term / Year
    year_match = YEAR_REGEX.search(line)
    year = year_match.group(1).strip() if year_match else ""

    # Match Instructor
    instructor = ""
    inst_match = re.search(
        r"(?:by\s+|Prof\.?\s+|Dr\.?\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", line
    )
    if inst_match:
        instructor = inst_match.group(1).strip()
    else:
        paren_match = re.search(
            r"\(([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)\)", line
        )
        if paren_match:
            candidate = paren_match.group(1).strip()
            if not any(
                k in candidate.lower()
                for k in [
                    "fall",
                    "spring",
                    "winter",
                    "summer",
                    "notes",
                    "youtube",
                    "video",
                    "complete",
                    "lecture",
                    "playlist",
                ]
            ):
                instructor = candidate

    # Parse Links
    video_links = []
    primary_url = ""

    video_keywords = ["video", "youtube", "watch", "lecture", "playlist", "vod"]
    video_domains = [
        "youtube.com",
        "youtu.be",
        "panopto.com",
        "vimeo.com",
        "bilibili.com",
        "video_galleries",
        "infocobuild",
    ]

    for label, url in links:
        url_lower = url.lower()
        lbl_lower = label.lower()

        is_video = any(domain in url_lower for domain in video_domains) or any(
            kw in lbl_lower for kw in video_keywords
        )

        if is_video:
            video_links.append({"label": label.strip(), "url": url.strip()})
        else:
            if not primary_url:
                primary_url = url.strip()

    if not primary_url and video_links:
        primary_url = video_links[0]["url"]

    # Title cleanup
    clean_title = text_repr
    if course_code:
        clean_title = re.sub(
            re.escape(course_code) + r"\s*[-:–]?\s*", "", clean_title, count=1
        ).strip()

    # Strip institution names from title ends
    clean_title = re.sub(
        r"\s*[-–,]\s*(?:MIT|Stanford|UC Berkeley|CMU|Carnegie Mellon|Harvard|UNSW|Caltech|Cornell|Princeton|UIUC|Gatech|IIT|TUM|UW).*$",
        "",
        clean_title,
        flags=re.IGNORECASE,
    ).strip()
    clean_title = re.sub(
        r"\s*\((?:Spring|Fall|Winter|Summer)?\s*20\d{2}.*?\)$",
        "",
        clean_title,
        flags=re.IGNORECASE,
    ).strip()
    clean_title = re.sub(r"^[\[\(]+|[\]\)]+$", "", clean_title).strip()
    if not clean_title:
        clean_title = text_repr

    # Generate persistent unique ID
    base_slug = slugify(f"{matched_institution}-{course_code or 'cs'}-{clean_title[:40]}")
    course_id = f"{base_slug}-{line_num}"

    level = determine_level(course_code, category, clean_title)

    return {
        "id": course_id,
        "line_number": line_num,
        "code": course_code,
        "title": clean_title,
        "category": category,
        "subcategory": subcategory or "General",
        "institution": matched_institution,
        "instructor": instructor,
        "year": year,
        "primary_url": primary_url,
        "video_urls": video_links,
        "video_count": len(video_links),
        "has_video": len(video_links) > 0,
        "level": level,
        "raw_markdown": raw_line.strip(),
    }


class CSCoursesEngine:
    """Master engine for parsing, caching, querying, and managing CS video courses."""

    def __init__(self, readme_path: Optional[Path] = None, db_path: Optional[Path] = None):
        self.readme_path = readme_path or README_PATH
        self.db_path = db_path or DB_PATH
        self.json_path = JSON_PATH
        self.courses: List[Dict[str, Any]] = []

    def ensure_data_dir(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def parse_readme(self) -> List[Dict[str, Any]]:
        """Parse the README.md file and extract all courses deterministically."""
        if not self.readme_path.exists():
            raise FileNotFoundError(f"README not found at {self.readme_path}")

        with open(self.readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Split after '## Courses' section to discard Table of Contents
        if "## Courses" in content:
            body = content.split("## Courses", 1)[1]
        else:
            body = content

        lines = body.split("\n")
        current_category = "General Computer Science"
        current_subcategory = ""
        parsed: List[Dict[str, Any]] = []

        for idx, line in enumerate(lines, start=1):
            s = line.strip()
            if s.startswith("### "):
                current_category = s.replace("### ", "").strip()
                current_subcategory = ""
                continue
            elif s.startswith("- ####") or s.startswith("####"):
                sub_match = re.search(r"\*\*(.+?)\*\*", s)
                if sub_match:
                    current_subcategory = sub_match.group(1).strip()
                else:
                    current_subcategory = s.replace("####", "").replace("-", "").strip()
                continue
            elif s.startswith("- ") and ("[" in s or "http" in s):
                item = parse_course_line(s, current_category, current_subcategory, idx)
                if item:
                    parsed.append(item)

        self.courses = parsed
        return parsed

    def build_database(self) -> int:
        """Create SQLite schema and insert all parsed courses with FTS5 virtual table."""
        self.ensure_data_dir()
        if not self.courses:
            self.parse_readme()

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Drop existing tables
        cur.execute("DROP TABLE IF EXISTS courses_fts;")
        cur.execute("DROP TABLE IF EXISTS courses;")

        # Create main relational table
        cur.execute(
            """
            CREATE TABLE courses (
                id TEXT PRIMARY KEY,
                line_number INTEGER,
                code TEXT,
                title TEXT,
                category TEXT,
                subcategory TEXT,
                institution TEXT,
                instructor TEXT,
                year TEXT,
                level TEXT,
                primary_url TEXT,
                video_count INTEGER,
                has_video INTEGER,
                video_urls_json TEXT,
                raw_markdown TEXT
            );
        """
        )

        # Create indexes for high-speed relational filtering
        cur.execute("CREATE INDEX idx_courses_category ON courses(category);")
        cur.execute("CREATE INDEX idx_courses_subcategory ON courses(subcategory);")
        cur.execute("CREATE INDEX idx_courses_institution ON courses(institution);")
        cur.execute("CREATE INDEX idx_courses_level ON courses(level);")
        cur.execute("CREATE INDEX idx_courses_has_video ON courses(has_video);")

        # Create FTS5 full text search table
        cur.execute(
            """
            CREATE VIRTUAL TABLE courses_fts USING fts5(
                id UNINDEXED,
                code,
                title,
                category,
                subcategory,
                institution,
                instructor,
                level,
                tokenize = 'porter unicode61'
            );
        """
        )

        # Insert records
        for c in self.courses:
            cur.execute(
                """
                INSERT INTO courses (
                    id, line_number, code, title, category, subcategory,
                    institution, instructor, year, level, primary_url,
                    video_count, has_video, video_urls_json, raw_markdown
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
                (
                    c["id"],
                    c["line_number"],
                    c["code"],
                    c["title"],
                    c["category"],
                    c["subcategory"],
                    c["institution"],
                    c["instructor"],
                    c["year"],
                    c["level"],
                    c["primary_url"],
                    c["video_count"],
                    1 if c["has_video"] else 0,
                    json.dumps(c["video_urls"]),
                    c["raw_markdown"],
                ),
            )

            cur.execute(
                """
                INSERT INTO courses_fts (
                    id, code, title, category, subcategory, institution, instructor, level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
                (
                    c["id"],
                    c["code"],
                    c["title"],
                    c["category"],
                    c["subcategory"],
                    c["institution"],
                    c["instructor"],
                    c["level"],
                ),
            )

        conn.commit()
        conn.close()

        # Save JSON catalog
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.courses, f, indent=2, ensure_ascii=False)

        return len(self.courses)

    def search_courses(
        self,
        query: str = "",
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        institution: Optional[str] = None,
        level: Optional[str] = None,
        has_video_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Fast hybrid full-text and relational search over courses."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        conditions = []
        params = []

        if query.strip():
            # Clean search query for FTS5 syntax
            safe_query = re.sub(r"[^\w\s*]", " ", query).strip()
            terms = [f'"{t}"*' for t in safe_query.split() if t]
            if terms:
                fts_expr = " AND ".join(terms)
                conditions.append(
                    "c.id IN (SELECT id FROM courses_fts WHERE courses_fts MATCH ?)"
                )
                params.append(fts_expr)

        if category and category != "All":
            conditions.append("c.category = ?")
            params.append(category)

        if subcategory and subcategory != "All":
            conditions.append("c.subcategory = ?")
            params.append(subcategory)

        if institution and institution != "All":
            conditions.append("c.institution = ?")
            params.append(institution)

        if level and level != "All":
            conditions.append("c.level = ?")
            params.append(level)

        if has_video_only:
            conditions.append("c.has_video = 1")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"""
            SELECT c.*
            FROM courses c
            {where_clause}
            ORDER BY c.line_number ASC
            LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])

        cur.execute(sql, params)
        rows = cur.fetchall()

        results = []
        for r in rows:
            item = dict(r)
            item["video_urls"] = json.loads(item["video_urls_json"])
            del item["video_urls_json"]
            item["has_video"] = bool(item["has_video"])
            results.append(item)

        conn.close()
        return results

    def get_summary_stats(self) -> Dict[str, Any]:
        """Generate high-level metadata and statistical distributions."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM courses;")
        total_courses = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM courses WHERE has_video = 1;")
        courses_with_videos = cur.fetchone()[0]

        cur.execute(
            """
            SELECT category, COUNT(*) as cnt 
            FROM courses 
            GROUP BY category 
            ORDER BY cnt DESC;
        """
        )
        tracks = [{"category": row[0], "count": row[1]} for row in cur.fetchall()]

        cur.execute(
            """
            SELECT institution, COUNT(*) as cnt 
            FROM courses 
            GROUP BY institution 
            ORDER BY cnt DESC;
        """
        )
        institutions = [
            {"institution": row[0], "count": row[1]} for row in cur.fetchall()
        ]

        cur.execute(
            """
            SELECT level, COUNT(*) as cnt 
            FROM courses 
            GROUP BY level 
            ORDER BY cnt DESC;
        """
        )
        levels = [{"level": row[0], "count": row[1]} for row in cur.fetchall()]

        conn.close()

        return {
            "total_courses": total_courses,
            "courses_with_videos": courses_with_videos,
            "total_categories": len(tracks),
            "total_institutions": len(institutions),
            "tracks": tracks,
            "institutions": institutions,
            "levels": levels,
        }


if __name__ == "__main__":
    engine = CSCoursesEngine()
    print("Ingesting CS Video Courses from README...")
    count = engine.build_database()
    print(f"Successfully loaded and indexed {count} courses into {DB_PATH}!")
    stats = engine.get_summary_stats()
    print(
        f"Summary: {stats['total_courses']} courses across {stats['total_categories']} tracks and {stats['total_institutions']} institutions."
    )
