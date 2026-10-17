import os

target_dirs = [
    r"E:\Temp\amehr\adityamehra007_site",
    r"E:\Temp\amehr\AdityaMehra007_profile",
    r"e:\anti\resumes",
    r"e:\anti\portfolio",
]

total_cleaned = 0

for d in target_dirs:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith((".html", ".md", ".txt", ".json", ".py", ".xml")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                    if "ashishiash007@gmail.com" in text:
                        new_text = text.replace("ashishiash007@gmail.com", "adityamehra007@gmail.com")
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        total_cleaned += 1
                        print(f"Standardized email in: {filepath}")
                except Exception as e:
                    pass

# Also check root md/html files in e:\anti
for f in os.listdir(r"e:\anti"):
    if f.endswith((".html", ".md", ".py")):
        filepath = os.path.join(r"e:\anti", f)
        try:
            with open(filepath, "r", encoding="utf-8") as fl:
                text = fl.read()
            if "ashishiash007@gmail.com" in text:
                new_text = text.replace("ashishiash007@gmail.com", "adityamehra007@gmail.com")
                with open(filepath, "w", encoding="utf-8") as fl:
                    fl.write(new_text)
                total_cleaned += 1
                print(f"Standardized email in: {filepath}")
        except Exception:
            pass

print(f"\nDone! Successfully standardized {total_cleaned} files to adityamehra007@gmail.com.")
