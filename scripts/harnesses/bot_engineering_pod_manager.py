"""
Build-Operate-Transfer (BOT) Engineering Pod Manager
Calculates deployment economics, sprint velocity, margin models,
and Month-12 enterprise absorption transfer fees for Bangalore GCC capability centers.
"""

class BOTEngineeringPodManager:
    def __init__(self, pod_name, target_gcc, sprint_cadence_days=14):
        self.pod_name = pod_name
        self.target_gcc = target_gcc
        self.sprint_cadence_days = sprint_cadence_days
        self.engineers = []

    def add_engineer(self, role, seniority, base_annual_ctc_inr, monthly_bill_rate_inr):
        self.engineers.append({
            "role": role,
            "seniority": seniority,
            "annual_ctc_inr": base_annual_ctc_inr,
            "monthly_bill_rate_inr": monthly_bill_rate_inr
        })

    def calculate_pod_economics(self, contract_duration_months=12, transfer_fee_percentage=0.15):
        total_monthly_billing = sum(e["monthly_bill_rate_inr"] for e in self.engineers)
        total_monthly_payroll_cost = sum(e["annual_ctc_inr"] / 12 for e in self.engineers)
        gross_monthly_margin = total_monthly_billing - total_monthly_payroll_cost
        gross_margin_percentage = (gross_monthly_margin / total_monthly_billing) * 100 if total_monthly_billing > 0 else 0
        
        annual_pod_revenue = total_monthly_billing * contract_duration_months
        total_transfer_fee = sum(e["annual_ctc_inr"] * transfer_fee_percentage for e in self.engineers)
        total_lifetime_deal_value = annual_pod_revenue + total_transfer_fee
        
        return {
            "pod_name": self.pod_name,
            "target_gcc": self.target_gcc,
            "headcount": len(self.engineers),
            "total_monthly_billing_inr": total_monthly_billing,
            "gross_monthly_margin_inr": gross_monthly_margin,
            "gross_margin_percentage": round(gross_margin_percentage, 1),
            "12_month_contract_revenue_inr": annual_pod_revenue,
            "month_12_absorption_transfer_fee_inr": total_transfer_fee,
            "total_lifetime_deal_value_inr": total_lifetime_deal_value,
            "total_lifetime_deal_value_usd": round(total_lifetime_deal_value / 83.5, 2)
        }

if __name__ == "__main__":
    # Example: Specialized Distributed Systems / AI Infra Pod for Intel India or Cisco Systems
    manager = BOTEngineeringPodManager(
        pod_name="Omega Distributed AI Infra Pod",
        target_gcc="Intel India Technology Center / Cisco Systems"
    )
    
    manager.add_engineer("Principal Rust & CUDA Engineer", "L6 / Staff", base_annual_ctc_inr=4200000, monthly_bill_rate_inr=650000)
    manager.add_engineer("Senior Distributed Systems Engineer", "L5 / Senior", base_annual_ctc_inr=3200000, monthly_bill_rate_inr=500000)
    manager.add_engineer("AI Platform & Triton Inference Specialist", "L5 / Senior", base_annual_ctc_inr=3000000, monthly_bill_rate_inr=480000)
    manager.add_engineer("Full-Stack Observability & CI/CD Lead", "L4 / SDE-2", base_annual_ctc_inr=2200000, monthly_bill_rate_inr=350000)
    
    econ = manager.calculate_pod_economics()
    
    print("=== BUILD-OPERATE-TRANSFER (BOT) POD ECONOMICS ===")
    print(f"Target GCC: {econ['target_gcc']}")
    print(f"Pod Sizing: {econ['headcount']} Elite Engineers")
    print(f"Monthly Pod Billing: INR {econ['total_monthly_billing_inr']:,}")
    print(f"Gross Monthly Margin: INR {econ['gross_monthly_margin_inr']:,} ({econ['gross_margin_percentage']}%)")
    print(f"12-Month Pod Contract Value: INR {econ['12_month_contract_revenue_inr']:,}")
    print(f"Month-12 Transfer / Absorption Fee: INR {econ['month_12_absorption_transfer_fee_inr']:,}")
    print(f"TOTAL LIFETIME CONTRACT VALUE: INR {econ['total_lifetime_deal_value_inr']:,} (~${econ['total_lifetime_deal_value_usd']:,} USD)")
