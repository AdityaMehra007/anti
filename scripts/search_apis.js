const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'public_apis_master.json');
if (!fs.existsSync(dbPath)) {
  console.error('Error: public_apis_master.json not found. Run parse_public_apis.js first.');
  process.exit(1);
}

const apis = JSON.parse(fs.readFileSync(dbPath, 'utf-8'));
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
Usage:
  node search_apis.js <query>                 Search name & description
  node search_apis.js --cat <category>        Filter by category
  node search_apis.js --no-auth               Only show APIs requiring No auth
  node search_apis.js --cors                  Only show APIs with CORS Yes
  node search_apis.js --list-categories       List all 52 categories and API counts

Examples:
  node search_apis.js job
  node search_apis.js --cat Finance
  node search_apis.js weather --no-auth
  node search_apis.js scraping
`);
  process.exit(0);
}

if (args.includes('--list-categories')) {
  const catStats = {};
  apis.forEach(a => catStats[a.category] = (catStats[a.category] || 0) + 1);
  console.log('\n=== Available Categories ===');
  Object.entries(catStats).sort((a,b) => b[1] - a[1]).forEach(([cat, count]) => {
    console.log(`  • ${cat.padEnd(35)} : ${count} APIs`);
  });
  console.log(`\nTotal: ${apis.length} APIs across ${Object.keys(catStats).length} categories.\n`);
  process.exit(0);
}

let query = '';
let categoryFilter = '';
let noAuthOnly = false;
let corsOnly = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--cat' && args[i + 1]) {
    categoryFilter = args[i + 1].toLowerCase();
    i++;
  } else if (args[i] === '--no-auth') {
    noAuthOnly = true;
  } else if (args[i] === '--cors') {
    corsOnly = true;
  } else if (!args[i].startsWith('--')) {
    query = args[i].toLowerCase();
  }
}

const results = apis.filter(api => {
  if (categoryFilter && !api.category.toLowerCase().includes(categoryFilter)) return false;
  if (noAuthOnly && api.auth.toLowerCase() !== 'no') return false;
  if (corsOnly && api.cors.toLowerCase() !== 'yes') return false;
  if (query) {
    const text = `${api.name} ${api.description} ${api.category}`.toLowerCase();
    return text.includes(query);
  }
  return true;
});

console.log(`\nFound ${results.length} APIs matching your criteria:\n`);
results.slice(0, 50).forEach((api, index) => {
  console.log(`${(index + 1).toString().padStart(2)}. [${api.name}] (${api.category})`);
  console.log(`    URL:         ${api.url}`);
  console.log(`    Description: ${api.description}`);
  console.log(`    Auth:        ${api.auth} | HTTPS: ${api.https} | CORS: ${api.cors}\n`);
});

if (results.length > 50) {
  console.log(`... and ${results.length - 50} more. Refine search with specific keywords or category filter.`);
}
