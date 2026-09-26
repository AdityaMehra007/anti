# AI MULTI-AGENT ARCHITECTURE & INFERENCE ROUTING

```
                                  [USER INGESTION]
                                         |
                                 (Documents / ERP)
                                         |
                       +─────────────────▼─────────────────+
                       |    API GATEWAY & SECURITY PROXY   |
                       +─────────────────┬─────────────────+
                                         |
                                [ORCHESTRATION LAYER]
                       Company Commander / Task Controller
                                         |
            +────────────────────────────┼────────────────────────────+
            |                            |                            |
    [VISION INGESTION]          [REASONING AGENT]            [VERIFICATION AGENT]
  Flash / Local OCR Parser     Deep Domain Analysis         Deterministic Validator
   (Invoice/Packing List)     (Tariff & Regulatory Match)   (WCO/DGFT Database Cross-Check)
            |                            |                            |
            +────────────────────────────┼────────────────────────────+
                                         |
                             [EVIDENCE LEDGER AUDIT]
                                         |
                             [STRUCTURED OUTPUT & PDF]
```

## Inference Routing & Cost Optimization Rules
1. **Tier 1 (Extraction & OCR)**: Use high-speed, cost-efficient models (e.g. Gemini 1.5 Flash / Claude 3.5 Haiku) for raw bounding-box OCR and structured key-value extraction.
2. **Tier 2 (Trade Reasoning & Legal Matching)**: Route to high-reasoning models (Claude 3.5 Sonnet / Gemini 1.5 Pro) with exact system prompt constraints and temperature = 0.0.
3. **Tier 3 (Verification & Math Check)**: 100% deterministic Python rule checks (HS-code digit verification, currency exchange rate reconciliation, total weight balance). Zero hallucination allowed.
