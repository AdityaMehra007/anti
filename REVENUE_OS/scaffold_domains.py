import os
from pathlib import Path

root = Path("e:/anti/REVENUE_OS")
dirs = [
    "01_COMMAND_CENTER", "02_REVENUE", "03_MARKET", "04_LEADS", "05_CRM",
    "06_SALES", "07_OFFERS", "08_PRODUCTS", "09_CONTENT", "10_SEO",
    "11_PARTNERS", "12_AFFILIATES", "13_FINANCE", "14_AI_AGENTS",
    "15_AUTOMATIONS", "16_CUSTOMERS", "17_ANALYTICS", "18_RISK",
    "19_KNOWLEDGE", "20_FOUNDER_OS", "21_FUTURE", "22_COMPLIANCE", "23_SETTINGS",
    "database", "web"
]

for d in dirs:
    p = root / d
    p.mkdir(parents=True, exist_ok=True)
    init_file = p / "__init__.py"
    if not init_file.exists():
        init_file.write_text(f'"""Package for {d}."""\n', encoding="utf-8")
    readme_file = p / "README.md"
    if not readme_file.exists():
        readme_file.write_text(f"# {d}\n\nDomain component of REVENUE OS.\n", encoding="utf-8")

print("23 domain directories + database + web scaffolded successfully.")
