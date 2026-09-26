const fs = require('fs');
const path = require('path');

const readmePath = path.join(__dirname, 'public-apis', 'README.md');
const outputPath = path.join(__dirname, 'public_apis_master.json');

const content = fs.readFileSync(readmePath, 'utf-8');
const lines = content.split('\n');

let currentCategory = '';
const apis = [];

for (const line of lines) {
  const trimmed = line.trim();
  if (trimmed.startsWith('### ')) {
    currentCategory = trimmed.replace('### ', '').trim();
  } else if (trimmed.startsWith('| [') && currentCategory) {
    const parts = trimmed.split('|').map(p => p.trim()).filter((_, idx) => idx > 0);
    // Format: | [Name](url) | Description | Auth | HTTPS | CORS |
    if (parts.length >= 5) {
      const nameMatch = parts[0].match(/\[([^\]]+)\]\(([^)]+)\)/);
      if (nameMatch) {
        const name = nameMatch[1];
        const url = nameMatch[2];
        const description = parts[1];
        const auth = parts[2].replace(/`/g, '') || 'No';
        const https = parts[3] || 'Unknown';
        const cors = parts[4] || 'Unknown';

        apis.push({
          name,
          url,
          description,
          auth,
          https,
          cors,
          category: currentCategory
        });
      }
    }
  }
}

fs.writeFileSync(outputPath, JSON.stringify(apis, null, 2), 'utf-8');
console.log(`Successfully parsed ${apis.length} APIs across 52 categories into ${outputPath}`);

// Also generate category summary
const catStats = {};
apis.forEach(api => {
  catStats[api.category] = (catStats[api.category] || 0) + 1;
});

const statsPath = path.join(__dirname, 'public_apis_categories.json');
fs.writeFileSync(statsPath, JSON.stringify(catStats, null, 2), 'utf-8');
console.log(`Saved category stats to ${statsPath}`);
