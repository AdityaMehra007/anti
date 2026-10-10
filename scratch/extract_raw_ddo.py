with open("scratch/lowes_page.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("phApp.ddo =")
if pos != -1:
    end_script = html.find("</script>", pos)
    print(f"ddo script length: {end_script - pos}")
    snippet = html[pos:end_script]
    # save snippet
    with open("scratch/lowes_ddo_raw.js", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Saved raw ddo to scratch/lowes_ddo_raw.js")
