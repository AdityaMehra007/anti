/**
 * ============================================================================
 * SHEET2PIPELINE — AI-Powered B2B Lead Enrichment & Cold Outreach Engine
 * ============================================================================
 * Version: 2.5.0 (Production Micro-SaaS Edition)
 * Engine: Google Sheets + Gemini Flash AI (1.5 Flash / 2.0 Flash / Pro)
 * Built for: B2B Founders, Agencies, SDRs, and Growth Freelancers
 * 
 * FEATURES:
 *  1. ⚡ 1-Click Sheet Setup (Auto-creates standardized headers & formatting)
 *  2. 🌐 Company Enrichment & Tech Stack Finder (Gemini AI + Live Web Scraping)
 *  3. 🎯 Prospect ICP Scoring (1-100) with strategic rationale
 *  4. 💡 Punchy 1-Line Icebreakers (Hyper-personalized, non-cringe hooks)
 *  5. ✉️ Full 3-Touch Cold Email Sequence Generator (Sub-90-word high-conversion copy)
 *  6. 📬 1-Click Gmail Draft Creator (Pushes customized emails straight to Gmail)
 *  7. ⚙️ Interactive Modern Sidebar UI for API Keys, Offers, and ICP Settings
 *  8. 🧮 Custom Formulas (=S2P_ENRICH, =S2P_ICEBREAKER, =S2P_ICP_SCORE, =S2P_EMAIL)
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// GLOBAL CONFIGURATION & CONSTANTS
// ----------------------------------------------------------------------------
const S2P_CONFIG = {
  APP_NAME: 'Sheet2Pipeline AI',
  DEFAULT_MODEL: 'gemini-1.5-flash',
  API_BASE_URL: 'https://generativelanguage.googleapis.com/v1beta/models/',
  PROP_API_KEY: 'S2P_GEMINI_API_KEY',
  PROP_MODEL: 'S2P_GEMINI_MODEL',
  PROP_OFFER: 'S2P_USER_OFFER',
  PROP_SENDER_NAME: 'S2P_SENDER_NAME',
  PROP_COMPANY: 'S2P_USER_COMPANY',
  PROP_ICP: 'S2P_TARGET_ICP',
  PROP_CTA: 'S2P_CALL_TO_ACTION'
};

// Standard Sheet Column Schema
const S2P_COLUMNS = [
  'First Name',
  'Last Name',
  'Prospect Email',
  'Job Title',
  'Company Name',
  'Website / Domain',
  'Prospect Bio / Context',
  'Company Intel & Tech Stack',
  'ICP Fit Score (1-100)',
  'Personalized Icebreaker',
  'Email Subject Line',
  'Cold Email (Touch 1)',
  'Follow-Up 1',
  'Follow-Up 2',
  'Gmail Draft Status'
];

// ----------------------------------------------------------------------------
// 1. MENU & INITIALIZATION
// ----------------------------------------------------------------------------

/**
 * Creates custom menu when the Google Sheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('⚡ Sheet2Pipeline AI')
    .addItem('🚀 1-Click Sheet Template Setup', 'setupSheetTemplate')
    .addItem('⚙️ Open Settings & AI Control Panel', 'showSidebar')
    .addSeparator()
    .addItem('🌐 Enrich Company Intel (Selected Rows)', 'menuEnrichCompany')
    .addItem('🎯 Score Prospect ICP Fit (Selected Rows)', 'menuScoreICP')
    .addItem('💡 Generate Icebreakers (Selected Rows)', 'menuGenerateIcebreakers')
    .addItem('✉️ Generate Cold Email Sequences (Selected Rows)', 'menuGenerateSequences')
    .addSeparator()
    .addItem('⚡ Run Full Pipeline on Selected Rows', 'menuRunFullPipeline')
    .addSeparator()
    .addItem('📬 Create Gmail Drafts (Selected Rows)', 'menuCreateGmailDrafts')
    .addSeparator()
    .addItem('🧪 Test Gemini API Connection', 'testGeminiConnection')
    .addItem('📖 User Guide & Quick Help', 'showHelpDialog')
    .addToUi();
}

/**
 * Initializes sheet headers, styling, and standard columns
 */
