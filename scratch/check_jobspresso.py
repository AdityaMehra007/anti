import re
import json
import urllib.request

path = r'C:\Users\amehr\.gemini\antigravity\brain\840e3399-4077-429e-83be-e8dc0b080fe3\.system_generated\steps\1074\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

ajax_url_match = re.search(r'job_manager_ajax_url\s*=\s*["\']([^"\']+)["\']', text)
if ajax_url_match:
    print('Found job_manager_ajax_url:', ajax_url_match.group(1))
else:
    wp_ajax = re.findall(r'https?://[^"\']*/(?:admin-ajax\.php|jm-ajax/[^"\']*)', text)
    print('WP AJAX patterns:', wp_ajax)

# Search for any job_manager or wp-job-manager scripts or config
configs = re.findall(r'var job_manager[^\;]+;', text)
for c in configs:
    print(c[:200])

scripts = re.findall(r'https?://[^"\']+/wp-content/plugins/wp-job-manager[^"\']+', text)
print('Job manager scripts:', scripts[:5])
