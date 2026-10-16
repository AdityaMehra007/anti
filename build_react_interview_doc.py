#!/usr/bin/env python3
"""
Compiles the Senior ReactJS Interview Guide into:
1. e:\anti\reports\REACT_SENIOR_INTERVIEW_GUIDE.docx
2. e:\anti\reports\REACT_SENIOR_INTERVIEW_GUIDE.pdf (via Word COM)
"""

import json
import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import win32com.client

JSON_TOP50 = Path(r"e:\anti\data\react_interview_top_50.json")
DOCX_OUT = Path(r"e:\anti\reports\REACT_SENIOR_INTERVIEW_GUIDE.docx")
PDF_OUT = Path(r"e:\anti\reports\REACT_SENIOR_INTERVIEW_GUIDE.pdf")

def build_guide():
    with open(JSON_TOP50, "r", encoding="utf-8") as f:
        questions = json.load(f)

    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.6)
        s.bottom_margin = Inches(0.6)
        s.left_margin = Inches(0.6)
        s.right_margin = Inches(0.6)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("REACT.JS SENIOR & STAFF INTERVIEW ARCHITECTURE GUIDE")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(14, 116, 144)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Curated High-Impact Conceptual, Fiber, Concurrency & Performance Questions\nDerived from sudheerj/reactjs-interview-questions")
    r_sub.font.size = Pt(9.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    for i, q in enumerate(questions, 1):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        r_num = p_q.add_run(f"#{i} [Q{q['id']}] ")
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(30, 58, 138)
        r_num.font.size = Pt(10.5)

        r_title = p_q.add_run(q['title'])
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(15, 23, 42)

        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_before = Pt(0)
        p_meta.paragraph_format.space_after = Pt(3)
        r_meta = p_meta.add_run(f"Category: {q['category']} | Level: {q['difficulty']}")
        r_meta.font.size = Pt(8.5)
        r_meta.font.italic = True
        r_meta.font.color.rgb = RGBColor(100, 116, 139)

        # Answer body summary (take first 3-4 clean paragraphs)
        clean_text = q["answer_markdown"]
        paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip() and not p.strip().startswith("```")][:3]
        for para in paragraphs:
            p_body = doc.add_paragraph()
            p_body.paragraph_format.space_after = Pt(3)
            p_body.paragraph_format.space_before = Pt(0)
            r_b = p_body.add_run(para.replace("**", "").replace("_", ""))
            r_b.font.size = Pt(9.5)

    os.makedirs(DOCX_OUT.parent, exist_ok=True)
    doc.save(str(DOCX_OUT))
    print(f"[✓] Saved Word Guide to {DOCX_OUT}")

    # Compile PDF via Word COM
    print("[+] Compiling PDF via Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        w_doc = word.Documents.Open(str(DOCX_OUT))
        pages = w_doc.ComputeStatistics(2)
        w_doc.ExportAsFixedFormat(str(PDF_OUT), 17)
        w_doc.Close()
        print(f"[✓] Successfully compiled {PDF_OUT} ({pages} pages)!")
    finally:
        word.Quit()

if __name__ == "__main__":
    build_guide()