function setupSheetTemplate() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const ui = SpreadsheetApp.getUi();

  if (sheet.getLastRow() > 1) {
    const response = ui.alert(
      'Initialize Sheet Template',
      'This will insert the Sheet2Pipeline standardized header row at Row 1. Existing data will not be deleted, but Column A-O headers will be updated. Proceed?',
      ui.ButtonSet.YES_NO
    );
    if (response !== ui.Button.YES) return;
  }

  // Set headers
  const headerRange = sheet.getRange(1, 1, 1, S2P_COLUMNS.length);
  headerRange.setValues([S2P_COLUMNS]);

  // Styling
  headerRange.setBackground('#1e293b')
    .setFontColor('#ffffff')
    .setFontWeight('bold')
    .setFontFamily('Google Sans, Inter, Roboto, Arial')
    .setFontSize(10)
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle')
    .setWrap(true);

  sheet.setRowHeight(1, 40);
  sheet.setFrozenRows(1);

  // Set column widths for optimal workflow
  const widths = [110, 110, 190, 150, 150, 170, 200, 240, 130, 240, 180, 280, 220, 220, 140];
  widths.forEach((w, idx) => sheet.setColumnWidth(idx + 1, w));

  // Add a sample demo row if empty
  if (sheet.getLastRow() === 1) {
    const sampleRow = [
      'Sarah',
      'Jenkins',
      'sarah.jenkins@saasgrowthlab.io',
      'VP of Growth & Marketing',
      'SaaS Growth Lab',
      'https://saasgrowthlab.io',
      'Scaling outbound revenue and ABM for Series A/B B2B SaaS companies. Recently posted about SDR ramp times.',
      '', '', '', '', '', '', '', 'Pending'
    ];
    sheet.getRange(2, 1, 1, sampleRow.length).setValues([sampleRow]);
    sheet.getRange(2, 1, 1, sampleRow.length).setFontFamily('Google Sans, Inter, Roboto, Arial').setFontSize(10);
  }

  SpreadsheetApp.getActiveSpreadsheet().toast('Sheet2Pipeline template initialized successfully! 🚀', 'Ready', 5);
}

// ----------------------------------------------------------------------------
// 2. SIDEBAR & SETTINGS (HTML / CSS / JS EMBEDDED)
// ----------------------------------------------------------------------------

/**
 * Displays the modern Glassmorphism control panel sidebar
 */
