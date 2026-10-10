with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    html = f.read()

import json
import re

# Find the script containing "results":[
idx = html.find('"results":[')
if idx != -1:
    print("Found '\"results\":[' at index", idx)
    # let's find the start of the JSON object or script
    start = html.rfind('<script', 0, idx)
    end = html.find('</script>', idx)
    script_content = html[start:end]
    print("Script length:", len(script_content))
    with open("scratch/mp_data_script.js", "w", encoding="utf-8") as out:
        out.write(script_content)
    print("Saved scratch/mp_data_script.js")
else:
    print("Could not find '\"results\":['")
