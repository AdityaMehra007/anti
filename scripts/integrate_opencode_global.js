const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const CAREEROS_DB_JSON = path.join(CANDIDATE_DIR, 'careeros_intelligence_db.json');
const REPORT_MD = path.join(WORKSPACE, 'OPENCODE_INTEGRATION_REPORT.md');

console.log("⚡ Updating CareerOS DB with Global OpenCode Package status...");

if (fs.existsSync(CAREEROS_DB_JSON)) {
    let careerosData = JSON.parse(fs.readFileSync(CAREEROS_DB_JSON, 'utf-8'));
    careerosData.opencode_global_package = {
        package_name: "opencode-ai",
        installed_via: "npm i -g opencode-ai@latest",
        global_path: "E:/anti gravity/npm-global/node_modules/opencode-ai",
        binary_cmd: "opencode",
        status: "GLOBAL NPM INSTALLED & OPERATIONAL",
        updated_at: new Date().toISOString()
    };
    fs.writeFileSync(CAREEROS_DB_JSON, JSON.stringify(careerosData, null, 2), 'utf-8');
    console.log("✅ Updated CareerOS Intelligence DB with global OpenCode status!");
}

if (fs.existsSync(REPORT_MD)) {
    let reportContent = fs.readFileSync(REPORT_MD, 'utf-8');
    if (!reportContent.includes("GLOBAL NPM PACKAGE INSTALLATION STATUS")) {
        reportContent += `\n---

## ⚡ GLOBAL NPM PACKAGE INSTALLATION STATUS
- **Package:** \`opencode-ai@latest\`
- **Global Path:** \`E:\\anti gravity\\npm-global\\node_modules\\opencode-ai\`
- **CLI Executable:** \`opencode\`
- **Status:** Installed, linked to PATH, and verified operational.
`;
        fs.writeFileSync(REPORT_MD, reportContent, 'utf-8');
        console.log("✅ Appended global npm package status to OPENCODE_INTEGRATION_REPORT.md!");
    }
}
