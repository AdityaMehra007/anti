/**
 * supabase_client.js
 * Production-grade Supabase client module for Node.js.
 * Zero-dependency: uses native Node.js fetch (v18+).
 */

const DEFAULT_URL = process.env.SUPABASE_URL || 'http://localhost:8000';
const DEFAULT_KEY = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MDAwMDAwMDAsImV4cCI6MjAwMDAwMDAwMH0.M1m5sK_4-yHk9jN7X0wK3pQ8g7h9r3v2y1t0q8p9o6w';

class SupabaseNodeClient {
  constructor(url = DEFAULT_URL, key = DEFAULT_KEY) {
    this.url = url.replace(/\/+$/, '');
    this.key = key;
    this.restUrl = `${this.url}/rest/v1`;
    this.authUrl = `${this.url}/auth/v1`;
    this.storageUrl = `${this.url}/storage/v1`;
  }

  _headers(customHeaders = {}) {
    return {
      'apikey': this.key,
      'Authorization': `Bearer ${this.key}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...customHeaders,
    };
  }

  async _request(method, endpoint, body = null, headers = {}) {
    const fullUrl = endpoint.startsWith('http') ? endpoint : `${this.url}/${endpoint.replace(/^\/+/, '')}`;
    const options = {
      method,
      headers: this._headers(headers),
    };
    if (body !== null) {
      options.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(fullUrl, options);
      const text = await response.text();
      let data = null;
      try {
        data = text ? JSON.parse(text) : null;
      } catch {
        data = text;
      }
      return {
        status: response.status,
        ok: response.ok,
        data: response.ok ? data : null,
        error: !response.ok ? data : null,
      };
    } catch (err) {
      return {
        status: 0,
        ok: false,
        data: null,
        error: err.message,
      };
    }
  }

  // PostgREST Database operations
  async select(table, select = '*', filters = {}) {
    const params = new URLSearchParams({ select, ...filters });
    return this._request('GET', `${this.restUrl}/${table}?${params.toString()}`);
  }

  async insert(table, records, upsert = false) {
    const headers = { 'Prefer': 'return=representation' };
    if (upsert) headers['Prefer'] += ',resolution=merge-duplicates';
    return this._request('POST', `${this.restUrl}/${table}`, records, headers);
  }

  async update(table, matchColumn, matchValue, values) {
    const headers = { 'Prefer': 'return=representation' };
    return this._request('PATCH', `${this.restUrl}/${table}?${matchColumn}=eq.${encodeURIComponent(matchValue)}`, values, headers);
  }

  async delete(table, matchColumn, matchValue) {
    return this._request('DELETE', `${this.restUrl}/${table}?${matchColumn}=eq.${encodeURIComponent(matchValue)}`);
  }

  async rpc(functionName, params = {}) {
    return this._request('POST', `${this.restUrl}/rpc/${functionName}`, params);
  }

  // Auth operations
  async signUp(email, password, metadata = {}) {
    return this._request('POST', `${this.authUrl}/signup`, { email, password, data: metadata });
  }

  async signInWithPassword(email, password) {
    return this._request('POST', `${this.authUrl}/token?grant_type=password`, { email, password });
  }

  // Health check
  async healthCheck() {
    const rest = await this._request('GET', `${this.restUrl}/`);
    const auth = await this._request('GET', `${this.authUrl}/health`);
    return {
      gateway: rest.status !== 0 || auth.status !== 0,
      rest: [200, 401, 404].includes(rest.status),
      auth: [200, 401].includes(auth.status),
      details: { rest, auth }
    };
  }
}

function createClient(url, key) {
  return new SupabaseNodeClient(url, key);
}

module.exports = {
  createClient,
  SupabaseNodeClient,
  DEFAULT_URL,
  DEFAULT_KEY,
};

if (require.main === module) {
  const client = createClient();
  console.log('[*] Testing Supabase Node.js client...');
  client.healthCheck().then(res => {
    console.log('[*] Health Check Result:', JSON.stringify(res, null, 2));
  });
}
