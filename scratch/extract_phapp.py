with open("scratch/lowes_page.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find('var phApp = phApp ||')
if pos != -1:
    snippet = html[pos:pos+3000]
    print(snippet)
    with open("scratch/lowes_phapp_snippet.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
