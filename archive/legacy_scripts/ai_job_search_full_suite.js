const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const MODULES_DIR = path.join(WORKSPACE, 'external_skills', 'ai-job-search', '.claude', 'skills', 'job-application-assistant');
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const OUTPUT_JSON = path.join(CANDIDATE_DIR, 'ai_job_search_9_modules.json');
const REPORT_MD = path.join(WORKSPACE, 'AI_JOB_SEARCH_9_MODULES_REPORT.md');

const modulesList = [
    { code: "01", name: "Candidate Profile", file: "01-candidate-profile.md" },
    { code: "02", name: "Behavioral STAR Profile", file: "02-behavioral-profile.md" },
    { code: "03", name: "Writing Style Guardrails", file: "03-writing-style.md" },
    { code: "04", name: "Job Evaluation Engine", file: "04-job-evaluation.md" },
    { code: "05", name: "ATS CV Templates", file: "05-cv-templates.md" },
    { code: "06", name: "Cover Letter Engine", file: "06-cover-letter-templates.md" },
    { code: "07", name: "Interview Prep & Twin", file: "07-interview-prep.md" },
    { code: "08", name: "Application Form Shortcuts", file: "08-application-forms.md" },
    { code: "09", name: "Company Web Research", file: "09-web-research.md" }
];

function processModules() {
    console.log("🚀 Processing 9 Core Career Guidance Modules from MadsLorentzen/ai-job-search...");

    const processedData = {
        framework: "MadsLorentzen/ai-job-search (Integrated)",
        processed_at: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }),
        candidate: "Aditya Mehra (BBA International Business '26)",
        modules: []
    };

    let reportMarkdown = `# MADS LORENTZEN 9-MODULE AI JOB SEARCH MASTER REPORT
**Target Candidate:** Aditya Mehra | BBA International Business, DSU Bangalore '26  
**Source Repository:** https://github.com/MadsLorentzen/ai-job-search.git  
**Integration Version:** V16-9-MODULE-FULL-SUITE  

---

`;

    modulesList.forEach(mod => {
        const filePath = path.join(MODULES_DIR, mod.file);
        let content = "";
        let size = 0;

        if (fs.existsSync(filePath)) {
            content = fs.readFileSync(filePath, 'utf-8');
            size = content.length;
            console.log(`  ✔ Module ${mod.code} loaded: ${mod.name} (${size} bytes)`);
        } else {
            console.warn(`  ⚠️ Module ${mod.code} file not found: ${filePath}`);
        }

        processedData.modules.push({
            code: mod.code,
            name: mod.name,
            file: mod.file,
            byte_size: size,
            status: fs.existsSync(filePath) ? "LOADED" : "MISSING"
        });

        reportMarkdown += `## Module ${mod.code}: ${mod.name} (\`${mod.file}\`)\n\n`;
        reportMarkdown += `**Status:** 🟢 INTEGRATED (${size} bytes)\n\n`;
        reportMarkdown += `\`\`\`markdown\n${content.substring(0, 400)}...\n\`\`\`\n\n---\n\n`;
    });

    fs.writeFileSync(OUTPUT_JSON, JSON.stringify(processedData, null, 2), 'utf-8');
    fs.writeFileSync(REPORT_MD, reportMarkdown, 'utf-8');

    console.log(`✅ 9-Module JSON written to: ${OUTPUT_JSON}`);
    console.log(`✅ Master 9-Module Report written to: ${REPORT_MD}`);
}

processModules();
