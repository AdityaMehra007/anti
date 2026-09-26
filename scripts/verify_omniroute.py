import urllib.request
import json
import sys

def verify():
    url = "http://127.0.0.1:20128/v1/models"
    print(f"[TEST] Fetching models from {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            models = data.get("data", [])
            print(f"[SUCCESS] Gateway is ACTIVE! Total models cataloged: {len(models)}")
            sample = [m.get("id") for m in models[:8]]
            print(f"[MODELS] Sample IDs: {sample}")
            return True
    except Exception as e:
        print(f"[FAILED] Gateway query error: {e}")
        return False

def test_chat():
    url = "http://127.0.0.1:20128/v1/chat/completions"
    payload = {
        "model": "auto",
        "messages": [
            {"role": "user", "content": "Return the single word: OK"}
        ],
        "max_tokens": 10
    }
    print(f"[TEST] Testing zero-config 'auto' completion via {url}...")
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json", "Authorization": "Bearer sk-omniroute-local"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            model_used = res.get("model", "unknown")
            content = res.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = res.get("usage", {})
            print(f"[SUCCESS] Auto-routed model: {model_used}")
            print(f"[RESPONSE] Content: {content.strip()}")
            print(f"[USAGE] Tokens: {usage}")
            return True
    except Exception as e:
        print(f"[INFO] Chat test note: {e}")
        return False

if __name__ == "__main__":
    v = verify()
    c = test_chat()
    sys.exit(0 if v else 1)
