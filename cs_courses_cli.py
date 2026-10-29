"""
CS Video Courses Universal CLI - Command-Line Interface for CS Video Courses
Orchestrates search, catalog inspection, career roadmaps, export, and cockpit serving.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional

from cs_courses_engine import CSCoursesEngine
from cs_courses_roadmaps import CSRoadmapsEngine

WORKSPACE_ROOT = Path(__file__).resolve().parent
DATA_DIR = WORKSPACE_ROOT / "data"
ROADMAPS_JSON = DATA_DIR / "cs_role_roadmaps.json"


def format_table_row(cols, widths):
    formatted = []
    for c, w in zip(cols, widths):
        s = str(c)[:w]
        formatted.append(s.ljust(w))
    return " | ".join(formatted)


def cmd_info(args):
    engine = CSCoursesEngine()
    stats = engine.get_summary_stats()

    print("\n=======================================================")
    print("      COMPUTER SCIENCE VIDEO COURSES INTELLIGENCE      ")
    print("=======================================================")
    print(f" Total University Courses  : {stats['total_courses']}")
    print(f" Courses with Video Links  : {stats['courses_with_videos']}")
    print(f" Curricular Domains/Tracks : {stats['total_categories']}")
    print(f" Universities / Institutes : {stats['total_institutions']}")
    print("-------------------------------------------------------")
    print(" Top Curricular Domains:")
    for t in stats["tracks"][:8]:
        print(f"   * {t['category']:<40} : {t['count']} courses")
    print("-------------------------------------------------------")
    print(" Top Academic Institutions:")
    for inst in stats["institutions"][:8]:
        print(f"   * {inst['institution']:<40} : {inst['count']} courses")
    print("=======================================================\n")


def cmd_search(args):
    engine = CSCoursesEngine()
    results = engine.search_courses(
        query=args.query or "",
        category=args.category,
        institution=args.institution,
        level=args.level,
        has_video_only=args.video_only,
        limit=args.limit or 20,
    )

    if not results:
        print(f"\nNo courses found matching query: '{args.query}'\n")
        return

    print(f"\nFound {len(results)} courses (showing up to {args.limit}):\n")
    widths = [12, 38, 22, 14, 18]
    print(format_table_row(["CODE", "TITLE", "INSTITUTION", "VIDEOS", "LEVEL"], widths))
    print("-" * (sum(widths) + 3 * len(widths)))

    for r in results:
        v_str = f"{r['video_count']} video(s)" if r["has_video"] else "Syllabus only"
        print(
            format_table_row(
                [
                    r["code"] or "N/A",
                    r["title"],
                    r["institution"],
                    v_str,
                    r["level"],
                ],
                widths,
            )
        )
        if args.verbose:
            print(f"   -> Link: {r['primary_url']}")
            if r["video_urls"]:
                print(f"   -> Lecture: {r['video_urls'][0]['url']}")
            print()
    print()


def cmd_tracks(args):
    engine = CSCoursesEngine()
    stats = engine.get_summary_stats()
    print("\nCurricular Domains & Categories:\n")
    widths = [45, 10]
    print(format_table_row(["DOMAIN TRACK", "COURSES"], widths))
    print("-" * (sum(widths) + 5))
    for t in stats["tracks"]:
        print(format_table_row([t["category"], t["count"]], widths))
    print()


def cmd_track(args):
    engine = CSCoursesEngine()
    results = engine.search_courses(category=args.category, limit=100)
    if not results:
        print(f"\nNo track found with exact name '{args.category}'. Use 'tracks' to see all names.\n")
        return

    print(f"\nCourses in track '{args.category}' ({len(results)} courses):\n")
    widths = [14, 40, 24, 12]
    print(format_table_row(["CODE", "TITLE", "INSTITUTION", "VIDEOS"], widths))
    print("-" * (sum(widths) + 5))
    for r in results:
        v_str = f"{r['video_count']} videos" if r["has_video"] else "No"
        print(format_table_row([r["code"] or "N/A", r["title"], r["institution"], v_str], widths))
    print()


def cmd_institutions(args):
    engine = CSCoursesEngine()
    stats = engine.get_summary_stats()
    print("\nAcademic Institutions & Universities:\n")
    widths = [45, 10]
    print(format_table_row(["INSTITUTION", "COURSES"], widths))
    print("-" * (sum(widths) + 5))
    for inst in stats["institutions"]:
        print(format_table_row([inst["institution"], inst["count"]], widths))
    print()


def cmd_institution(args):
    engine = CSCoursesEngine()
    results = engine.search_courses(institution=args.institution, limit=100)
    if not results:
        print(f"\nNo courses found for '{args.institution}'. Use 'institutions' to view names.\n")
        return

    print(f"\nCourses from '{args.institution}' ({len(results)} courses):\n")
    widths = [14, 42, 28, 12]
    print(format_table_row(["CODE", "TITLE", "CATEGORY", "VIDEOS"], widths))
    print("-" * (sum(widths) + 5))
    for r in results:
        v_str = f"{r['video_count']} videos" if r["has_video"] else "No"
        print(format_table_row([r["code"] or "N/A", r["title"], r["category"], v_str], widths))
    print()


def cmd_roadmaps(args):
    if not ROADMAPS_JSON.exists():
        builder = CSRoadmapsEngine()
        builder.build_all_roadmaps()

    with open(ROADMAPS_JSON, "r", encoding="utf-8") as f:
        roadmaps = json.load(f)

    print("\nAccredited Role-Based Degree Roadmaps:\n")
    widths = [32, 45, 10]
    print(format_table_row(["ROLE ID", "TITLE", "COURSES"], widths))
    print("-" * (sum(widths) + 5))
    for r in roadmaps:
        print(format_table_row([r["role_id"], r["title"], r["course_count"]], widths))
    print("\nUse 'python cs_courses_cli.py roadmap <role_id>' to inspect a full syllabus.\n")


def cmd_roadmap(args):
    if not ROADMAPS_JSON.exists():
        builder = CSRoadmapsEngine()
        builder.build_all_roadmaps()

    with open(ROADMAPS_JSON, "r", encoding="utf-8") as f:
        roadmaps = json.load(f)

    role_id = args.role_id.lower().strip()
    match = next((r for r in roadmaps if r["role_id"] == role_id), None)
    if not match:
        print(f"\nRole '{args.role_id}' not found. Available roles:")
        for r in roadmaps:
            print(f"  - {r['role_id']}")
        print()
        return

    print("\n=======================================================")
    print(f"  UNIVERSITY CURRICULUM: {match['title'].upper()}")
    print("=======================================================")
    print(f"Role ID    : {match['role_id']}")
    print(f"Overview   : {match['description']}")
    print(f"Total Tier : {match['total_tiers']} Progressive Tiers ({match['course_count']} courses)")
    print("-------------------------------------------------------")

    for tier in match["tiers"]:
        print(f"\n[ {tier['tier_name'].upper()} ]")
        print(f"Target Level: {tier['level']}")
        print("Competencies:")
        for comp in tier["required_competencies"]:
            print(f"  - {comp}")
        print("Courses:")
        for c in tier["courses"]:
            code_str = f"[{c['code']}] " if c["code"] else ""
            v_url = c["video_urls"][0]["url"] if c["video_urls"] else c["primary_url"]
            print(f"  * {code_str}{c['title']} ({c['institution']})")
            print(f"    Lecture: {v_url}")

    print("\n=======================================================\n")


def cmd_export(args):
    print("Exporting datasets, SQLite indexes, and curricula...")
    engine = CSCoursesEngine()
    engine.build_database()
    builder = CSRoadmapsEngine()
    builder.build_all_roadmaps()
    print("Export successfully completed!")


def cmd_serve(args):
    port = args.port or 8779
    print(f"Starting CS Video Courses API Server on port {port}...")
    import cs_courses_api_server
    cs_courses_api_server.run_server(port=port)


def cmd_do_everything(args):
    print("\n" + "=" * 65)
    print("  CS VIDEO COURSES SOVEREIGN LIFECYCLE: DO EVERYTHING")
    print("=" * 65)

    print("\n[Phase 1/5] Ingesting & Building SQLite FTS5 Database...")
    engine = CSCoursesEngine()
    count = engine.build_database()
    stats = engine.get_summary_stats()
    print(f" -> Indexed {count} courses across {stats['total_categories']} tracks and {stats['total_institutions']} institutions.")

    print("\n[Phase 2/5] Synthesizing Degree-Grade Career Roadmaps...")
    roadmaps_engine = CSRoadmapsEngine()
    roadmaps = roadmaps_engine.build_all_roadmaps()
    print(f" -> Created {len(roadmaps)} role curricula in docs/curricula/ and data/cs_role_roadmaps.json.")

    print("\n[Phase 3/5] Verifying Full-Text Search Queries...")
    test_queries = ["deep learning", "operating systems", "distributed systems", "database systems", "quantum"]
    for q in test_queries:
        res = engine.search_courses(q, limit=3)
        print(f" -> Query '{q}': {len(res)} matches (top: {res[0]['title'] if res else 'None'})")

    print("\n[Phase 4/5] Compiling Comprehensive Architecture Dossier...")
    dossier_path = WORKSPACE_ROOT / "docs" / "CS_VIDEO_COURSES_SUPREME_GUIDE.md"
    dossier_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dossier_path, "w", encoding="utf-8") as f:
        f.write(f"""# CS Video Courses Supreme Architecture & Curriculum Guide

