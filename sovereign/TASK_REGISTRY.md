# 📋 ADI SOVEREIGN OS — TASK STATE & PRIORITY ENGINE

## 1. TASK STATE MACHINE

```text
[DISCOVERED] ➔ [PLANNED] ➔ [READY] ➔ [RUNNING] ➔ [REVIEW] ➔ [VERIFIED] ➔ [COMPLETE]
                                    │               │
                                    ▼               ▼
                                [BLOCKED]       [FAILED] ➔ [RETRYING] ➔ [ESCALATED]
```

## 2. PRIORITY SCORING FORMULA

$$\text{Priority} = \frac{\text{Impact} \times \text{Probability} \times \text{Urgency} \times \text{Strategic Value} \times \text{Leverage}}{\text{Cost}}$$

- **Impact** (1–10): Real-world upside to income, leverage, or capability.
- **Probability** (0.1–1.0): Likelihood of successful execution.
- **Urgency** (1–10): Time decay and opportunity expiration speed.
- **Strategic Value** (1–10): Long-term compounding effect.
- **Leverage** (1–10): Ability to become reusable infrastructure.
- **Cost** (1–10): Time, attention, and resource expenditure.
