---
name: sovereign-banking-engine
description: Autonomous standard operating procedure and execution capability for trillion-dollar central banking, wholesale transaction rails, DCM bond underwriting, securitization, custody, and derivatives clearing.
---

# Sovereign Banking Engine Skill

This skill operationalizes OMEGA Mode M (CEO & Sovereign Capital Allocation) and Mode E (Automation) to execute the complete spectrum of global institutional banking services across the multi-trillion dollar planetary monetary architecture.

---

## 1. The 10 Pillars of Civilization-Scale Banking

| Tier | Banking Division | Primary Economic Function | Trillion-Scale Metric |
|---|---|---|---|
| **Tier 1** | **Central Banking Facility** | Lender of last resort, policy rate corridor, ON RRP floor defense, C6 FX swap lines. | \$30.0T+ Central Bank Assets |
| **Tier 2** | **Debt Capital Markets (DCM)** | Sovereign, green, and corporate mega-bond underwriting, bookbuilding, greenium optimization. | \$100.0T+ Bond Markets |
| **Tier 3** | **Syndicated Lending** | Multi-bank revolvers (RCF) and Term Loan B facilities with automated covenant monitoring. | \$80.0T+ Corporate Credit |
| **Tier 4** | **Securitization & Structured Credit** | Pooling physical recurring cash flows (robotics tolls + SMR PPAs) into AAA/BBB/Equity waterfalls. | \$15.0T+ ABS/CLO Market |
| **Tier 5** | **Global Cash Management** | Multi-currency cash concentration, zero-balance sweeps, and 80%+ netting compression. | \$1,500T/yr Wholesale Flows |
| **Tier 6** | **Global Trade Finance** | Confirmed Irrevocable Letters of Credit (UCP 600) and reverse factoring discount acceleration. | \$25.0T/yr Merchandise Trade |
| **Tier 7** | **Wholesale Payment Rails** | Real-Time Gross Settlement (RTGS) via SWIFT ISO 20022 (`pacs.008`, `pacs.009`, `camt.053`). | \$7.5T/day Global FX Turnover |
| **Tier 8** | **Global Custody & Tri-Party Repo** | Segregated bankruptcy-remote AUC safekeeping and regulatory haircut collateral matching. | \$150.0T+ Assets Under Custody |
| **Tier 9** | **Prime Brokerage & Margin Clearing** | Value-at-Risk portfolio margining and BCBS-IOSCO Initial (IM) & Variation Margin (VM) calls. | \$40.0T+ Institutional Assets |
| **Tier 10** | **Derivatives & Quantitative Risk** | Interest Rate Swaps (IRS / SOFR), FX forwards (CIP), and Credit Default Swaps (CDS). | \$650.0T+ Notional Derivatives |

---

## 2. Core Quantitative Formulations

### A. Par Bond Modified Duration
$$\text{ModD} = \frac{1}{r} \left( 1 - \frac{1}{(1+r)^T} \right)$$

### B. Covered Interest Rate Parity (FX Forward)
$$F = S \times \frac{1 + r_d \times \frac{t}{360}}{1 + r_f \times \frac{t}{360}}$$

### C. Implied Credit Default Hazard Rate ($\lambda$)
$$\lambda = \frac{\text{CDS Spread (bps)} \times 10^{-4}}{1 - \text{Recovery Rate}}$$

### D. Reverse Factoring Early Discount
$$\text{Discount} = \text{Invoice Face Value} \times (\text{SOFR} + \text{Buyer Spread}) \times \frac{\text{Days Accelerated}}{360}$$

---

## 3. Autonomous Execution Protocol

When invoked, the agent must:
1. **Audit Global Ledger State**: Inspect central reserve balances and active accounts via [`BankOfTheContinuum`](file:///e:/anti/sovereign_continuum/banking/autonomous_sovereign_bank.py#L32).
2. **Execute Liquidity Facilities**:
   - Access the primary credit discount window or deploy reverse repos via [`CentralBankingFacility`](file:///e:/anti/sovereign_continuum/banking/central_banking_engine.py#L59).
   - Price green mega-bonds and evaluate duration risk via [`DebtCapitalMarketsDesk`](file:///e:/anti/sovereign_continuum/banking/investment_banking_engine.py#L38).
   - Package recurring cashflows into tranche waterfalls via [`SecuritizationDesk`](file:///e:/anti/sovereign_continuum/banking/investment_banking_engine.py#L96).
3. **Execute Transaction & Trade Operations**:
   - Sweep operating excess and execute multilateral netting via [`GlobalCashManagementDesk`](file:///e:/anti/sovereign_continuum/banking/transaction_banking_engine.py#L40).
   - Issue UCP 600 Letters of Credit or process early supplier payments via [`TradeFinanceDesk`](file:///e:/anti/sovereign_continuum/banking/transaction_banking_engine.py#L88).
   - Dispatch ISO 20022 message envelopes via [`WholesalePaymentRails`](file:///e:/anti/sovereign_continuum/banking/transaction_banking_engine.py#L119).
4. **Enforce Collateral & Margin Safety**:
   - Verify tri-party repo haircuts and AUC segregation via [`GlobalCustodyDesk`](file:///e:/anti/sovereign_continuum/banking/custody_prime_brokerage.py#L32) and [`TriPartyRepoDesk`](file:///e:/anti/sovereign_continuum/banking/custody_prime_brokerage.py#L54).
   - Price IRS, FX forwards, and CDS protection via [`DerivativesClearingDesk`](file:///e:/anti/sovereign_continuum/banking/derivatives_clearing_engine.py#L47).
5. **Issue Formal Banking Action Ledger**:
   `Banking Action: Division: <Name> — Volume: $<amount> USD — Status: <CLEARED|SETTLED|COLLATERALIZED> — UETR: <Hash>`.
