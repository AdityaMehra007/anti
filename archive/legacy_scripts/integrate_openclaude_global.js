const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const CAREEROS_DB_JSON = path.join(CANDIDATE_DIR, 'careeros_intelligence_db.json');
const REPORT_MD = path.join(WORKSPACE, 'OPENCLAUDE_INTEGRATION_REPORT.md');

console.log("⚡ Updating CareerOS DB with Global OpenClaude Package (v0.29.1)...");

if (fs.existsSync(CAREEROS_DB_JSON)) {
    let careerosData = JSON.parse(fs.readFileSync(CAREEROS_DB_JSON, 'utf-8'));
    careerosData.openclaude_global_package = {
        package_name: "@gitlawb/openclaude",
        installed_version: "0.29.1",
        global_path: "E:/anti gravity/npm-global/node_modules/@gitlawb/openclaude",
        status: "GLOBAL NPM INSTALLED & OPERATIONAL"
    };
    fs.writeFileSync(CAREEROS_DB_JSON, JSON.stringify(careerosData, null, 2), 'utf-8');
    console.log("✅ Updated CareerOS Intelligence DB with global OpenClaude v0.29.1 status!");
}

let reportContent = fs.readFileSync(REPORT_MD, 'utf-8');
if (!reportContent.includes("GLOBAL NPM PACKAGE")) {
    reportContent += `\n---

## ⚡ GLOBAL NPM PACKAGE INSTALLATION STATUS
- **Package:** \`@gitlawb/openclaude@latest\`
- **Installed Version:** **v0.29.1**
- **Global Path:** \`E:\\anti gravity\\npm-global\\node_modules\\@gitlawb\\openclaude\`
- **CLI Executable:** Verified operational via Node entrypoint (\`0.29.1 (OpenClaude)\`).
`;
    fs.writeFileSync(REPORT_MD, reportContent, 'utf-8');
    console.log("✅ Appended global npm package status to OPENCLAUDE_INTEGRATION_REPORT.md!");
}
