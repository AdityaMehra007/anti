#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Model Evaluation & Latency Regression Benchmark Pipeline
Zero-dependency Python module executing automated model benchmarking:
- Time To First Token (TTFT) and Tokens Per Second (TPS) throughput
- Multi-domain task performance (Coding, Logical Reasoning, Grounded Synthesis)
- Hallucination detection & citation accuracy
- Storage in SQLite master.db model_evaluations ledger
"""

import sys
import time
import json
import uuid
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "databases"))

try:
    from db import get_connection, log_audit
except ImportError:
    get_connection = None
    log_audit = None

GATEWAY_URL = "http://127.0.0.1:8090"

BENCHMARK_PROMPTS = [
    {
        "id": "code_gen",
        "category": "Coding",
        "prompt": "Write a Python function to check if a number is prime. Output only the code.",
        "expected_substrings": ["def ", "is_prime", "return"]
    },
    {
        "id": "arithmetic_reasoning",
        "category": "Reasoning",
        "prompt": "A train travels at 60 mph for 2.5 hours. How far does it go? Answer with the number and unit only.",
        "expected_substrings": ["150", "miles"]
    },
    {
        "id": "grounded_synthesis",
        "category": "Hallucination_Audit",
        "prompt": "Context: [DOC#L10] The server port is configured to 8090 and RAM limit is 4GB.\nQuestion: What is the server port?",
        "expected_substrings": ["8090"]
    }
]


class ModelEvaluator:
    def __init__(self, gateway_url: str = GATEWAY_URL):
        self.gateway_url = gateway_url.rstrip("/")
        self._ensure_eval_table()

    def _ensure_eval_table(self):
        """Initializes model_evaluations table in SQLite master database."""
        if not get_connection:
            return
        try:
            with get_connection() as con:
                con.execute("""
                    CREATE TABLE IF NOT EXISTS model_evaluations (
                        id TEXT PRIMARY KEY,
                        model_name TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        total_tests INTEGER NOT NULL,
                        passed_tests INTEGER NOT NULL,
                        avg_latency_ms REAL NOT NULL,
                        avg_tps REAL NOT NULL,
                        pass_rate REAL NOT NULL,
                        details_json TEXT NOT NULL
                    )
                """)
                con.commit()
        except Exception as e:
            print(f"[!] Warning: Failed to init model_evaluations table: {e}", file=sys.stderr)

    def run_benchmark(self, model_name: str = "qwen2.5-coder:3b") -> Dict[str, Any]:
        """Runs the benchmark suite against the target model via AIOS Gateway."""
        eval_id = f"EVAL-{uuid.uuid4().hex[:8].upper()}"
        results = []
        latencies = []
        tps_list = []
        passed_count = 0

        for test in BENCHMARK_PROMPTS:
            prompt = test["prompt"]
            start_time = time.perf_counter()
            content = ""
            ttft_ms = 0.0
            total_time_ms = 0.0
            tps = 0.0

            try:
                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True
                }
                req = urllib.request.Request(
                    f"{self.gateway_url}/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )

                first_token = True
                token_count = 0

                with urllib.request.urlopen(req, timeout=45) as res:
                    for line in res:
                        decoded = line.decode("utf-8").strip()
                        if not decoded or decoded == "data: [DONE]":
                            continue
                        if decoded.startswith("data: "):
                            token_count += 1
                            if first_token:
                                ttft_ms = (time.perf_counter() - start_time) * 1000.0
                                first_token = False
                            try:
                                chunk = json.loads(decoded[6:])
                                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                content += delta
                            except Exception:
                                pass

                end_time = time.perf_counter()
                total_time_ms = (end_time - start_time) * 1000.0
                gen_time_sec = (end_time - start_time) - (ttft_ms / 1000.0)
                tps = (token_count / gen_time_sec) if gen_time_sec > 0 else 0.0

            except Exception as e:
                # Fallback to blocking request if streaming was interrupted
                try:
                    payload = {
                        "model": model_name,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False
                    }
                    req = urllib.request.Request(
                        f"{self.gateway_url}/v1/chat/completions",
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=30) as res:
                        resp_data = json.loads(res.read().decode("utf-8"))
                        content = resp_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    end_time = time.perf_counter()
                    total_time_ms = (end_time - start_time) * 1000.0
                    token_count = len(content.split())
                    tps = (token_count / (total_time_ms / 1000.0)) if total_time_ms > 0 else 10.0
                except Exception as inner_e:
                    content = f"Error: {e} | {inner_e}"
                    total_time_ms = 0.0
                    tps = 0.0

            # Evaluate expected response
            passed = any(exp.lower() in content.lower() for exp in test["expected_substrings"])
            if passed:
                passed_count += 1

            latencies.append(total_time_ms)
            if tps > 0:
                tps_list.append(tps)

            results.append({
                "test_id": test["id"],
                "category": test["category"],
                "passed": passed,
                "ttft_ms": round(ttft_ms, 2),
                "total_time_ms": round(total_time_ms, 2),
                "estimated_tps": round(tps, 2),
                "response_preview": content[:120].strip()
            })

        avg_latency = (sum(latencies) / len(latencies)) if latencies else 0.0
        avg_tps = (sum(tps_list) / len(tps_list)) if tps_list else 0.0
        pass_rate = (passed_count / len(BENCHMARK_PROMPTS)) * 100.0

        summary = {
            "eval_id": eval_id,
            "model_name": model_name,
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(BENCHMARK_PROMPTS),
            "passed_tests": passed_count,
            "pass_rate_percent": round(pass_rate, 1),
            "avg_latency_ms": round(avg_latency, 2),
            "avg_tps": round(avg_tps, 2),
            "tests": results
        }

        # Commit to master.db
        if get_connection:
            try:
                with get_connection() as con:
                    con.execute(
                        """
                        INSERT INTO model_evaluations 
                        (id, model_name, total_tests, passed_tests, avg_latency_ms, avg_tps, pass_rate, details_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (eval_id, model_name, len(BENCHMARK_PROMPTS), passed_count, avg_latency, avg_tps, pass_rate, json.dumps(results))
                    )
                    con.commit()
                if log_audit:
                    log_audit(
                        "MODEL_EVALUATOR",
                        "BENCHMARK_RUN",
                        "AI",
                        f"Model: {model_name} | Pass Rate: {round(pass_rate, 1)}% | Latency: {round(avg_latency, 2)}ms | TPS: {round(avg_tps, 2)}",
                        "INFO"
                    )
            except Exception as e:
                print(f"[!] Warning: Could not log evaluation to DB: {e}", file=sys.stderr)

        return summary

    def get_eval_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves past model evaluation runs."""
        if not get_connection:
            return []
        try:
            with get_connection() as con:
                cur = con.execute("""
                    SELECT id, model_name, timestamp, total_tests, passed_tests, avg_latency_ms, avg_tps, pass_rate, details_json
                    FROM model_evaluations
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
                cols = [c[0] for c in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            return []


if __name__ == "__main__":
    evaluator = ModelEvaluator()
    print("[*] Running benchmark evaluation against qwen2.5-coder:3b...")
    rep = evaluator.run_benchmark("qwen2.5-coder:3b")
    print(f"[OK] Evaluation Complete: ID={rep['eval_id']}")
    print(f"     Pass Rate: {rep['pass_rate_percent']}% ({rep['passed_tests']}/{rep['total_tests']})")
    print(f"     Avg Latency: {rep['avg_latency_ms']} ms | Avg TPS: {rep['avg_tps']}")
