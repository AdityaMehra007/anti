const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const DOCS_DIR = path.join(WORKSPACE, 'docs');

if (!fs.existsSync(DOCS_DIR)) {
    fs.mkdirSync(DOCS_DIR, { recursive: true });
}

console.log("📚 PHASE 3: Generating Full OmniSystem Documentation Hierarchy (/docs)...");

const docFiles = [
    {
        filename: "architecture.md",
        title: "ANTIGRAVITY OMNISYSTEM ARCHITECTURE",
        content: `## 🌐 Architecture Topology
Command Center ➔ Master Orchestrator ➔ (Planning | Intelligence | Execution) ➔ Tool Fabric ➔ Data + Memory ➔ Observability ➔ Self-Improvement.`
    },
    {
        filename: "agents.md",
        title: "22 SPECIALIST AGENTS & CEO ORCHESTRATOR REGISTRY",
        content: `## 🤖 22 Domain Specialist Agents
1. System Architect, 2. Software Engineer, 3. Debugger, 4. QA Engineer, 5. Security Engineer, 6. Researcher, 7. Web Intelligence, 8. Data Engineer, 9. Database Engineer, 10. Analytics Agent, 11. Business Intelligence, 12. Market Intelligence, 13. Career Intelligence, 14. Design Agent, 15. Product Manager, 16. Documentation Agent, 17. Automation Engineer, 18. DevOps Engineer, 19. Observability Engineer, 20. Optimization Agent, 21. Security Auditor, 22. Final Reviewer.`
    },
    {
        filename: "tools.md",
        title: "TOOL ROUTER & EXECUTION CAPABILITIES",
        content: `## 🛠️ Tool Fabric Router
Selection policy: Smallest sufficient tool set with strict permission checking.`
    },
    {
        filename: "mcp.md",
        title: "MODEL CONTEXT PROTOCOL (MCP) INTEGRATION",
        content: `## 🔌 Registered MCP Servers
mcp-filesystem, mcp-browser, mcp-openclaw, mcp-openclaude, mcp-github, mcp-postgres, mcp-figma.`
    },
    {
        filename: "plugins.md",
        title: "PLUGIN MANAGER & 9 OMNI-PLUGINS",
        content: `## 🔌 9 Custom Omni-Plugins
OMNI-RESEARCH, OMNI-DATA, OMNI-CODE, OMNI-BUSINESS, OMNI-CAREER, OMNI-AUTOMATION, OMNI-ANALYTICS, OMNI-SECURITY, OMNI-OPS.`
    },
    {
        filename: "skills.md",
        title: "SKILLS LIBRARY & SPECIFICATIONS",
        content: `## 🎯 Reusable Skills Catalog
Standardized YAML frontmatter with input/output validation schemas.`
    },
    {
        filename: "workflows.md",
        title: "WORKFLOW AUTOMATION ENGINE",
        content: `## ⚡ Workflow Pipeline
TRIGGER ➔ PLAN ➔ AGENTS ➔ DATA ➔ ACTIONS ➔ VERIFICATION ➔ OUTPUT ➔ LOGGING.`
    },
    {
        filename: "security.md",
        title: "SECURITY GOVERNANCE & 6 PERMISSION TIERS",
        content: `## 🛡️ Permission Levels
Level 0 Read-Only to Level 5 Destructive with mandatory Human Approval Checkpoints.`
    },
    {
        filename: "data-model.md",
        title: "CANONICAL RELATIONAL DATA MODEL (3NF)",
        content: `## 📊 Canonical Schema
Entities: Companies, Roles, Jobs, Skills, Locations, Events, Sources, Observations.`
    },
    {
        filename: "troubleshooting.md",
        title: "DIAGNOSTICS & TROUBLESHOOTING GUIDE",
        content: `## 🔍 Diagnostics
Step-by-step resolution for API rate limits, tool dispatch errors, and agent timeouts.`
    },
    {
        filename: "recovery.md",
        title: "BACKUP & RECOVERY STRATEGY",
        content: `## 🔄 Disaster Recovery
State snapshots, manifest backups, and fast restoration sequences.`
    },
    {
        filename: "operations.md",
        title: "SYSTEM OPERATIONS & BOOT SEQUENCE",
        content: `## ⚡ Boot & Shutdown Sequences
Automated environment validation, MCP health check, and queue resumption.`
    },
    {
        filename: "changelog.md",
        title: "SYSTEM CHANGELOG",
        content: `## 📝 System Change Log
- **v23.5 Enterprise**: Built 22 Specialist Agents, 9 Omni-Plugins, 13 Test Suites & Master Command Center UI.`
    }
];

docFiles.forEach(doc => {
    const filePath = path.join(DOCS_DIR, doc.filename);
    const markdown = `# ${doc.title}\n\n**Generated for:** Antigravity OmniSystem Engine (v23.5)\n**Timestamp:** ${new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })} IST\n\n---\n\n${doc.content}\n`;
    fs.writeFileSync(filePath, markdown, 'utf-8');
});

console.log(`✅ All 13 Documentation files written to: ${DOCS_DIR}`);
