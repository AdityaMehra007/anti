/**
 * n8n_bridge.js — Node.js Automation & Webhook Bridge for n8n
 *
 * Exposes lightweight helper utilities to emit events from Node/JavaScript tasks
 * directly into n8n webhook nodes or manage execution payloads.
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

class N8nBridge {
  constructor(baseUrl = process.env.N8N_BASE_URL || 'http://localhost:5678', apiKey = process.env.N8N_API_KEY || '') {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.apiKey = apiKey;
  }

  /**
   * Dispatch payload to an n8n webhook endpoint
   * @param {string} path Webhook path configured in n8n (e.g. 'outreach-hook')
   * @param {object} payload JSON payload object
   * @param {boolean} isTest Whether to trigger test webhook URL
   */
  async triggerWebhook(path, payload = {}, isTest = false) {
    const prefix = isTest ? 'webhook-test' : 'webhook';
    const cleanPath = path.replace(/^\/+/, '');
    const targetUrl = new URL(`${this.baseUrl}/${prefix}/${cleanPath}`);

    const data = JSON.stringify(payload);
    const transport = targetUrl.protocol === 'https:' ? https : http;

    return new Promise((resolve, reject) => {
      const req = transport.request(
        targetUrl,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data),
            ...(this.apiKey ? { 'X-N8N-API-KEY': this.apiKey } : {}),
          },
          timeout: 10000,
        },
        (res) => {
          let body = '';
          res.on('data', (chunk) => (body += chunk));
          res.on('end', () => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              try {
                resolve(body ? JSON.parse(body) : { status: 'ok', statusCode: res.statusCode });
              } catch {
                resolve({ status: 'ok', raw: body, statusCode: res.statusCode });
              }
            } else {
              reject(new Error(`n8n webhook error [${res.statusCode}]: ${body}`));
            }
          });
        }
      );

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Webhook request timed out after 10s'));
      });

      req.write(data);
      req.end();
    });
  }

  /**
   * Check n8n health endpoint
   */
  async checkHealth() {
    return new Promise((resolve) => {
      const targetUrl = new URL(`${this.baseUrl}/healthz`);
      const transport = targetUrl.protocol === 'https:' ? https : http;

      const req = transport.get(targetUrl, { timeout: 4000 }, (res) => {
        resolve(res.statusCode === 200 || res.statusCode === 204);
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });
    });
  }
}

module.exports = { N8nBridge };

// Direct execution test
if (require.main === module) {
  const bridge = new N8nBridge();
  console.log('[*] Testing n8n bridge connection to:', bridge.baseUrl);
  bridge.checkHealth().then((ok) => {
    console.log(`[*] n8n service is: ${ok ? 'ONLINE' : 'OFFLINE'}`);
  });
}
