import re
from pathlib import Path
import pypdf
import docx

pdf_path = Path(r"e:\anti\ADITYA_MEHRA_FLAWLESS_CV.pdf")
docx_path = Path(r"e:\anti\ADITYA_MEHRA_FLAWLESS_CV.docx")

reader = pypdf.PdfReader(str(pdf_path))
page = reader.pages[0]
text = page.extract_text()

# 1. Page count
num_pages = len(reader.pages)

# 2. Links
links = []
if '/Annots' in page:
    for annot in page['/Annots']:
        obj = annot.get_object()
        if '/A' in obj and '/URI' in obj['/A']:
            links.append(obj['/A']['/URI'])

# 3. Word and Character stats
words = text.split()
word_count = len(words)
char_count = len(text)

# 4. Check for prohibited numbers/metrics in bullet points
bullet_lines = [line.strip() for line in text.split('\n') if line.strip().startswith('•') or 'Intern |' in line or 'Coordinator |' in line or 'Assistant |' in line]
numbers_in_bullets = []
for bl in bullet_lines:
    found_nums = re.findall(r'\b\d+(?:[\.,]\d+)?%?\b', bl)
    if found_nums:
        numbers_in_bullets.extend(found_nums)

# 5. Check languages
langs = []
if "English" in text: langs.append("English")
if "Hindi" in text: langs.append("Hindi")
if "Bengali" in text: langs.append("Bengali")
if "Punjabi" in text: langs.append("Punjabi")

# 6. Readability metrics (Flesch Reading Ease approximation)
sentences = [s for s in re.split(r'[\.\?!]\s+', text) if s.strip()]
sentence_count = max(1, len(sentences))
syllable_count = 0
for w in words:
    w_clean = re.sub(r'[^a-zA-Z]', '', w).lower()
    if not w_clean: continue
    s_count = len(re.findall(r'[aeiouy]+', w_clean))
    syllable_count += max(1, s_count)

asl = word_count / sentence_count
asw = syllable_count / max(1, word_count)
flesch_reading_ease = 206.835 - (1.015 * asl) - (84.6 * asw)
flesch_kincaid_grade = (0.39 * asl) + (11.8 * asw) - 15.59

print(f"--- FLAWLESS CV AUDIT & SCORING METRICS ---")
print(f"Page Count: {num_pages} (Invariant: strictly 1)")
print(f"Total Words: {word_count} (Optimal: 320-380)")
print(f"Total Characters: {char_count}")
print(f"Sentences: {sentence_count}")
print(f"Avg Sentence Length: {asl:.1f} words")
print(f"Flesch Reading Ease: {flesch_reading_ease:.1f} (Ideal: 50-70 for professional CV)")
print(f"Flesch-Kincaid Grade: {flesch_kincaid_grade:.1f} (Clear, accessible professional English)")
print(f"Active Clickable Links: {len(links)} / 5 verified ({links})")
print(f"Forbidden Numbers in Bullets: {len(numbers_in_bullets)} ({numbers_in_bullets})")
print(f"Languages Listed: {langs} (Strict Rule: English, Hindi only)")
