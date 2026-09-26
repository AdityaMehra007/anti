#!/usr/bin/env python3
"""
========================================================================================
HARVARD ATS RESUME PDF BATCH COMPILER (PLAYWRIGHT CHROMIUM)
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Compiles pixel-perfect, 1-page Harvard ATS resumes into printable .pdf files:
  1. Master Bangalore Operations Resume (Aditya_Mehra_Master_ATS_Resume_Bangalore.pdf)
  2. Specialized Track Resumes (Operations, EXIM/SCM, AI Data, Brand/Ground Ops)
  3. Top Company Requisition Resumes (Accenture, Puma, Amazon, Goldman Sachs, etc.)
Outputs to: e:/anti/resumes_pdf/
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT_DIR / "resumes_pdf"
PACKAGES_DIR = ROOT_DIR / "applications_generated" / "bangalore_61_packages"

async def compile_resumes():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 80)
    print("  COMPILING HARVARD ATS RESUMES TO VECTOR PDF")
    print(f"  Target Directory: {PDF_DIR}")
    print("=" * 80)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Compile from 61 packages where resume_ats_1page.html exists
        pkg_folders = sorted(list(PACKAGES_DIR.glob("BLR-JOB-*")))
        compiled = 0

        # Master copy from first top package
        if pkg_folders:
            top_pkg = pkg_folders[0]
            top_html = top_pkg / "resume_ats_1page.html"
            if top_html.exists():
                master_pdf = PDF_DIR / "Aditya_Mehra_Master_ATS_Resume_Bangalore.pdf"
                await page.goto(top_html.as_uri())
                await page.pdf(
                    path=str(master_pdf),
                    format="A4",
                    print_background=True,
                    margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
                )
                print(f"[✓] Compiled Master Agency Resume -> {master_pdf.name} ({master_pdf.stat().st_size} bytes)")
                compiled += 1

        # Specific Priority Packages
        for pkg in pkg_folders[:12]:
            html_file = pkg / "resume_ats_1page.html"
            if html_file.exists():
                company_slug = pkg.name.replace("BLR-JOB-", "")
                pdf_target = PDF_DIR / f"Aditya_Mehra_Resume_{company_slug}.pdf"
                await page.goto(html_file.as_uri())
                await page.pdf(
                    path=str(pdf_target),
                    format="A4",
                    print_background=True,
                    margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
                )
                # Also save inside the package folder for easy drag-drop
                pkg_pdf = pkg / f"Aditya_Mehra_Resume_{company_slug}.pdf"
                await page.pdf(
                    path=str(pkg_pdf),
                    format="A4",
                    print_background=True,
                    margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
                )
                print(f"[✓] Compiled {pkg.name} -> {pdf_target.name}")
                compiled += 1

        await browser.close()

    print("=" * 80)
    print(f"[✓] Successfully compiled {compiled} Harvard ATS PDF resumes in: {PDF_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(compile_resumes())
