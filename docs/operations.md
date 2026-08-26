# 🛡️ OMEGA SECURITY & PERMISSIONS MODEL

## 1. Principles
* **Least Privilege:** Specialized agents can only request actions within their domain.
* **Approval Gates:** Production financial transfers and external government submissions require human sign-off via `OmegaApprovalEngine`.
* **Zero Secrets in Git:** Sensitive API tokens are loaded strictly via environment variables.

---

# 🔄 OMEGA DISASTER RECOVERY & INCIDENT PLAYBOOK

## 1. Mismatch Incident Protocol
* When `OmegaReconciliationEngine` detects a field mismatch, an automatic incident is created (`INC-<TX_ID>`).
* Downstream automated retries are halted until reviewed.

---

# 🕹️ OMEGA OPERATIONS & RUNBOOKS

## Master Run Commands
* **Run Gateway Certification:** `python e:\anti\omega_gateway_certifier.py`
* **Run Omniverse 151-Test Battery:** `python e:\anti\run_master_omniverse_verification.py`
* **Run Control Plane Test Suite:** `python e:\anti\apex\control_plane\tests\test_omega_control_plane.py`
* **Launch Control Tower:** `Start-Process "e:\anti\deploy\omega_control_tower.html"`