function showSidebar() {
  const html = HtmlService.createHtmlOutput(getSidebarHtml())
    .setTitle('⚡ Sheet2Pipeline Control Panel')
    .setWidth(340);
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Returns complete responsive HTML/CSS/JS for Sidebar
 */
function getSidebarHtml() {
  const props = PropertiesService.getUserProperties();
  const currentKey = props.getProperty(S2P_CONFIG.PROP_API_KEY) || '';
  const currentModel = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;
  const currentOffer = props.getProperty(S2P_CONFIG.PROP_OFFER) || 'We build AI-powered outbound lead engines that add 15-25 qualified B2B sales meetings/month on 100% pay-on-results basis.';
  const currentSender = props.getProperty(S2P_CONFIG.PROP_SENDER_NAME) || 'Adi Mehra';
  const currentCompany = props.getProperty(S2P_CONFIG.PROP_COMPANY) || 'OutboundVelocity AI';
  const currentICP = props.getProperty(S2P_CONFIG.PROP_ICP) || 'B2B SaaS / Agency Founders, CMOs, VPs of Sales with 10-100 employees looking to scale outbound.';
  const currentCTA = props.getProperty(S2P_CONFIG.PROP_CTA) || 'Open to seeing a 3-min loom breakdown of how we did this for [Competitor]?';

  return `
<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
    body { background: #0f172a; color: #f8fafc; padding: 16px; font-size: 12px; line-height: 1.5; }
    .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 12px; border-bottom: 1px solid #334155; margin-bottom: 16px; }
    .header h2 { font-size: 15px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 6px; }
    .badge { background: #0284c7; color: white; font-size: 9px; padding: 2px 6px; border-radius: 999px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
    .card-title { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; }
    label { display: block; font-size: 11px; font-weight: 500; color: #cbd5e1; margin-bottom: 4px; }
    input, select, textarea { width: 100%; background: #0f172a; border: 1px solid #475569; border-radius: 6px; padding: 8px 10px; color: #f8fafc; font-size: 12px; margin-bottom: 8px; transition: border 0.2s; }
    input:focus, select:focus, textarea:focus { outline: none; border-color: #38bdf8; }
    textarea { resize: vertical; min-height: 54px; }
    .btn { width: 100%; padding: 9px 12px; border: none; border-radius: 6px; font-weight: 600; font-size: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: all 0.2s; margin-bottom: 6px; }
    .btn-primary { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; }
    .btn-primary:hover { opacity: 0.95; transform: translateY(-1px); }
    .btn-success { background: #10b981; color: white; }
    .btn-success:hover { background: #059669; }
    .btn-secondary { background: #334155; color: #e2e8f0; }
    .btn-secondary:hover { background: #475569; }
    .btn-action { background: #6366f1; color: white; }
    .btn-action:hover { background: #4f46e5; }
    .status-box { padding: 8px 10px; border-radius: 6px; font-size: 11px; display: none; margin-top: 8px; word-break: break-word; }
    .status-success { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }
    .status-error { background: #450a0a; color: #fca5a5; border: 1px solid #dc2626; }
    .help-link { color: #38bdf8; text-decoration: none; font-size: 11px; }
    .help-link:hover { text-decoration: underline; }
    .quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
    .quick-actions button { margin-bottom: 0; font-size: 11px; padding: 7px 6px; }
  </style>
</head>
<body>
  <div class="header">
    <h2>⚡ Sheet2Pipeline <span class="badge">PRO</span></h2>
  </div>

  <!-- API CONFIGURATION -->
  <div class="card">
    <div class="card-title">
      <span>1. Gemini AI API Key</span>
      <a href="https://aistudio.google.com/app/apikey" target="_blank" class="help-link">Get Free Key ↗</a>
    </div>
    <label>Google Gemini API Key:</label>
    <input type="password" id="apiKey" value="${currentKey}" placeholder="AIzaSy..." />
    
    <label>AI Model:</label>
    <select id="model">
      <option value="gemini-1.5-flash" ${currentModel === 'gemini-1.5-flash' ? 'selected' : ''}>Gemini 1.5 Flash (Ultra Fast & Free)</option>
      <option value="gemini-2.0-flash" ${currentModel === 'gemini-2.0-flash' ? 'selected' : ''}>Gemini 2.0 Flash (Next-Gen)</option>
      <option value="gemini-1.5-pro" ${currentModel === 'gemini-1.5-pro' ? 'selected' : ''}>Gemini 1.5 Pro (Deep Reasoning)</option>
    </select>
    
    <button class="btn btn-primary" onclick="saveApiSettings()">💾 Save & Test API Key</button>
    <div id="apiStatus" class="status-box"></div>
  </div>

  <!-- OFFER & SENDER SETTINGS -->
  <div class="card">
    <div class="card-title">2. Your Outreach Context</div>
    <label>Your Name:</label>
    <input type="text" id="senderName" value="${currentSender}" placeholder="e.g. Adi Mehra" />
    
    <label>Your Company / Agency:</label>
    <input type="text" id="company" value="${currentCompany}" placeholder="e.g. OutboundVelocity" />
    
    <label>Your Core Value Proposition / Offer:</label>
    <textarea id="offer" placeholder="What results do you deliver for clients?">${currentOffer}</textarea>

    <label>Target ICP Criteria (for scoring 1-100):</label>
    <textarea id="icp" placeholder="Target roles, industry, pain points...">${currentICP}</textarea>

    <label>Standard Call To Action (Low Friction):</label>
    <input type="text" id="cta" value="${currentCTA}" placeholder="e.g. Open to seeing a quick 3-min teardown?" />

    <button class="btn btn-secondary" onclick="saveContextSettings()">💾 Save Outreach Profile</button>
    <div id="contextStatus" class="status-box"></div>
  </div>

  <!-- QUICK ACTIONS -->
  <div class="card">
    <div class="card-title">3. Quick Actions (Selected Rows)</div>
    <div class="quick-actions">
      <button class="btn btn-action" onclick="runScriptAction('menuEnrichCompany')">🌐 Enrich Intel</button>
      <button class="btn btn-action" onclick="runScriptAction('menuScoreICP')">🎯 Score ICP</button>
      <button class="btn btn-action" onclick="runScriptAction('menuGenerateIcebreakers')">💡 Icebreakers</button>
      <button class="btn btn-action" onclick="runScriptAction('menuGenerateSequences')">✉️ Cold Emails</button>
    </div>
    <button class="btn btn-primary" style="margin-top:8px;" onclick="runScriptAction('menuRunFullPipeline')">⚡ Run Full AI Pipeline</button>
    <button class="btn btn-success" onclick="runScriptAction('menuCreateGmailDrafts')">📬 Create Gmail Drafts</button>
  </div>

  <script>
    function showStatus(id, text, isSuccess) {
      const el = document.getElementById(id);
      el.style.display = 'block';
      el.className = 'status-box ' + (isSuccess ? 'status-success' : 'status-error');
      el.innerText = text;
      setTimeout(() => { el.style.display = 'none'; }, 6000);
    }

    function saveApiSettings() {
      const apiKey = document.getElementById('apiKey').value.trim();
      const model = document.getElementById('model').value;
      if (!apiKey) {
        showStatus('apiStatus', 'Please enter a valid Gemini API key.', false);
        return;
      }
      google.script.run
        .withSuccessHandler(res => {
          showStatus('apiStatus', res.message, res.success);
        })
        .withFailureHandler(err => {
          showStatus('apiStatus', 'Error: ' + err.message, false);
        })
        .saveApiConfig(apiKey, model);
    }

    function saveContextSettings() {
      const sender = document.getElementById('senderName').value.trim();
      const company = document.getElementById('company').value.trim();
      const offer = document.getElementById('offer').value.trim();
      const icp = document.getElementById('icp').value.trim();
      const cta = document.getElementById('cta').value.trim();

      google.script.run
        .withSuccessHandler(res => {
          showStatus('contextStatus', res.message, res.success);
        })
        .withFailureHandler(err => {
          showStatus('contextStatus', 'Error: ' + err.message, false);
        })
        .saveContextConfig(sender, company, offer, icp, cta);
    }

    function runScriptAction(fnName) {
      google.script.run[fnName]();
    }
  </script>
</body>
</html>
  `;
}

// ----------------------------------------------------------------------------
// 3. SETTINGS PERSISTENCE & API WRAPPERS
// ----------------------------------------------------------------------------

/**
 * Saves API key and validates it against Google Gemini API
 */
function saveApiConfig(apiKey, model) {
  const props = PropertiesService.getUserProperties();
  props.setProperty(S2P_CONFIG.PROP_API_KEY, apiKey);
  props.setProperty(S2P_CONFIG.PROP_MODEL, model);

  // Test the key
  const testRes = callGeminiApi('Respond with the word "CONNECTED" only.', apiKey, model);
  if (testRes && testRes.includes('CONNECTED')) {
    return { success: true, message: '✅ API Key verified and saved successfully! Model: ' + model };
  } else if (testRes) {
    return { success: true, message: '✅ API Key saved! Response received.' };
  } else {
    return { success: false, message: '❌ Invalid API key or connection error. Please check your Gemini key.' };
  }
}

/**
 * Saves user offer, ICP, and sender settings
 */
function saveContextConfig(senderName, company, offer, icp, cta) {
  const props = PropertiesService.getUserProperties();
  props.setProperty(S2P_CONFIG.PROP_SENDER_NAME, senderName);
  props.setProperty(S2P_CONFIG.PROP_COMPANY, company);
  props.setProperty(S2P_CONFIG.PROP_OFFER, offer);
  props.setProperty(S2P_CONFIG.PROP_ICP, icp);
  props.setProperty(S2P_CONFIG.PROP_CTA, cta);

  return { success: true, message: '✅ Outreach context & ICP profile saved!' };
}

/**
 * Standalone connection tester for the menu
 */
function testGeminiConnection() {
  const ui = SpreadsheetApp.getUi();
  const props = PropertiesService.getUserProperties();
  const apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  const model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;

  if (!apiKey) {
    ui.alert('No API Key Found', 'Please open "⚡ Sheet2Pipeline AI" -> "⚙️ Open Settings & AI Control Panel" and enter your free Gemini API key from Google AI Studio.', ui.ButtonSet.OK);
    return;
  }

  ui.alert('Testing Connection', 'Pinging Gemini API with model: ' + model + '...', ui.ButtonSet.OK);
  const response = callGeminiApi('Write a 5-word slogan for B2B outbound sales.', apiKey, model);
  
  if (response) {
    ui.alert('🎉 Connection Successful!', 'Gemini Flash AI responded:\n\n"' + response.trim() + '"\n\nYou are all set to enrich leads and generate high-converting sequences!', ui.ButtonSet.OK);
  } else {
    ui.alert('Connection Failed', 'Could not connect to Gemini API. Please ensure your API key is valid and has access in Google AI Studio.', ui.ButtonSet.OK);
  }
}

// ----------------------------------------------------------------------------
// 4. CORE GEMINI API ENGINE
// ----------------------------------------------------------------------------

/**
 * Low-level Gemini API Caller with rate limit backoff and error handling
 */
function callGeminiApi(promptText, apiKey, model) {
  if (!apiKey) {
    const props = PropertiesService.getUserProperties();
    apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  }
  if (!model) {
    const props = PropertiesService.getUserProperties();
    model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;
  }

  if (!apiKey) {
    throw new Error('Gemini API key missing. Please configure in Settings.');
  }

  const endpoint = `${S2P_CONFIG.API_BASE_URL}${model}:generateContent?key=${apiKey}`;

  const payload = {
    contents: [
      {
        parts: [
          { text: promptText }
        ]
      }
    ],
    generationConfig: {
      temperature: 0.4,
      maxOutputTokens: 1200
    }
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  let attempts = 0;
  const maxAttempts = 3;

  while (attempts < maxAttempts) {
    try {
      const response = UrlFetchApp.fetch(endpoint, options);
      const statusCode = response.getResponseCode();
      const body = response.getContentText();

      if (statusCode === 200) {
        const json = JSON.parse(body);
        if (json.candidates && json.candidates.length > 0 && json.candidates[0].content && json.candidates[0].content.parts.length > 0) {
          return json.candidates[0].content.parts[0].text.trim();
        }
        return '';
      } else if (statusCode === 429) {
        // Rate limit - backoff
        attempts++;
        Utilities.sleep(1500 * attempts);
      } else {
        Logger.log('Gemini API Error: ' + body);
        return null;
      }
    } catch (e) {
      Logger.log('Fetch exception: ' + e.toString());
      attempts++;
      Utilities.sleep(1000 * attempts);
    }
  }
  return null;
}

// ----------------------------------------------------------------------------
// 5. WEB SCRAPING & INTEL HELPER
// ----------------------------------------------------------------------------

/**
 * Fetches website homepage text & detects tech stack signatures
 */
function fetchWebsiteIntel(domainOrUrl) {
  if (!domainOrUrl || domainOrUrl.toString().trim() === '') return '';
  let url = domainOrUrl.toString().trim();
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  try {
    const response = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true,
      validateHttpsCertificates: false,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
      }
    });

    if (response.getResponseCode() !== 200) {
      return `Domain reachable (HTTP ${response.getResponseCode()})`;
    }

    const html = response.getContentText();

    // Detect common tech stack signatures
    const detectedTech = [];
    if (/wp-content|wordpress/i.test(html)) detectedTech.push('WordPress');
    if (/shopify|cdn\.shopify\.com/i.test(html)) detectedTech.push('Shopify');
    if (/webflow/i.test(html)) detectedTech.push('Webflow');
    if (/hubspot|hs-scripts/i.test(html)) detectedTech.push('HubSpot');
    if (/salesforce|pardot/i.test(html)) detectedTech.push('Salesforce');
    if (/klaviyo/i.test(html)) detectedTech.push('Klaviyo');
    if (/stripe\.com/i.test(html)) detectedTech.push('Stripe');
    if (/intercom/i.test(html)) detectedTech.push('Intercom');
    if (/segment\.com|analytics\.js/i.test(html)) detectedTech.push('Segment');
    if (/next\.js|__NEXT_DATA__/i.test(html)) detectedTech.push('Next.js/React');

    // Clean text for meta title and description
    let titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    let title = titleMatch ? titleMatch[1].trim() : '';

    let metaDescMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i);
    let metaDesc = metaDescMatch ? metaDescMatch[1].trim() : '';

    // Strip HTML tags for clean body sample
    let cleanText = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, ' ')
                        .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, ' ')
                        .replace(/<[^>]+>/g, ' ')
                        .replace(/\s+/g, ' ')
                        .trim()
                        .substring(0, 1800);

    return JSON.stringify({
      title: title,
      description: metaDesc,
      detectedTech: detectedTech.join(', '),
      contentSnippet: cleanText
    });
  } catch (err) {
    return 'Website fetch error: ' + err.message;
  }
}

