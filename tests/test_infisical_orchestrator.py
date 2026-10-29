"""
Unit and Integration Tests for Infisical Sovereign SecretOps Orchestrator
========================================================================
Validates cryptographic integrity, AES-256-GCM encryption, secret versioning,
rollback mechanisms, leak scanning, dynamic leases, PKI/CA issuance,
cloud synchronization, and tamper-evident audit blockchain.
"""

import os
import sys
import unittest
import tempfile
import json

from infisical_orchestrator import (
    CryptographicEngine,
    SecretScannerEngine,
    InfisicalConfig,
    InfisicalClient,
    InfisicalOrchestrator,
)


class TestInfisicalOrchestrator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_file = os.path.join(self.temp_dir.name, "test_vault.json")
        self.config = InfisicalConfig(
            project_id="test-proj-001",
            environment="production",
            vault_file=self.vault_file,
            mock_mode=True,
        )
        self.client = InfisicalClient(self.config)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_crypto_engine_aes256_gcm(self):
        """Test AES-256-GCM authenticated encryption and decryption."""
        crypto = CryptographicEngine(master_password="test-omega-secret-key")
        plaintext = "SUPER_SECRET_PAYLOAD_12345"
        ad = "project:env:key"

        ct_b64, nonce_b64, tag_b64 = crypto.encrypt_secret(plaintext, associated_data=ad)
        self.assertNotEqual(plaintext, ct_b64)
        self.assertTrue(len(nonce_b64) > 0)
        self.assertTrue(len(tag_b64) > 0)

        decrypted = crypto.decrypt_secret(ct_b64, nonce_b64, tag_b64, associated_data=ad)
        self.assertEqual(plaintext, decrypted)

        # Verify tampering with ciphertext triggers validation failure
        tampered_ct = ct_b64[:-2] + "AA"
        with self.assertRaises(Exception):
            crypto.decrypt_secret(tampered_ct, nonce_b64, tag_b64, associated_data=ad)

    def test_02_secret_versioning_and_rollback(self):
        """Test point-in-time version history and rollback mechanism."""
        # Set v1
        s1 = self.client.set_secret("STRIPE_KEY", "sk_live_v1_old_key", comment="v1 initial")
        self.assertEqual(s1["version"], 1)

        # Set v2
        s2 = self.client.set_secret("STRIPE_KEY", "sk_live_v2_new_key", comment="v2 rotated")
        self.assertEqual(s2["version"], 2)

        # Rollback to v1
        rolled = self.client.rollback_secret("STRIPE_KEY", target_version=1)
        self.assertIsNotNone(rolled)
        self.assertEqual(rolled["version"], 3)  # increments version upon rollback
        self.assertEqual(rolled["value"], "sk_live_v1_old_key")

    def test_03_high_entropy_secret_scanner(self):
        """Test regex pattern detection and Shannon entropy calculation."""
        scanner = SecretScannerEngine()
        code_sample = """
        const aws_key = "AKIAIOSFODNN7EXAMPLE";
        const gh_token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz";
        const stripe_key = "sk_live_51OzK9x8Lm3N2vP1qR4sT5uV6";
        """
        matches = scanner.scan_text(code_sample, file_path="test.js")
        self.assertGreaterEqual(len(matches), 3)

        rule_names = [m.rule_name for m in matches]
        self.assertIn("AWS Access Key ID", rule_names)
        self.assertIn("GitHub Personal Access Token (Classic)", rule_names)
        self.assertIn("Stripe Live Secret Key", rule_names)

        for m in matches:
            self.assertGreater(m.entropy, 2.5)

    def test_04_dynamic_secrets_lifecycle(self):
        """Test ephemeral dynamic credential generation and revocation."""
        lease = self.client.create_dynamic_secret_lease("core-postgres", engine_type="postgres", ttl_seconds=1800)
        self.assertEqual(lease["status"], "active")
        self.assertTrue(lease["username"].startswith("inf_dyn_postgres_"))
        self.assertTrue(len(lease["password"]) >= 20)

        # Revoke lease
        revoked = self.client.revoke_dynamic_lease(lease["lease_id"])
        self.assertTrue(revoked)

        all_leases = self.client.list_dynamic_leases()
        revoked_item = next(l for l in all_leases if l["lease_id"] == lease["lease_id"])
        self.assertEqual(revoked_item["status"], "revoked")

    def test_05_internal_pki_ca_and_cert_issuance(self):
        """Test Root CA generation and X.509 leaf TLS certificate issuance."""
        cert = self.client.issue_tls_certificate(
            common_name="gateway.omega.internal",
            sans=["gateway.omega.internal", "localhost"],
            validity_days=30
        )
        self.assertEqual(cert["subject_cn"], "gateway.omega.internal")
        self.assertEqual(cert["status"], "active")
        self.assertTrue("BEGIN CERTIFICATE" in cert["cert_pem"])
        self.assertTrue(len(cert["serial_number"]) > 0)

        # Revoke cert
        rev_ok = self.client.revoke_certificate(cert["serial_number"], reason="KeyCompromise")
        self.assertTrue(rev_ok)

    def test_06_cloud_integration_sync(self):
        """Test secret sync dispatch formatting for Kubernetes and AWS."""
        integrations = self.client.list_integrations()
        self.assertGreater(len(integrations), 0)

        k8s_integ = next((i for i in integrations if i["target"] == "kubernetes"), None)
        self.assertIsNotNone(k8s_integ)

        res = self.client.sync_integration(k8s_integ["id"])
        self.assertEqual(res["sync_status"], "synchronized")
        self.assertGreater(res["synced_keys_count"], 0)
        self.assertTrue("apiVersion: v1" in res["exported_manifest"])

    def test_07_audit_blockchain_integrity(self):
        """Test SHA-256 chained hash integrity and tamper detection."""
        # Baseline check
        valid, count, err = self.client.state.verify_audit_chain()
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Inject a malicious mutation into history
        original_action = self.client.state.audit_log[1].action
        self.client.state.audit_log[1].action = "MALICIOUS_TAMPERED_ACTION"
        tampered_valid, _, tampered_err = self.client.state.verify_audit_chain()
        self.assertFalse(tampered_valid)
        self.assertIsNotNone(tampered_err)

        # Restore
        self.client.state.audit_log[1].action = original_action
        restored_valid, _, _ = self.client.state.verify_audit_chain()
        self.assertTrue(restored_valid)

    def test_08_sovereign_12_phase_lifecycle(self):
        """Test complete 12-phase execution and manifest generation."""
        orch = InfisicalOrchestrator(self.client)
        manifest = orch.do_everything()
        self.assertEqual(manifest["overall_status"], "SUCCESS_100_PERCENT")
        self.assertEqual(manifest["phases_completed"], 12)
        self.assertEqual(manifest["phases_total"], 12)
        self.assertTrue(len(manifest["cryptographic_ledger_signature"]) == 64)


if __name__ == "__main__":
    unittest.main()
