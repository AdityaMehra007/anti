"""
Local Verification Runner for Bengaluru Referral Strike Dockets
"""

import os
import sys

# Add scripts directory to path and run verification
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from verify_referral_strike import TestReferralStrikeR1R2
import unittest

if __name__ == '__main__':
    unittest.main()
