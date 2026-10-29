"""
Bengaluru Referral Strike Matcher & Docket Synthesis Engine
Aligns live Bengaluru openings with verified LinkedIn employee & recruiter contacts for Aditya Mehra.
Delegates to build_verified_referral_dockets to ensure all 11 mandated employers and verified contacts are maintained.
"""

import os
import sys

# Add scripts directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from build_verified_referral_dockets import (
    generate_dockets,
    build_connection_note,
    build_referral_ask,
    build_referral_docket,
    clean_first_name,
    clean_full_name,
    CORE_11_MANDATES
)


def main():
    return generate_dockets()


if __name__ == '__main__':
    main()
