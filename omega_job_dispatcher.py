"""
OMEGA JOB DISPATCHER ROOT ENTRYPOINT
Routes commands directly to omega.engines.omega_job_dispatcher
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omega.engines.omega_job_dispatcher import main

if __name__ == "__main__":
    main()
