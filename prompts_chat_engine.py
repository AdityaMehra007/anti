"""
prompts_chat_engine.py — High-Performance Prompts.chat Deep Module & Engine
=============================================================================
Supreme prompt intelligence, FTS5 indexing, variable interpolation,
quality auditing, and Universal Job Taxonomy mapping for all 2,627+ prompts.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sqlite3
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Support massive text fields in community prompt CSVs
csv.field_size_limit(20000000)

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = ROOT_DIR / "external" / "prompts-chat" / "prompts.csv"
DEFAULT_DB_PATH = ROOT_DIR / "data" / "prompts_chat.db"
DEFAULT_BOOK_DIR = ROOT_DIR / "external" / "prompts-chat" / "src" / "content" / "book"


@dataclass
class PromptVariable:
    name: str
    default_value: str
    raw_token: str
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PromptRecord:
    id: int
    slug: str
    act: str
    prompt: str
    for_devs: bool
    type: str
    contributor: str
    variables: List[PromptVariable] = field(default_factory=list)
    quality_score: int = 0
    category: str = "General"
    archetype: str = "GENERAL_ASSISTANT"
    related_skills: List[str] = field(default_factory=list)
    char_count: int = 0
    word_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["variables"] = [v.to_dict() if isinstance(v, PromptVariable) else v for v in self.variables]
        return d


class VariableExtractor:
    """Detects and interpolates parameterized prompt variables."""

    # Patterns: ${Name:Default}, ${Name}, [Name:Default], [Name], {Name}
    VAR_PATTERN_DOLLAR = re.compile(r"\$\{([^}]+)\}")
    VAR_PATTERN_BRACKET = re.compile(r"\[([A-Z][a-zA-Z0-9_\s]{2,30})\]")

    @classmethod
    def extract(cls, text: str) -> List[PromptVariable]:
        variables: List[PromptVariable] = []
        seen = set()

        # Find ${Variable:Default} or ${Variable}
        for match in cls.VAR_PATTERN_DOLLAR.finditer(text):
            raw = match.group(0)
            inner = match.group(1).strip()
            if ":" in inner:
                name, default = inner.split(":", 1)
                name, default = name.strip(), default.strip()
            else:
                name, default = inner, ""

            if name and name not in seen:
                seen.add(name)
                variables.append(PromptVariable(name=name, default_value=default, raw_token=raw))

        # Find [Variable] style placeholders if not already covered
        for match in cls.VAR_PATTERN_BRACKET.finditer(text):
            raw = match.group(0)
            name = match.group(1).strip()
            if name and name not in seen and not name.lower().startswith("http"):
                seen.add(name)
                variables.append(PromptVariable(name=name, default_value="", raw_token=raw))

        return variables

    @classmethod
    def interpolate(cls, text: str, values: Dict[str, str]) -> str:
        result = text
        # Replace ${Name:Default} or ${Name}
        for match in cls.VAR_PATTERN_DOLLAR.finditer(text):
            raw = match.group(0)
            inner = match.group(1).strip()
            name = inner.split(":", 1)[0].strip() if ":" in inner else inner
            default = inner.split(":", 1)[1].strip() if ":" in inner else ""
            replacement = values.get(name, default if default else raw)
            result = result.replace(raw, replacement)

        # Replace [Name]
        for match in cls.VAR_PATTERN_BRACKET.finditer(result):
            raw = match.group(0)
            name = match.group(1).strip()
            if name in values:
                result = result.replace(raw, values[name])

        return result


class QualityScorer:
    """Scores prompt effectiveness and robustness (0-100)."""

    POSITIVE_MARKERS = [
        (re.compile(r"i want you to act as", re.I), 15, "Explicit role grounding"),
        (re.compile(r"do not|never|avoid|only reply|do not write explanations", re.I), 20, "Strict negative boundaries"),
        (re.compile(r"format|markdown|table|bullet points|json|code block", re.I), 15, "Output structure specification"),
        (re.compile(r"first (sentence|command|task|question) is", re.I), 15, "Immediate priming sequence"),
        (re.compile(r"example|step-by-step|think|rationale", re.I), 10, "Procedural reasoning guidance"),
        (re.compile(r"\$\{[^}]+\}|\[[A-Za-z]+\]", re.I), 10, "Dynamic parameterization"),
    ]

    @classmethod
    def score(cls, prompt_text: str) -> Tuple[int, List[str]]:
        score = 20  # Base score
        positives = []

        for pattern, points, desc in cls.POSITIVE_MARKERS:
            if pattern.search(prompt_text):
                score += points
                positives.append(desc)

        # Length bonus
        words = len(prompt_text.split())
        if 40 <= words <= 350:
            score += 10
            positives.append("Optimal prompt density (40-350 words)")
        elif words > 350:
            score += 5
            positives.append("Comprehensive long-form prompt")

        # Clamp 0-100
        score = min(100, max(0, score))
        return score, positives


class ArchetypeClassifier:
    """Classifies prompts into Categories and Universal Job Archetypes."""

    CATEGORY_RULES = [
        ("Software & Coding", re.compile(r"developer|programmer|terminal|console|code|sql|python|javascript|solidity|debug|regex|api|docker|linux|git|c\+\+|css|html", re.I)),
        ("Writing & Editorial", re.compile(r"translator|editor|essay|poet|novelist|storyteller|scriptwriter|writer|copywriter|proofread|plagiarism|summarizer", re.I)),
        ("Business & Strategy", re.compile(r"interview|recruiter|ceo|consultant|startup|marketing|sales|investment|business|advertis|pitch|pricing|accounting|financial", re.I)),
        ("Academic & Science", re.compile(r"math|physic|chemist|philosophy|historian|scientific|researcher|teacher|academic|tutor|astronomer|statistician", re.I)),
        ("Creative & Arts", re.compile(r"artist|composer|song|rapper|designer|photographer|filmmaker|game|comedian|midjourney|dall-e", re.I)),
        ("Productivity & Coaching", re.compile(r"coach|mentor|planner|organizer|counselor|travel guide|dietitian|personal trainer|chef|nutritionist", re.I)),
        ("Legal & Governance", re.compile(r"lawyer|legal|compliance|contract|attorney|policy|patent", re.I)),
    ]

    ARCHETYPE_RULES = [
        ("SOFTWARE_ENGINEER_BACKEND", re.compile(r"linux|terminal|backend|sql|api|database|solidity|ethereum|docker|server|python", re.I)),
        ("SOFTWARE_ENGINEER_FRONTEND", re.compile(r"javascript|css|html|frontend|react|vue|web design|svg", re.I)),
        ("AI_LLM_ENGINEER", re.compile(r"ai|llm|prompt|machine learning|model|embedding|neural", re.I)),
        ("MANAGEMENT_CONSULTANT", re.compile(r"consultant|strategy|framework|mckinsey|advisory|analyst", re.I)),
        ("TECHNICAL_RECRUITER", re.compile(r"interviewer|recruiter|talent|candidate|hiring|job interview", re.I)),
        ("FINANCIAL_ANALYST_FPA", re.compile(r"financial|accounting|investment|valuation|excel|spreadsheet|stock", re.I)),
        ("PRODUCT_MANAGER", re.compile(r"product manager|user story|roadmap|prd|agile|scrum", re.I)),
        ("TECHNICAL_WRITER", re.compile(r"technical writer|documentation|translator|manual|editor", re.I)),
        ("GROWTH_MARKETING_MANAGER", re.compile(r"growth|marketing|seo|social media|copywriter|advertis", re.I)),
        ("CYBERSECURITY_ENGINEER", re.compile(r"security|penetration|cyber|vulnerability|exploit|firewall", re.I)),
    ]

    SKILL_MAPPINGS = {
        "SOFTWARE_ENGINEER_BACKEND": ["backend-patterns", "docker-patterns", "api-design", "systematic-debugging"],
        "SOFTWARE_ENGINEER_FRONTEND": ["frontend-design", "react-best-practices", "web-quality-audit"],
        "AI_LLM_ENGINEER": ["system-prompts-intelligence", "genai-skill-01", "eval-harness"],
        "MANAGEMENT_CONSULTANT": ["exec-strategy-skill-001", "omega-capital-allocation"],
        "TECHNICAL_RECRUITER": ["recruiter-network-strike", "interview-simulator-pro", "talent-skill-01"],
        "FINANCIAL_ANALYST_FPA": ["finance-treasury-skill-001", "finance-billing-ops"],
        "PRODUCT_MANAGER": ["product-lens", "product-capability", "decomposition-planning-roadmap"],
        "TECHNICAL_WRITER": ["docs-writer", "writing-for-agents", "humanizer"],
        "GROWTH_MARKETING_MANAGER": ["growth-seo-skill-001", "content-to-pipeline", "ai-sdr"],
        "CYBERSECURITY_ENGINEER": ["security-best-practices", "security-threat-model", "antifragile-red-team"],
    }

    @classmethod
    def classify(cls, act: str, prompt: str) -> Tuple[str, str, List[str]]:
        combined = f"{act} {prompt}"
        
        # Category
        category = "General"
        for cat_name, cat_re in cls.CATEGORY_RULES:
            if cat_re.search(combined):
                category = cat_name
                break

        # Archetype
        archetype = "GENERAL_ASSISTANT"
        for arch_name, arch_re in cls.ARCHETYPE_RULES:
            if arch_re.search(combined):
                archetype = arch_name
                break

        skills = cls.SKILL_MAPPINGS.get(archetype, ["prompt-lookup", "system-prompts-intelligence"])
        return category, archetype, skills


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", cleaned)


class PromptsChatEngine:
    """Master Database & Query Engine for Prompts.chat."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH, csv_path: Path = DEFAULT_CSV_PATH):
        self.db_path = Path(db_path)
        self.csv_path = Path(csv_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    act TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    for_devs INTEGER NOT NULL DEFAULT 0,
                    type TEXT NOT NULL DEFAULT 'TEXT',
                    contributor TEXT NOT NULL DEFAULT '',
                    variables_json TEXT NOT NULL DEFAULT '[]',
                    quality_score INTEGER NOT NULL DEFAULT 0,
                    category TEXT NOT NULL DEFAULT 'General',
                    archetype TEXT NOT NULL DEFAULT 'GENERAL_ASSISTANT',
                    related_skills_json TEXT NOT NULL DEFAULT '[]',
                    char_count INTEGER NOT NULL DEFAULT 0,
                    word_count INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_prompts_act ON prompts(act)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_prompts_category ON prompts(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_prompts_devs ON prompts(for_devs)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_prompts_archetype ON prompts(archetype)")

            # Create FTS5 full-text search table
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS prompts_fts USING fts5(
                    act,
                    prompt,
                    category,
                    contributor,
                    content='prompts',
                    content_rowid='id'
                )
            """)
            conn.commit()

    def count(self) -> int:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM prompts")
            return cur.fetchone()[0]

    def sync(self, force: bool = False) -> int:
        """Parses CSV and syncs into SQLite FTS5 database."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Prompts CSV not found at {self.csv_path}")

        current_count = self.count()
        if current_count > 0 and not force:
            return current_count

        records_to_insert = []
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            seen_slugs = set()
            for idx, row in enumerate(reader, 1):
                act = (row.get("act") or "").strip()
                prompt = (row.get("prompt") or "").strip()
                if not act or not prompt:
                    continue

                for_devs = 1 if str(row.get("for_devs", "")).strip().lower() in ("true", "1") else 0
                ptype = (row.get("type") or "TEXT").strip().upper()
                contributor = (row.get("contributor") or "").strip()

                base_slug = slugify(act) or f"prompt-{idx}"
                slug = base_slug
                counter = 2
                while slug in seen_slugs:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                seen_slugs.add(slug)

                variables = VariableExtractor.extract(prompt)
                quality_score, _ = QualityScorer.score(prompt)
                category, archetype, skills = ArchetypeClassifier.classify(act, prompt)

                char_count = len(prompt)
                word_count = len(prompt.split())

                records_to_insert.append((
                    slug,
                    act,
                    prompt,
                    for_devs,
                    ptype,
                    contributor,
                    json.dumps([v.to_dict() for v in variables]),
                    quality_score,
                    category,
                    archetype,
                    json.dumps(skills),
                    char_count,
                    word_count
                ))

        with self._get_connection() as conn:
            conn.execute("DELETE FROM prompts")
            conn.execute("DELETE FROM prompts_fts")
            conn.executemany("""
                INSERT INTO prompts (
                    slug, act, prompt, for_devs, type, contributor,
                    variables_json, quality_score, category, archetype,
                    related_skills_json, char_count, word_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records_to_insert)

            # Rebuild FTS
            conn.execute("INSERT INTO prompts_fts(prompts_fts) VALUES('rebuild')")
            conn.commit()

        return len(records_to_insert)

    def _row_to_record(self, row: sqlite3.Row) -> PromptRecord:
        raw_vars = json.loads(row["variables_json"])
        vars_objs = [PromptVariable(**v) for v in raw_vars]
        skills = json.loads(row["related_skills_json"])

        return PromptRecord(
            id=row["id"],
            slug=row["slug"],
            act=row["act"],
            prompt=row["prompt"],
            for_devs=bool(row["for_devs"]),
            type=row["type"],
            contributor=row["contributor"],
            variables=vars_objs,
            quality_score=row["quality_score"],
            category=row["category"],
            archetype=row["archetype"],
            related_skills=skills,
            char_count=row["char_count"],
            word_count=row["word_count"],
        )

    def search(
        self,
        query: str = "",
        category: Optional[str] = None,
        for_devs: Optional[bool] = None,
        archetype: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[PromptRecord], int]:
        """Performs full-text search and faceted filtering."""
        with self._get_connection() as conn:
            conditions = []
            params: List[Any] = []

            # Clean query for FTS5
            cleaned_q = query.strip()
            if cleaned_q:
                # Escape FTS5 double quotes and form prefix search
                terms = [re.sub(r"[^\w]", "", t) for t in cleaned_q.split()]
                fts_query = " ".join(f'"{t}"*' for t in terms if t)
                if fts_query:
                    conditions.append("prompts.id IN (SELECT rowid FROM prompts_fts WHERE prompts_fts MATCH ?)")
                    params.append(fts_query)

            if category and category.lower() != "all":
                conditions.append("prompts.category = ?")
                params.append(category)

            if for_devs is not None:
                conditions.append("prompts.for_devs = ?")
                params.append(1 if for_devs else 0)

            if archetype and archetype.lower() != "all":
                conditions.append("prompts.archetype = ?")
                params.append(archetype)

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            # Count total matching
            count_sql = f"SELECT COUNT(*) FROM prompts {where_clause}"
            total = conn.execute(count_sql, params).fetchone()[0]

            # Fetch rows ordered by quality score descending
            order_clause = "ORDER BY quality_score DESC, act ASC"
            if cleaned_q and fts_query:
                # Rank by relevance
                order_clause = "ORDER BY quality_score DESC"

            data_sql = f"SELECT * FROM prompts {where_clause} {order_clause} LIMIT ? OFFSET ?"
            cur = conn.execute(data_sql, params + [limit, offset])
            records = [self._row_to_record(r) for r in cur.fetchall()]

            return records, total

    def get_by_act(self, act_name: str) -> Optional[PromptRecord]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM prompts WHERE LOWER(act) = LOWER(?) LIMIT 1", (act_name.strip(),))
            row = cur.fetchone()
            return self._row_to_record(row) if row else None

    def get_by_slug(self, slug: str) -> Optional[PromptRecord]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM prompts WHERE slug = ? LIMIT 1", (slug.strip(),))
            row = cur.fetchone()
            return self._row_to_record(row) if row else None

    def get_by_id(self, prompt_id: int) -> Optional[PromptRecord]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM prompts WHERE id = ? LIMIT 1", (prompt_id,))
            row = cur.fetchone()
            return self._row_to_record(row) if row else None

    def get_random(self, for_devs: Optional[bool] = None, category: Optional[str] = None) -> Optional[PromptRecord]:
        with self._get_connection() as conn:
            conditions = []
            params: List[Any] = []
            if for_devs is not None:
                conditions.append("for_devs = ?")
                params.append(1 if for_devs else 0)
            if category and category.lower() != "all":
                conditions.append("category = ?")
                params.append(category)

            where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            sql = f"SELECT * FROM prompts {where} ORDER BY RANDOM() LIMIT 1"
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            return self._row_to_record(row) if row else None

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM prompts").fetchone()[0]
            dev_total = conn.execute("SELECT COUNT(*) FROM prompts WHERE for_devs = 1").fetchone()[0]
            avg_quality = conn.execute("SELECT AVG(quality_score) FROM prompts").fetchone()[0] or 0
            contributors_count = conn.execute("SELECT COUNT(DISTINCT contributor) FROM prompts WHERE contributor != ''").fetchone()[0]

            cat_cur = conn.execute("SELECT category, COUNT(*) as cnt FROM prompts GROUP BY category ORDER BY cnt DESC")
            categories = {row["category"]: row["cnt"] for row in cat_cur.fetchall()}

            type_cur = conn.execute("SELECT type, COUNT(*) as cnt FROM prompts GROUP BY type")
            types = {row["type"]: row["cnt"] for row in type_cur.fetchall()}

            top_contrib = conn.execute(
                "SELECT contributor, COUNT(*) as cnt FROM prompts WHERE contributor != '' GROUP BY contributor ORDER BY cnt DESC LIMIT 10"
            )
            contributors = [{"name": row["contributor"], "count": row["cnt"]} for row in top_contrib.fetchall()]

            return {
                "total_prompts": total,
                "developer_prompts": dev_total,
                "average_quality": round(float(avg_quality), 1),
                "unique_contributors": contributors_count,
                "categories": categories,
                "types": types,
                "top_contributors": contributors,
            }

    def fill_prompt(self, act_or_slug: str, values: Dict[str, str]) -> Optional[str]:
        record = self.get_by_act(act_or_slug) or self.get_by_slug(act_or_slug)
        if not record:
            return None
        return VariableExtractor.interpolate(record.prompt, values)

    def get_book_languages(self) -> List[Dict[str, str]]:
        """Returns list of supported languages for the interactive prompt engineering book."""
        lang_names = {
            "en": "English",
            "es": "Spanish (Español)",
            "tr": "Turkish (Türkçe)",
            "zh": "Chinese (中文)",
            "ja": "Japanese (日本語)",
            "fr": "French (Français)",
            "de": "German (Deutsch)",
            "pt": "Portuguese (Português)",
            "it": "Italian (Italiano)",
            "ru": "Russian (Русский)",
            "ko": "Korean (한국어)",
            "ar": "Arabic (العربية)",
            "nl": "Dutch (Nederlands)",
            "fa": "Persian (فارسی)",
            "he": "Hebrew (עברית)",
            "el": "Greek (Ελληνικά)",
            "az": "Azerbaijani (Azərbaycan)",
        }
        res = [{"code": "en", "name": "English"}]
        if DEFAULT_BOOK_DIR.exists():
            for d in sorted(DEFAULT_BOOK_DIR.iterdir()):
                if d.is_dir() and d.name in lang_names and d.name != "en":
                    res.append({"code": d.name, "name": lang_names[d.name]})
        return res

    def get_book_chapters(self, lang: str = "en") -> List[Dict[str, Any]]:
        """Returns list of chapters from the interactive prompt engineering book."""
        target_dir = DEFAULT_BOOK_DIR if lang == "en" else DEFAULT_BOOK_DIR / lang
        if not target_dir.exists():
            target_dir = DEFAULT_BOOK_DIR

        chapters = []
        for p in sorted(target_dir.glob("*.mdx")):
            slug = p.stem
            # Clean human title from filename (e.g. 01-understanding-ai-models -> Understanding AI Models)
            parts = slug.split("-", 1)
            raw_title = parts[1] if len(parts) > 1 else parts[0]
            title = raw_title.replace("-", " ").title()
            chapters.append({
                "slug": slug,
                "title": title,
                "filename": p.name,
                "size_bytes": p.stat().st_size
            })
        return chapters

    def get_book_chapter(self, slug_or_filename: str, lang: str = "en") -> Optional[Dict[str, Any]]:
        """Retrieves raw content of a specific book chapter."""
        target_dir = DEFAULT_BOOK_DIR if lang == "en" else DEFAULT_BOOK_DIR / lang
        if not target_dir.exists():
            target_dir = DEFAULT_BOOK_DIR

        filename = slug_or_filename if slug_or_filename.endswith(".mdx") else f"{slug_or_filename}.mdx"
        file_path = target_dir / filename
        if not file_path.exists():
            # Try searching by partial stem
            matches = list(target_dir.glob(f"*{slug_or_filename}*.mdx"))
            if matches:
                file_path = matches[0]
            else:
                return None

        content = file_path.read_text(encoding="utf-8")
        slug = file_path.stem
        parts = slug.split("-", 1)
        raw_title = parts[1] if len(parts) > 1 else parts[0]
        title = raw_title.replace("-", " ").title()

        return {
  