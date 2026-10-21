#!/usr/bin/env python3
"""
test_dossier_compilation.py - Unit Test Suite for Enterprise Dossier Document Compiler
======================================================================================
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from scripts.compile_enterprise_dossier_docs import (
    create_resume_docx,
    create_cover_letter_docx,
    create_html_files
)

class TestDossierCompilation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.sample_manifest = {
            "docket_id": "TEST-DOCKET-001",
            "company": "DeepMind Technologies",
            "role_title": "AI Systems Analyst",
            "location": "London / Remote",
            "ats_score_pct": 95.0,
            "matched_skills": ["Python", "FastAPI", "SQL", "Agentic Systems"],
            "candidate": {
                "name": "Aditya Mehra",
                "email": "adityamehra799@gmail.com",
                "phone": "+91 70034 56624",
                "location": "Bengaluru, Karnataka, India",
                "linkedin": "https://www.linkedin.com/in/adityamehra07",
                "degree": "BBA International Business",
                "institution": "Dayananda Sagar University (DSU), Bengaluru"
            }
        }
        self.sample_resume_md = "# Aditya Mehra\nResume Content"
        self.sample_cover_md = "# Cover Letter\nLetter Content"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_resume_docx(self):
        docx_path = create_resume_docx(self.temp_dir, self.sample_manifest, self.sample_resume_md)
        self.assertTrue(docx_path.exists())
        self.assertEqual(docx_path.name, "ATS_RESUME.docx")
        self.assertGreater(docx_path.stat().st_size, 1000)

    def test_create_cover_letter_docx(self):
        docx_path = create_cover_letter_docx(self.temp_dir, self.sample_manifest, self.sample_cover_md)
        self.assertTrue(docx_path.exists())
        self.assertEqual(docx_path.name, "COVER_LETTER.docx")
        self.assertGreater(docx_path.stat().st_size, 1000)

    def test_create_html_files(self):
        create_html_files(self.temp_dir, self.sample_manifest)
        res_html = self.temp_dir / "RESUME.html"
        cov_html = self.temp_dir / "COVER_LETTER.html"

        self.assertTrue(res_html.exists())
        self.assertTrue(cov_html.exists())

        res_content = res_html.read_text(encoding="utf-8")
        self.assertIn("Aditya Mehra", res_content)
        self.assertIn("DeepMind Technologies", res_content)
        self.assertIn("AI Systems Analyst", res_content)
        self.assertIn("95.0%", res_content)

        cov_content = cov_html.read_text(encoding="utf-8")
        self.assertIn("Dear Hiring Team at DeepMind Technologies", cov_content)
        self.assertIn("Dayananda Sagar University", cov_content)

if __name__ == "__main__":
    unittest.main()
