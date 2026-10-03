---
name: distilled-port-conflict-resolution
description: Resolution protocol for port binding collisions on Windows
---

# distilled-port-conflict-resolution — Autonomous Distilled Skill

**Distilled Origin**: OMEGA Autonomous Learning Engine (Mode L)  
**Verification Level**: Cryptographically Stamped & Validated  

## Core Standard Operating Procedure
1. Query port using netstat -ano | findstr <port>\n2. Identify PID\n3. Terminate cleanly or rebind to alternative port.

## Heuristics & Execution Guidelines
- Strictly prioritize zero-dependency standard library solutions.
- Test changes immediately with targeted unit tests (Red-Green-Refactor).
- Log all decisions into the system audit trail.