// ----------------------------------------------------------------------------
// 6. PIPELINE WORKERS (ROW-LEVEL LOGIC)
// ----------------------------------------------------------------------------

/**
 * Worker: Enrich Company Info & Tech Stack
 */
function enrichCompanyRow(companyName, website, prospectTitle) {
  const props = PropertiesService.getUserProperties();
  const apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  const model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;

  let scrapedData = '';
  if (website) {
    scrapedData = fetchWebsiteIntel(website);
  }

  const prompt = `
You are a senior B2B Market Intelligence & Sales Research Analyst.
Analyze this company and return a concise, high-value intelligence summary for a sales rep.

Company Name: ${companyName}
Website: ${website}
Prospect Title: ${prospectTitle}
Scraped Website Data / Tech Stack hints: ${scrapedData}

Provide a structured 3-bullet summary in EXACTLY this format:
• Core Business & ICP: [1 punchy sentence describing what they do and who they sell to]
• Tech Stack & Tools: [List detected or typical tools used e.g. HubSpot, Shopify, React, Stripe]
• Growth / Pain Trigger: [1 observable opportunity or scaling challenge they likely face]

Keep the entire output under 60 words. No fluff.
`;

  return callGeminiApi(prompt, apiKey, model) || 'Unable to enrich company.';
}

