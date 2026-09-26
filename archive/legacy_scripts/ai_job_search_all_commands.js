const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const COMMANDS_DIR = path.join(WORKSPACE, 'external_skills', 'ai-job-search', '.claude', 'commands');
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const OUTPUT_JSON = path.join(CANDIDATE_DIR, 'ai_job_search_all_commands.json');

const commandsMap = [
    { cmd: "/apply", file: "apply.md", desc: "Drafter-Reviewer application pipeline (CV + Cover Letter)" },
    { cmd: "/setup", file: "setup.md", desc: "Onboarding, candidate documents, CV import" },
    { cmd: "/expand", file: "expand.md", desc: "Competency enrichment from documents and online presence" },
    { cmd: "/add-template", file: "add-template.md", desc: "Register custom templates (LaTeX, Typst, HTML)" },
    { cmd: "/add-portal", file: "add-portal.md", desc: "Generate a job-portal search skill for your market" },
    { cmd: "/rank", file: "rank.md", desc: "Triage scraped jobs into a ranked shortlist" },
    { cmd: "/outcome", file: "outcome.md", desc: "Record application results and archive materials" },
    { cmd: "/gmail-sync", file: "gmail-sync.md", desc: "Auto-detect application status from Gmail" },
    { cmd: "/interview", file: "interview.md", desc: "Stage-specific prep pack + mock interview" },
    { cmd: "/html-report", file: "html-report.md", desc: "Generate application tracker dashboard" },
    { cmd: "/notion-sync", file: "notion-sync.md", desc: "One-way pipeline view in a Notion database" },
    { cmd: "/reset", file: "reset.md", desc: "Wipe profile data or documents folder safely" }
];

function processAllCommands() {
    console.log("⚡ Processing All 12 Slash-Commands from MadsLorentzen/ai-job-search...");

    const commandResults = {
        system: "CAREER OS V17 — Slash Command Suite",
        total_commands: commandsMap.length,
        commands: []
    };

    commandsMap.forEach(item => {
        const filePath = path.join(COMMANDS_DIR, item.file);
        let exists = fs.existsSync(filePath);
        let byteSize = exists ? fs.readFileSync(filePath, 'utf-8').length : 0;

        console.log(`  ✔ ${item.cmd} (${item.file}) - ${byteSize} bytes`);

        commandResults.commands.push({
            command: item.cmd,
            file: item.file,
            description: item.desc,
            byte_size: byteSize,
            status: exists ? "ACTIVE" : "MISSING"
        });
    });

    fs.writeFileSync(OUTPUT_JSON, JSON.stringify(commandResults, null, 2), 'utf-8');
    console.log(`✅ Slash command suite JSON written to: ${OUTPUT_JSON}`);
}

processAllCommands();
