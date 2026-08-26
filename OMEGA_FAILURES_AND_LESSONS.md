# OMEGA FAILURES & ARCHITECTURAL LESSONS

### Lesson 1: Never Allow Seed Data to Enter Confirmed States
- **Failure**: Initial release marked 20 seeded template jobs as `CONFIRMED_OPENING` upon module import.
- **Discovery**: Reality Audit probed URLs and found 9 broken links / 404s.
- **Fix**: Isolated seed data to `SEEDED_NOT_VERIFIED`. Only live HTTP 200 probes can elevate a job to `CONFIRMED_OPENING`.

### Lesson 2: Test Fixtures Must Not Pollute Production State
- **Failure**: Unit test execution generated a mock submission receipt and left an application in `SUBMITTED` state.
- **Discovery**: Reality Audit caught the test receipt reference.
- **Fix**: Created `ApplicationProofEngine` to downgrade unproven submissions to `READY` and reset test applications.

### Lesson 3: Loud Failure is Better Than Silent Simulation
- **Failure**: Early router fell back to simulated mock strings when models were offline.
- **Fix**: Replaced all silent mocks with explicit loud failures.
