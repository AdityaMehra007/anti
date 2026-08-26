# 🎯 PILLAR 1: BBA INTERNATIONAL BUSINESS CAREER MASTERPACK
**Target Role:** International Supply Chain Analyst @ Walmart Global Tech  
**Match Score:** 58.0%  
**Location:** Kadubeesanahalli (ORR) | **Compensation:** ₹8.5 - ₹12 LPA  

---

## 1. Resume Positioning & Key Value Proposition
- **Headline:** *BBA International Business Graduate specializing in AI-driven Supply Chain Analytics, Incoterms 2020 Compliance, and Cross-Border Landed Cost Optimization.*
- **Core Quantified Bullet 1:** *Automated tariff and customs landed-cost modeling, reducing scenario evaluation latency by 85%.*
- **Core Quantified Bullet 2:** *Built parametric safety stock models cutting simulated assembly line stockout risk from 42% to 0.5%.*

---

## 2. 3-Round Case Study Interview Intelligence
### Round 1: Core Trade & Incoterms Technical Case
- **Question:** *A supplier in Vietnam quotes FOB Da Nang, while another in Shenzhen quotes CIF Nhava Sheva. Freight rates are $3,200/FEU. How do you evaluate the true landed cost under Indian 40% BCD tariffs?*
- **Optimal Answer Framework:** Calculate Freight-per-watt ($0.0038/Wp), apply Basic Customs Duty (BCD) on Assessable Value (CIF + Landing charges), factor in IGST (18%), and calculate net working capital drag.

### Round 2: Data & SQL Analytical Drill
- **Question:** *How would you query an enterprise shipment database to identify suppliers with lead-time standard deviations > 15 days?*
- **Answer:** `SELECT supplier_id, AVG(lead_days), STDDEV(lead_days) FROM manifests GROUP BY supplier_id HAVING STDDEV(lead_days) > 15;`

### Round 3: Executive Behavioral & Ownership Case
- **Question:** *Nhava Sheva port customs has delayed 15 containers of critical components. The assembly plant in Karnataka faces shutdown in 48 hours. What is your action plan?*
- **Action Plan:** 1. Activate dual-source bonded warehouse buffer. 2. File for expedited customs clearance under AEO (Authorized Economic Operator) tier. 3. Re-route emergency air freight for high-value critical ICs.
