# LIVE TECHNOLOGY RADAR

| Domain | Technology / Component | Ring (Adopt / Trial / Assess / Hold) | Strategic Rationale |
|:---|:---|:---:|:---|
| **Vision & Extraction** | Gemini 1.5 Flash / Claude 3.5 Haiku | **ADOPT** | Sub-second extraction of scanned shipping bills at <$0.01 per page. |
| **Domain Reasoning** | Claude 3.5 Sonnet / Gemini 1.5 Pro | **ADOPT** | 99% accuracy on complex legal trade classification and cross-reference reasoning. |
| **Local Tariff DB** | SQLite / DuckDB In-Memory Index | **ADOPT** | Zero network latency on local 8-digit HS code search and validation. |
| **Autonomous Swarms** | LangGraph / Native Python Swarms | **ADOPT** | Deterministic state transitions; avoids chaotic non-deterministic looping. |
| **Heavy Vector DBs** | Pinecone / Milvus Managed Clusters | **HOLD** | Overkill for Stage 0; local DuckDB / SQLite FTS5 handles tariff search at zero cost. |