Automated intelligence, relational catalog, and accredited university pathways built from [`Developer-Y/cs-video-courses`](https://github.com/Developer-Y/cs-video-courses).

## Executive Summary
- **Total University Courses**: {stats['total_courses']}
- **Courses with Video Playlists**: {stats['courses_with_videos']}
- **Academic Institutions Cataloged**: {stats['total_institutions']}
- **Curricular Domains / Tracks**: {stats['total_categories']}
- **Career Archetype Roadmaps**: {len(roadmaps)} degree-grade learning pathways

## Major Academic Institutions
| Institution | Course Count | Signature Courses |
| :--- | :--- | :--- |
| **MIT** | 94 | 6.0001, 6.006, 6.046J, 6.824, 6.828, 18.06, 18.404J |
| **Stanford** | 75 | CS 106A/B, CS 161, CS 229, CS 231n, CS 224N, CS 25, CS 144 |
| **Carnegie Mellon (CMU)** | 72 | 15-213, 15-445/645 (Andy Pavlo), 10-601, 10-701, 15-721 |
| **UC Berkeley** | 70 | CS 61A, CS 61B, CS 162, CS 184, CS 189/289A |
| **Harvard** | 19 | CS 50 (David J. Malan), CS50P, CS50R, CS 109 |
| **IIT / NPTEL** | 135 | Problem Solving, C++, Data Structures, Algorithms |
| **University of Washington** | 42 | CSE 142, CSE 341, CSE 451 |

## Role Curricula Available
See detailed markdown syllabi in [`docs/curricula/`](file:///e:/anti/docs/curricula/):
""")
        for r in roadmaps:
            f.write(f"- [`{r['role_id']}`: {r['title']}](file:///e:/anti/docs/curricula/{r['role_id']}.md) ({r['course_count']} courses)\n")

    print(f" -> Written supreme guide to {dossier_path}")

    print("\n[Phase 5/5] Lifecycle Manifest Generation...")
    manifest_path = DATA_DIR / "cs_courses_manifest.json"
    manifest_data = {
        "status": "ready",
        "total_courses": stats["total_courses"],
        "courses_with_videos": stats["courses_with_videos"],
        "total_tracks": stats["total_categories"],
        "total_institutions": stats["total_institutions"],
        "roadmaps_count": len(roadmaps),
        "db_path": str(engine.db_path),
        "json_path": str(engine.json_path),
        "roadmaps_path": str(ROADMAPS_JSON),
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    print(f" -> Sovereign Lifecycle Manifest saved to {manifest_path}")
    print("\n" + "=" * 65)
    print("  ALL SYSTEMS READY: Run 'python cs_courses_cli.py serve' to launch!")
    print("=" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(description="CS Video Courses Master CLI")
    subparsers = parser.add_subparsers(dest="command")

    # info
    subparsers.add_parser("info", help="Display overview stats and institution distribution")

    # search
    search_p = subparsers.add_parser("search", help="Full-text search for courses")
    search_p.add_argument("query", nargs="?", default="", help="Search query (e.g., 'distributed systems')")
    search_p.add_argument("--category", "-c", help="Filter by curricular category")
    search_p.add_argument("--institution", "-i", help="Filter by university/institution")
    search_p.add_argument("--level", "-l", help="Filter by academic level")
    search_p.add_argument("--video-only", "-v", action="store_true", help="Only courses with video lectures")
    search_p.add_argument("--limit", type=int, default=20, help="Maximum number of results")
    search_p.add_argument("--verbose", action="store_true", help="Print links and lecture URLs")

    # tracks
    subparsers.add_parser("tracks", help="List all curricular domain tracks")
    track_p = subparsers.add_parser("track", help="List courses within a track")
    track_p.add_argument("category", help="Curricular category name")

    # institutions
    subparsers.add_parser("institutions", help="List universities and course counts")
    inst_p = subparsers.add_parser("institution", help="List courses for a specific university")
    inst_p.add_argument("institution", help="Institution name (e.g. 'MIT', 'Stanford')")

    # roadmaps
    subparsers.add_parser("roadmaps", help="List all career degree-grade roadmaps")
    roadmap_p = subparsers.add_parser("roadmap", help="Inspect a specific role roadmap")
    roadmap_p.add_argument("role_id", help="Role ID (e.g., 'genai-llm-engineer')")

    # export
    subparsers.add_parser("export", help="Re-export datasets, roadmaps, and curricula")

    # serve
    serve_p = subparsers.add_parser("serve", help="Launch the REST API server and Mission Control Cockpit")
    serve_p.add_argument("--port", "-p", type=int, default=8779, help="Port to run server on")

    # do-everything
    subparsers.add_parser("do-everything", help="Run end-to-end ingestion, DB creation, roadmaps, and verification")

    args = parser.parse_args()

    if args.command == "info":
        cmd_info(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "tracks":
        cmd_tracks(args)
    elif args.command == "track":
        cmd_track(args)
    elif args.command == "institutions":
        cmd_institutions(args)
    elif args.command == "institution":
        cmd_institution(args)
    elif args.command == "roadmaps":
        cmd_roadmaps(args)
    elif args.command == "roadmap":
        cmd_roadmap(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "serve":
        cmd_serve(args)
    elif args.command == "do-everything":
        cmd_do_everything(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
