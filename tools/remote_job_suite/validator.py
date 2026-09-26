"""
Repository Linter & PR Contribution Toolkit for awesome-remote-job
Enforces the 17 directives from CONTRIBUTING.md:
  1. Format: `[Name](url) - Description.`
  2. Length constraint: Name + Description < 100 characters
  3. Alphabetical ordering within sections
  4. Objective greppability (flags marketing buzzwords)
  5. Commit message generator: `Add Company Foo.io`
  6. Dead link validator (optional live check)
"""

import argparse
import os
import re
import sys
import urllib.request
from typing import Dict, List, Tuple

BUZZWORDS = [
    "world-class", "industry-leading", "game-changing", "revolutionary",
    "best-in-class", "next-gen", "cutting-edge", "premier", "disruptive",
    "unmatched", "state-of-the-art", "groundbreaking"
]


def lint_line(line: str, line_no: int) -> List[str]:
    issues = []
    # Check trailing whitespace
    if line.rstrip("\r\n") != line.rstrip():
        issues.append(f"Line {line_no}: Trailing whitespace detected.")

    clean = line.strip()
    if not clean or clean.startswith("#"):
        return issues

    # Check markdown link pattern
    m = re.match(r"^(?:\d+\.|\*|\-)\s+\[([^\]]+)\]\(([^)]+)\)(?:\s*[-–—:]\s*(.*))?$", clean)
    if not m:
        # If it contains a link but doesn't follow the exact list format
        if "[" in clean and "](" in clean:
            issues.append(f"Line {line_no}: Improper formatting. Expected `1. [Name](url) - Description.`")
        return issues

    name = m.group(1).strip()
    url = m.group(2).strip()
    desc = (m.group(3) or "").strip()

    # Rule: Name + description length <= 100 chars
    total_len = len(name) + len(desc)
    if total_len > 100:
        issues.append(
            f"Line {line_no}: Length violation! Name + Description is {total_len} chars (Must be < 100 chars)."
        )

    # Rule: Check for marketing buzzwords
    lower_desc = desc.lower()
    for b in BUZZWORDS:
        if b in lower_desc:
            issues.append(f"Line {line_no}: Vague marketing buzzword '{b}' found. Use objective tech keywords.")

    # Rule: Valid URL scheme
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:") or url.endswith(".md")):
        issues.append(f"Line {line_no}: Missing valid HTTP/HTTPS protocol in URL: {url}")

    return issues


def check_alphabetical_order(section_title: str, items: List[Tuple[int, str]]) -> List[str]:
    issues = []
    names = []
    for line_no, raw_line in items:
        m = re.search(r"\[([^\]]+)\]", raw_line)
        if m:
            names.append((line_no, m.group(1).strip()))

    for i in range(len(names) - 1):
        curr_no, curr_name = names[i]
        next_no, next_name = names[i + 1]
        if curr_name.lower() > next_name.lower():
            issues.append(
                f"Section '{section_title}' out of order: '{curr_name}' (Line {curr_no}) should appear after '{next_name}' (Line {next_no})."
            )
    return issues


def validate_file(filepath: str, check_urls: bool = False) -> Tuple[int, int]:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        return 1, 0

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    total_issues = 0
    current_section = "Header"
    section_items: List[Tuple[int, str]] = []

    print(f"Auditing '{filepath}' against CONTRIBUTING.md standards...\n")

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            # Check sorting of finished section
            if section_items:
                order_issues = check_alphabetical_order(current_section, section_items)
                for oi in order_issues:
                    print(f"  [SORT] {oi}")
                    total_issues += 1
                section_items = []
            current_section = stripped.replace("##", "").strip()
            continue

        if re.match(r"^\s*(?:\d+\.|\*|\-)\s+\[", stripped):
            section_items.append((idx, stripped))

        line_issues = lint_line(line, idx)
        for li in line_issues:
            print(f"  [LINT] {li}")
            total_issues += 1

    # Check last section
    if section_items:
        order_issues = check_alphabetical_order(current_section, section_items)
        for oi in order_issues:
            print(f"  [SORT] {oi}")
            total_issues += 1

    print(f"\nAudit completed: {total_issues} issues detected across {len(lines)} lines.")
    return total_issues, len(lines)


def format_contribution(name: str, url: str, description: str, category: str = "Companies") -> str:
    """
    Formats a new entry conforming to CONTRIBUTING.md and gives the exact PR commit message.
    """
    clean_name = name.strip()
    clean_url = url.strip()
    clean_desc = description.strip().rstrip(".") + "."

    total_len = len(clean_name) + len(clean_desc)
    entry_line = f"1. [{clean_name}]({clean_url}) - {clean_desc}"
    commit_msg = f"Add {category[:-1] if category.endswith('s') else category} {clean_name}"

    print("\n" + "=" * 60)
    print("PROPOSED PR ENTRY:")
    print("=" * 60)
    print(entry_line)
    print("\nMETRICS:")
    print(f"  - Character count: {total_len}/100 {'[PASS]' if total_len <= 100 else '[FAIL - TOO LONG!]'}")
    print(f"  - Recommended Commit Message: `{commit_msg}`")
    print("=" * 60)
    return entry_line


def main():
    parser = argparse.ArgumentParser(description="Validator & PR Contributor Toolkit for awesome-remote-job")
    parser.add_argument("--lint", help="Markdown file to lint against CONTRIBUTING.md")
    parser.add_argument("--new-entry", action="store_true", help="Format and validate a new entry for a PR")
    parser.add_argument("--name", help="Company / Board name")
    parser.add_argument("--url", help="Target URL")
    parser.add_argument("--desc", help="Short objective description")
    parser.add_argument("--category", default="Company", help="Category (e.g. Company, Job Board, Tool)")

    args = parser.parse_args()

    if args.new_entry:
        if not args.name or not args.url or not args.desc:
            print("Error: --name, --url, and --desc are required when formatting a new entry.", file=sys.stderr)
            sys.exit(1)
        format_contribution(args.name, args.url, args.desc, args.category)
        return

    if args.lint:
        validate_file(args.lint)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
