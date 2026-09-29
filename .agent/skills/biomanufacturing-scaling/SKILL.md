---
name: biomanufacturing-scaling
description: Optimization of precision cellular fermentation economics, synthetic genetic compilation, downstream separation yield, and petrochemical displacement at gigaton scale.
---

# Biomanufacturing Scaling Skill

This skill operationalizes OMEGA Mode D (Build) and Mode I (Optimization) to scale precision biological foundries capable of capturing the \$7.0 Trillion petrochemical, specialty chemical, and synthetic nutrition markets.

---

## 1. Thermodynamic and Volumetric Truths of Biology

Software scales infinitely at near-zero marginal cost, but physical biological matter is bound by physics:
1. **The Titer Ceiling**: Maximum microbial yield is dictated by metabolic toxicity and osmotic pressure. Operations must sustain $\ge 85.0\text{ g/L}$ titers.
2. **Volumetric Productivity**: $Q_p \ge 1.5\text{ g/L}\cdot\text{h}$ is required to beat petrochemical distillation columns on pure unit economics.
3. **Oxygen & Heat Dissipation**: High-density aerobic fermentation generates intense metabolic heat (~$460\text{ kJ/mol } O_2$), requiring direct integration with clean nuclear cooling loops or high-efficiency heat exchangers.

---

## 2. The Bioma Economic Flywheel

$$\text{Unit Cost (\$/kg)} = \frac{\text{Feedstock Cost} + \text{Utility Cost (Steam + Electricity)} + \text{Labor/Capex Amortization}}{\text{Titer (g/L)} \times \text{Downstream Recovery Yield (\%)}}$$

To capture commodity scale:
- Years 1–3: High-value pharmaceuticals, enzymes, and specialized cosmetic lipids (\$120–\$250/kg).
- Years 4–7: Industrial bio-monomers, performance proteins, and specialty lubricants (\$35–\$75/kg).
- Years 8–10: High-volume synthetic aviation fuels, biodegradable polymers, and bulk commodity fats (\$18–\$25/kg).

---

## 3. Autonomous Execution Protocol

When invoked, the agent must:
1. Synthesize targeted construct sequences and verify thermodynamic stability via [`DNACompiler`](file:///e:/anti/bioma_foundry/dna_compiler.py#L22).
2. Compute multi-year capacity curves, revenue projections, and FCF generation via [`BiomaEconomicEngine`](file:///e:/anti/bioma_foundry/bioreactor_economics.py#L22).
3. Validate downstream recovery efficiency: reject genetic strains with recovery yield $< 88\%$.
4. Check whether electrical demand from mega-bioreactor agitation is coupled to dedicated micro-SMR nuclear baseload via [`AetherVentureCalculator`](file:///e:/anti/aether_energy/ppa_tollbooth_calculator.py#L22).
5. Output production dispatch directive:
   `Bio Foundry Ruling: Strain: <ID> — Target Titer: <g/L> — Projected Cost: $<usd>/kg — FCF Margin: <pct>%`.