/**
 * Worker: Score ICP Fit (1-100)
 */
function scoreICPRow(prospectTitle, companyName, prospectBio, companyIntel) {
  const props = PropertiesService.getUserProperties();
  const apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  const model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;
  const targetICP = props.getProperty(S2P_CONFIG.PROP_ICP) || 'B2B Founders, CMOs, VPs of Sales looking to scale outbound.';

  const prompt = `
You are a strict B2B Sales Qualification Director.
Score the prospect's ICP (Ideal Customer Profile) fit from 1 to 100 based on our target criteria.

TARGET ICP CRITERIA:
"${targetICP}"

PROSPECT DATA:
- Role / Title: ${prospectTitle}
- Company: ${companyName}
- Bio / Notes: ${prospectBio}
- Company Intel: ${companyIntel}

SCORING RULES:
- 85-100: Direct decision-maker (Founder/C-level/VP) in exact target industry with urgent pain.
- 65-84: Good influencer or secondary target role, solid potential.
- Below 65: Poor fit, irrelevant department, or non-target size.

Output in EXACTLY this format:
[Score]/100 - [1 concise sentence explaining the exact reason for the score]
`;

  return callGeminiApi(prompt, apiKey, model) || 'Score: N/A';
}

/**
 * Worker: Generate 1-Line Punchy Icebreaker
 */
function generateIcebreakerRow(firstName, companyName, prospectTitle, prospectBio, companyIntel) {
  const props = PropertiesService.getUserProperties();
  const apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  const model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;

  const prompt = `
You are an elite B2B cold email copywriter who writes 1-line personalized hooks that get 40%+ reply rates.

PROSPECT:
- First Name: ${firstName}
- Company: ${companyName}
- Title: ${prospectTitle}
- Prospect Bio/Notes: ${prospectBio}
- Company Intel: ${companyIntel}

RULES:
1. Write EXACTLY ONE punchy sentence (10-22 words).
2. It must feel 1-to-1, thoughtful, and reference their specific role, company focus, or industry dynamic.
3. NEVER say: "I hope you're having a great week", "Congrats on the role", "I came across your profile", "Impressive work".
4. Sound like a peer executive dropping a sharp observation.

Output ONLY the one-line icebreaker sentence. No quotes, no preamble.
`;

  return callGeminiApi(prompt, apiKey, model) || `Noticed how ${companyName} is expanding its footprint in the market.`;
}

/**
 * Worker: Generate Full Cold Email Sequence (Touch 1, Follow-up 1, Follow-up 2)
 */
