import subprocess
import json
import base64

repos = [
    "PROJECT-AURELION-THE-LEGACY-OILWORKS-INTELLIGENCE-PLATFORM",
    "Moneyverse",
    "AI-Executive-OS",
    "Every-Toy.-Every-Imagination.-One-Universe.",
    "ARTISTRY-ONE-The-Grand-Digital-Atelier",
    "Numisma-Elite",
    "GameVerse",
    "GymVerse-OS",
    "Zuno",
    "JOYVERSE",
    "cloudbite-",
    "Cvlizations"
]

def gh_api(endpoint):
    res = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True)
    if res.returncode == 0:
        return json.loads(res.stdout)
    return None

results = {}
for repo in repos:
    print(f"Inspecting {repo}...")
    repo_data = gh_api(f"repos/AdityaMehra007/{repo}")
    meta_data = gh_api(f"repos/AdityaMehra007/{repo}/contents/metadata.json")
    meta_text = ""
    if meta_data and "content" in meta_data:
        try:
            meta_text = base64.b64decode(meta_data["content"]).decode("utf-8")
        except Exception:
            pass
    
    # Check tree or contents to see what packages / screens exist
    tree = gh_api(f"repos/AdityaMehra007/{repo}/git/trees/main?recursive=1")
    key_files = []
    if tree and "tree" in tree:
        for item in tree["tree"]:
            path = item["path"]
            if path.endswith(".kt") or path.endswith("AndroidManifest.xml") or path.endswith("build.gradle.kts"):
                key_files.append(path)

    results[repo] = {
        "description": repo_data.get("description") if repo_data else None,
        "topics": repo_data.get("topics") if repo_data else [],
        "visibility": repo_data.get("visibility") if repo_data else None,
        "default_branch": repo_data.get("default_branch") if repo_data else "main",
        "metadata": meta_text,
        "key_files": key_files[:20]  # sample of files
    }

with open("data/repos_inspection.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Inspection completed. Saved to data/repos_inspection.json")
