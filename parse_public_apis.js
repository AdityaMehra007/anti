const fs = require('fs');
const path = require('path');

const readmePath = path.join(__dirname, 'public-apis', 'README.md');
const masterOutputPath = path.join(__dirname, 'public_apis_master.json');
const catOutputPath = path.join(__dirname, 'public_apis_categories.json');

console.log('Reading README from:', readmePath);
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

fs.writeFileSync(masterOutputPath, JSON.stringify(apis, null, 2), 'utf-8');
console.log(`Successfully parsed ${apis.length} APIs across categories into ${masterOutputPath}`);

const catStats = {};
apis.forEach(api => {
  catStats[api.category] = (catStats[api.category] || 0) + 1;
});

fs.writeFileSync(catOutputPath, JSON.stringify(catStats, null, 2), 'utf-8');
console.log(`Saved category stats (${Object.keys(catStats).length} categories) to ${catOutputPath}`);