function generateSequenceRow(firstName, prospectTitle, companyName, icebreaker, companyIntel) {
  const props = PropertiesService.getUserProperties();
  const apiKey = props.getProperty(S2P_CONFIG.PROP_API_KEY);
  const model = props.getProperty(S2P_CONFIG.PROP_MODEL) || S2P_CONFIG.DEFAULT_MODEL;
  const senderName = props.getProperty(S2P_CONFIG.PROP_SENDER_NAME) || 'Adi';
  const senderCompany = props.getProperty(S2P_CONFIG.PROP_COMPANY) || 'OutboundAI';
  const offer = props.getProperty(S2P_CONFIG.PROP_OFFER) || 'We build AI-powered outbound lead engines on pay-on-results basis.';
  const cta = props.getProperty(S2P_CONFIG.PROP_CTA) || 'Open to seeing a 3-min loom breakdown?';

  const prompt = `
You are a world-class cold email strategist writing high-converting B2B outreach.

SENDER CONTEXT:
- Sender Name: ${senderName}
- Sender Company: ${senderCompany}
- Core Offer/Value Prop: ${offer}
- Call to Action: ${cta}

PROSPECT CONTEXT:
- Name: ${firstName}
- Role: ${prospectTitle}
- Company: ${companyName}
- Personalized Hook/Icebreaker: ${icebreaker}
- Company Intel: ${companyIntel}

Write a 3-part sequence with strict word limits. Return output in JSON format ONLY:
{
  "subject": "3-4 word curiosity subject line in lowercase (e.g., quick question re: ${companyName})",
  "touch1": "Under 80 words. Starts with the icebreaker hook -> transitions smoothly to our offer without hype -> ends with the low-friction CTA -> sign off as ${senderName}.",
  "followup1": "Under 45 words. A casual 3-day follow-up bumping the previous message with a quick 1-sentence social proof or insight -> repeats CTA.",
  "followup2": "Under 35 words. A low-pressure final check-in sharing a free asset or asking if timing is off."
}

Do not include markdown codeblocks or quotes outside the JSON. Return pure JSON.
`;

  const rawJson = callGeminiApi(prompt, apiKey, model);
  try {
    const cleaned = rawJson.replace(/```json/gi, '').replace(/```/g, '').trim();
    return JSON.parse(cleaned);
  } catch (e) {
    return {
      subject: `quick question re: ${companyName}`,
      touch1: `Hi ${firstName},\n\n${icebreaker}\n\n${offer}\n\n${cta}\n\nBest,\n${senderName}`,
      followup1: `Hi ${firstName}, wanted to bubble this up in case it got buried. Happy to share how we achieved similar results for peer companies.\n\n${cta}`,
      followup2: `Hi ${firstName}, know you're super busy running ${companyName}. If timing is off just let me know and I'll back off!`
    };
  }
}

// ----------------------------------------------------------------------------
// 7. BATCH EXECUTION WRAPPERS (MENU ACTIONS)
// ----------------------------------------------------------------------------

/**
 * Gets selected rows or active range
 */
function getSelectedRowIndices() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const selection = sheet.getActiveRange();
  if (!selection) return [];

  const startRow = Math.max(2, selection.getRow());
  const numRows = selection.getNumRows();
  const indices = [];

  for (let r = startRow; r < startRow + numRows; r++) {
    indices.push(r);
  }
  return indices;
}

/**
 * Menu Action: Enrich Company
 */
function menuEnrichCompany() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  if (rows.length === 0) {
    SpreadsheetApp.getUi().alert('Please select the row(s) you want to enrich.');
    return;
  }

  SpreadsheetApp.getActiveSpreadsheet().toast(`Enriching ${rows.length} company(ies)...`, 'Sheet2Pipeline', 5);

  rows.forEach((row, i) => {
    const companyName = sheet.getRange(row, 5).getValue();
    const website = sheet.getRange(row, 6).getValue();
    const title = sheet.getRange(row, 4).getValue();

    if (companyName || website) {
      sheet.getRange(row, 8).setValue('⏳ Scraping & analyzing...');
      SpreadsheetApp.flush();
      const intel = enrichCompanyRow(companyName, website, title);
      sheet.getRange(row, 8).setValue(intel);
    }
  });

  SpreadsheetApp.getActiveSpreadsheet().toast('✅ Company enrichment complete!', 'Done', 5);
}

/**
 * Menu Action: Score ICP
 */
function menuScoreICP() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  if (rows.length === 0) {
    SpreadsheetApp.getUi().alert('Please select the row(s) you want to score.');
    return;
  }

  SpreadsheetApp.getActiveSpreadsheet().toast(`Scoring ICP for ${rows.length} prospect(s)...`, 'Sheet2Pipeline', 5);

  rows.forEach((row) => {
    const title = sheet.getRange(row, 4).getValue();
    const company = sheet.getRange(row, 5).getValue();
    const bio = sheet.getRange(row, 7).getValue();
    const intel = sheet.getRange(row, 8).getValue();

    if (title || company) {
      sheet.getRange(row, 9).setValue('⏳ Scoring fit...');
      SpreadsheetApp.flush();
      const score = scoreICPRow(title, company, bio, intel);
      sheet.getRange(row, 9).setValue(score);
    }
  });

  SpreadsheetApp.getActiveSpreadsheet().toast('✅ ICP scoring complete!', 'Done', 5);
}

