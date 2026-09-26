import os
from langchain_openai import ChatOpenAI

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"[*] OpenRouter Key detected: {bool(api_key)}")

llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.1,
)

try:
    resp = llm.invoke("Hello, reply with only 'OPENROUTER_CONNECTED'!")
    print("[+] LLM Response:", resp.content)
except Exception as e:
    print("[-] OpenRouter connection error:", e)
