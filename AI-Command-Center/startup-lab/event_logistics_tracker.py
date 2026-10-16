"""
=============================================================================
EVENT LOGISTICS SLA & BUDGET TRACKER
Autonomous Operational Margin & Vendor Penalty Calculation Engine
Specialized for Bengaluru Corporate Summits, Conferences & Live Productions
=============================================================================
"""

from typing import Any


class EventLogisticsTracker:
    def __init__(self, event_name: str, budget_inr: float):
        self.event_name = event_name
        self.budget_inr = budget_inr
        self.milestones: list[dict[str, Any]] = []
        self.vendors: list[dict[str, Any]] = []

    def add_vendor(
        self,
        vendor_id: str,
        name: str,
        category: str,
        contracted_amount: float,
        hourly_delay_penalty_rate: float = 0.05,
    ):
        """
        hourly_delay_penalty_rate: Default 5% contractual penalty per hour of unapproved handover delay.
        """
        self.vendors.append(
            {
                "vendor_id": vendor_id,
                "name": name,
                "category": category,
                "contracted_amount": contracted_amount,
                "hourly_delay_penalty_rate": hourly_delay_penalty_rate,
                "actual_delay_hours": 0.0,
                "penalties_applied": 0.0,
                "final_payable": contracted_amount,
                "status": "ACTIVE",
            }
        )

    def record_vendor_delay(self, vendor_id: str, delay_hours: float):
        for v in self.vendors:
            if v["vendor_id"] == vendor_id:
                v["actual_delay_hours"] = max(0.0, delay_hours)
                penalty_amount = v["contracted_amount"] * (
                    v["hourly_delay_penalty_rate"] * v["actual_delay_hours"]
                )
                # Cap penalty at 30% of total contract value
                penalty_amount = min(penalty_amount, v["contracted_amount"] * 0.30)
                v["penalties_applied"] = round(penalty_amount, 2)
                v["final_payable"] = round(v["contracted_amount"] - penalty_amount, 2)
                return v
        raise ValueError(f"Vendor ID {vendor_id} not found.")

    def add_milestone(
        self,
        milestone_id: str,
        description: str,
        target_time: str,
        owner_vendor_id: str,
    ):
        self.milestones.append(
            {
                "milestone_id": milestone_id,
                "description": description,
                "target_time": target_time,
                "owner_vendor_id": owner_vendor_id,
                "status": "PENDING",
            }
        )

    def complete_milestone(
        self, milestone_id: str, completed_at: str, delay_hours: float = 0.0
    ):
        for m in self.milestones:
            if m["milestone_id"] == milestone_id:
                m["status"] = "COMPLETED"
                m["completed_at"] = completed_at
                m["delay_hours"] = delay_hours
                if delay_hours > 0 and m["owner_vendor_id"]:
                    self.record_vendor_delay(m["owner_vendor_id"], delay_hours)
                return m
        raise ValueError(f"Milestone ID {milestone_id} not found.")

    def generate_financial_audit(self) -> dict[str, Any]:
        total_contracted = sum(v["contracted_amount"] for v in self.vendors)
        total_penalties = sum(v["penalties_applied"] for v in self.vendors)
        final_expenditure = sum(v["final_payable"] for v in self.vendors)
        budget_variance = self.budget_inr - final_expenditure
        cost_savings_pct = (
            (total_penalties / total_contracted * 100.0)
            if total_contracted > 0
            else 0.0
        )

        return {
            "event_name": self.event_name,
            "total_budget_inr": self.budget_inr,
            "total_contracted_inr": total_contracted,
            "total_penalties_recovered_inr": total_penalties,
            "net_final_expenditure_inr": final_expenditure,
            "net_budget_savings_inr": budget_variance,
            "sla_recovery_rate_pct": round(cost_savings_pct, 2),
            "vendors_summary": self.vendors,
            "milestones_count": len(self.milestones),
        }


if __name__ == "__main__":
    tracker = EventLogisticsTracker(
        "Bengaluru AI Technology Summit 2026", budget_inr=1500000.0
    )

    # Add vendors
    tracker.add_vendor(
        "VEND-AV-01",
        "Apex Audio Visuals Pvt Ltd",
        "AV & LED Screens",
        contracted_amount=450000.0,
        hourly_delay_penalty_rate=0.05,
    )
    tracker.add_vendor(
        "VEND-STG-02",
        "Karnataka Staging & Fabrication",
        "Staging & Set Design",
        contracted_amount=380000.0,
        hourly_delay_penalty_rate=0.05,
    )
    tracker.add_vendor(
        "VEND-PWR-03",
        "Bangalore GenPower Solutions",
        "Silent Generators & Power",
        contracted_amount=120000.0,
        hourly_delay_penalty_rate=0.05,
    )
    tracker.add_vendor(
        "VEND-CAT-04",
        "Royal Corporate Caterers",
        "Food & Beverage",
        contracted_amount=350000.0,
        hourly_delay_penalty_rate=0.05,
    )

    # Add milestones
    tracker.add_milestone(
        "M1_LOADIN", "Venue Load-in & Power Grid Setup", "06:00 AM", "VEND-PWR-03"
    )
    tracker.add_milestone(
        "M2_STAGE", "Stage Truss & Backdrop Handover", "09:30 AM", "VEND-STG-02"
    )
    tracker.add_milestone(
        "M3_AV_COMMISSION",
        "4K LED Wall Testing & Audio Calibration",
        "11:00 AM",
        "VEND-AV-01",
    )
    tracker.add_milestone("M4_GUEST_ENTRY", "Main Hall Doors Open", "01:00 PM", "")

    # Execute simulation: Stage fabrication is delayed by 1.5 hours
    tracker.complete_milestone("M1_LOADIN", "06:15 AM", delay_hours=0.0)
    tracker.complete_milestone(
        "M2_STAGE", "11:00 AM", delay_hours=1.5
    )  # 1.5h delay applies 7.5% penalty
    tracker.complete_milestone("M3_AV_COMMISSION", "12:15 PM", delay_hours=0.0)
    tracker.complete_milestone("M4_GUEST_ENTRY", "01:00 PM", delay_hours=0.0)

    audit = tracker.generate_financial_audit()
    print("=== EVENT LOGISTICS SLA AUDIT RESULTS ===")
    print(f"Event: {audit['event_name']}")
    print(f"Original Budget: INR {audit['total_budget_inr']:,.2f}")
    print(f"Contracted Cost: INR {audit['total_contracted_inr']:,.2f}")
    print(f"SLA Penalties Recovered: INR {audit['total_penalties_recovered_inr']:,.2f}")
    print(f"Final Payable Expenditure: INR {audit['net_final_expenditure_inr']:,.2f}")
    print(f"Net Savings Below Budget: INR {audit['net_budget_savings_inr']:,.2f}")
    print(f"Recovery Rate: {audit['sla_recovery_rate_pct']}%")