/**
 * Menu Action: Generate Icebreakers
 */
function menuGenerateIcebreakers() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  if (rows.length === 0) {
    SpreadsheetApp.getUi().alert('Please select row(s) to generate icebreakers.');
    return;
  }

  SpreadsheetApp.getActiveSpreadsheet().toast(`Writing personalized hooks for ${rows.length} lead(s)...`, 'Sheet2Pipeline', 5);

  rows.forEach((row) => {
    const firstName = sheet.getRange(row, 1).getValue() || 'there';
    const title = sheet.getRange(row, 4).getValue();
    const company = sheet.getRange(row, 5).getValue();
    const bio = sheet.getRange(row, 7).getValue();
    const intel = sheet.getRange(row, 8).getValue();

    if (company || title) {
      sheet.getRange(row, 10).setValue('⏳ Crafting hook...');
      SpreadsheetApp.flush();
      const hook = generateIcebreakerRow(firstName, company, title, bio, intel);
      sheet.getRange(row, 10).setValue(hook);
    }
  });

  SpreadsheetApp.getActiveSpreadsheet().toast('✅ Icebreakers generated!', 'Done', 5);
}

/**
 * Menu Action: Generate Sequences
 */
function menuGenerateSequences() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  if (rows.length === 0) {
    SpreadsheetApp.getUi().alert('Please select row(s) to generate email sequences.');
    return;
  }

  SpreadsheetApp.getActiveSpreadsheet().toast(`Generating sequences for ${rows.length} lead(s)...`, 'Sheet2Pipeline', 5);

  rows.forEach((row) => {
    const firstName = sheet.getRange(row, 1).getValue() || 'there';
    const title = sheet.getRange(row, 4).getValue();
    const company = sheet.getRange(row, 5).getValue();
    let hook = sheet.getRange(row, 10).getValue();
    const intel = sheet.getRange(row, 8).getValue();
    const bio = sheet.getRange(row, 7).getValue();

    // If hook is missing, generate it on the fly
    if (!hook) {
      hook = generateIcebreakerRow(firstName, company, title, bio, intel);
      sheet.getRange(row, 10).setValue(hook);
    }

    sheet.getRange(row, 11).setValue('⏳ Writing...');
    SpreadsheetApp.flush();

    const seq = generateSequenceRow(firstName, title, company, hook, intel);
    sheet.getRange(row, 11).setValue(seq.subject);
    sheet.getRange(row, 12).setValue(seq.touch1);
    sheet.getRange(row, 13).setValue(seq.followup1);
    sheet.getRange(row, 14).setValue(seq.followup2);
  });

  SpreadsheetApp.getActiveSpreadsheet().toast('✅ Cold email sequences generated!', 'Done', 5);
}

/**
 * Menu Action: Full End-to-End Pipeline
 */
function menuRunFullPipeline() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  if (rows.length === 0) {
    SpreadsheetApp.getUi().alert('Please select the row(s) to run the full pipeline.');
    return;
  }

  SpreadsheetApp.getActiveSpreadsheet().toast(`Running complete AI pipeline on ${rows.length} lead(s)...`, 'Sheet2Pipeline', 8);

  rows.forEach((row, idx) => {
    const firstName = sheet.getRange(row, 1).getValue() || 'there';
    const title = sheet.getRange(row, 4).getValue();
    const company = sheet.getRange(row, 5).getValue();
    const website = sheet.getRange(row, 6).getValue();
    const bio = sheet.getRange(row, 7).getValue();

    SpreadsheetApp.getActiveSpreadsheet().toast(`Processing row ${row} (${idx + 1}/${rows.length}): ${company}...`, 'Working', 3);

    // 1. Enrich
    const intel = enrichCompanyRow(company, website, title);
    sheet.getRange(row, 8).setValue(intel);
    SpreadsheetApp.flush();

    // 2. Score ICP
    const score = scoreICPRow(title, company, bio, intel);
    sheet.getRange(row, 9).setValue(score);
    SpreadsheetApp.flush();

    // 3. Icebreaker
    const hook = generateIcebreakerRow(firstName, company, title, bio, intel);
    sheet.getRange(row, 10).setValue(hook);
    SpreadsheetApp.flush();

    // 4. Sequence
    const seq = generateSequenceRow(firstName, title, company, hook, intel);
    sheet.getRange(row, 11).setValue(seq.subject);
    sheet.getRange(row, 12).setValue(seq.touch1);
    sheet.getRange(row, 13).setValue(seq.followup1);
    sheet.getRange(row, 14).setValue(seq.followup2);
    SpreadsheetApp.flush();
  });

  SpreadsheetApp.getActiveSpreadsheet().toast('🎉 Full AI Pipeline completed for all selected rows!', 'Success', 8);
}

// ----------------------------------------------------------------------------
// 8. 1-CLICK GMAIL DRAFT ENGINE
// ----------------------------------------------------------------------------

/**
 * Menu Action: Create Gmail Drafts for Selected Rows
 */
