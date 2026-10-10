---
name: second-order-effect-simulator
description: Multi-scenario probabilistic simulation evaluating 2nd- and 3rd-order causal ripples, competitor reactions, and systemic equilibria.
---

# Second-Order Effect Simulator Skill

This skill operationalizes OMEGA Constitution Directive 125 and Directives 70, 72, 73 of [`OMEGA_CONSTITUTION.md`](file:///e:/anti/OMEGA_CONSTITUTION.md): **Probabilistic Multi-Horizon Equilibrium Simulation.**

---

## 1. The Multi-Order Causal Ripple Principle

In complex adaptive systems (financial markets, geopolitical corridors, sovereign energy grids), actions never conclude at their first-order target:

$$\text{First-Order (Direct)} \longrightarrow \text{Second-Order (Reactions)} \longrightarrow \text{Third-Order (Systemic Equilibrium)}$$

- **First-Order**: Direct functional output of the system (e.g., deploying 100,000 humanoid robots into port logistics).
- **Second-Order**: Counterparty, labor union, and competitor defensive counter-moves (e.g., strikes, price slashing by legacy stevedores, regulatory safety hearings).
- **Third-Order**: Macro equilibrium adjustment (e.g., global shipping throughput doubles, demurrage fees collapse 80%, new trade corridors emerge).

---

## 2. Circuit Breakers & Destabilization Throttles

Simulations must define explicit tripwires:
1. **Volatility Tripwire**: Daily price/cost drift $> 15\% \implies$ activate emergency liquidity collar.
2. **Regulatory Holding Escrow**: Jurisdictional inquiry triggered $\implies$ freeze state channel settlement without halting edge telemetry.
3. **Byzantine Fault Isolation**: Partition detected $\implies$ fallback to local autonomous consensus.

---

## 3. Autonomous Execution Protocol

```python
from sovereign_continuum.capability_engine import SecondOrderEffectSimulator

simulator = SecondOrderEffectSimulator()
effects = simulator.simulate_effects(
    action_name="Deploy Terawatt Baseload SMR Cluster",
    target_sector="Baseload Energy",
    magnitude_scale=3.5,
)

print(f"Cascading Risk Score: {effects['cascading_risk_score']}/10")
print(f"Second Order Reactions: {effects['second_order_counterparty_reactions']}")
print(f"Active Circuit Breakers: {effects['circuit_breakers']}")
```