function menuCreateGmailDrafts() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = getSelectedRowIndices();
  const ui = SpreadsheetApp.getUi();

  if (rows.length === 0) {
    ui.alert('Please select the row(s) you want to create Gmail drafts for.');
    return;
  }

  let createdCount = 0;
  let skippedCount = 0;

  rows.forEach((row) => {
    const email = sheet.getRange(row, 3).getValue();
    const subject = sheet.getRange(row, 11).getValue();
    const body = sheet.getRange(row, 12).getValue();

    if (!email || !email.toString().includes('@')) {
      sheet.getRange(row, 15).setValue('❌ Skipped (No valid email)');
      skippedCount++;
      return;
    }

    if (!subject || !body) {
      sheet.getRange(row, 15).setValue('❌ Skipped (Missing subject/body)');
      skippedCount++;
      return;
    }

    try {
      // Format text with linebreaks to HTML
      const htmlBody = body.toString().replace(/\n/g, '<br>');
      
      const draft = GmailApp.createDraft(email, subject, body, {
        htmlBody: htmlBody
      });

      const draftId = draft.getId();
      sheet.getRange(row, 15).setValue(`✅ Draft Created (${draftId.substring(0, 8)}...)`);
      createdCount++;
    } catch (err) {
      sheet.getRange(row, 15).setValue('❌ Error: ' + err.message);
    }
  });

  ui.alert(
    'Gmail Draft Creation Complete',
    `Created ${createdCount} draft(s) in your Gmail account.\nSkipped / Failed: ${skippedCount}.\n\nYou can now open Gmail, review your personalized drafts, and hit send!`,
    ui.ButtonSet.OK
  );
}

// ----------------------------------------------------------------------------
// 9. CUSTOM SPREADSHEET FORMULAS (FOR IN-CELL USE)
// ----------------------------------------------------------------------------

/**
 * Enriches a company domain with business summary and tech stack.
 * @param {string} domainOrUrl The company website URL or domain.
 * @return {string} High-value company intel bullet points.
 * @customfunction
 */
function S2P_ENRICH(domainOrUrl) {
  if (!domainOrUrl) return '';
  return enrichCompanyRow('', domainOrUrl, '');
}

/**
 * Generates a punchy, 1-line personalized cold email icebreaker.
 * @param {string} firstName Prospect's first name.
 * @param {string} company Prospect's company name.
 * @param {string} title Prospect's job role.
 * @param {string} notes Optional context, LinkedIn bio, or recent news.
 * @return {string} 1-line personalized hook.
 * @customfunction
 */
function S2P_ICEBREAKER(firstName, company, title, notes) {
  if (!company && !title) return '';
  return generateIcebreakerRow(firstName || 'there', company || '', title || '', notes || '', '');
}

/**
 * Scores prospect fit against your target ICP (1-100).
 * @param {string} title Prospect job title.
 * @param {string} company Prospect company.
 * @param {string} bio Prospect bio or notes.
 * @return {string} Score / 100 with explanation.
 * @customfunction
 */
function S2P_ICP_SCORE(title, company, bio) {
  if (!title && !company) return '';
  return scoreICPRow(title || '', company || '', bio || '', '');
}

/**
 * Generates a personalized cold email pitch.
 * @param {string} firstName Prospect name.
 * @param {string} company Company name.
 * @param {string} painPoint Specific pain point or intel.
 * @return {string} Cold email draft.
 * @customfunction
 */
function S2P_EMAIL(firstName, company, painPoint) {
  if (!company) return '';
  const hook = generateIcebreakerRow(firstName || 'there', company, '', painPoint || '', '');
  const seq = generateSequenceRow(firstName || 'there', '', company, hook, painPoint || '');
  return seq.touch1;
}

// ----------------------------------------------------------------------------
// 10. USER HELP DIALOG
// ----------------------------------------------------------------------------

function showHelpDialog() {
  const ui = SpreadsheetApp.getUi();
  const helpText = 
`⚡ SHEET2PIPELINE QUICK START GUIDE:

1. SETUP:
   • Click '⚡ Sheet2Pipeline AI' -> '🚀 1-Click Sheet Template Setup' to initialize columns.
   • Click '⚙️ Open Settings & AI Control Panel' to input your free Gemini API key and outreach offer.

2. RUNNING THE AI:
   • Fill or paste your lead data in Columns A through G.
   • Highlight the rows you want to process.
   • Click '⚡ Run Full Pipeline on Selected Rows' or run individual steps from the menu.

3. GMAIL INTEGRATION:
   • Once sequences are generated in Columns K & L, select the rows.
   • Click '📬 Create Gmail Drafts (Selected Rows)'.
   • Open Gmail -> Drafts folder -> Review & hit Send!

4. CUSTOM FORMULAS:
   • =S2P_ICEBREAKER("Sarah", "Acme Corp", "VP Marketing", "Scaling SDRs")
   • =S2P_ENRICH("stripe.com")
   • =S2P_ICP_SCORE("Chief Revenue Officer", "TechFlow", "Series B SaaS")

Need help or want custom workflow automation? Contact Adi Mehra.`;

  ui.alert('📖 Sheet2Pipeline User Manual', helpText, ui.ButtonSet.OK);
}
