# ANTIGRAVITY OMNIVERSE: DATA ARCHITECTURE & KNOWLEDGE FABRIC
## Document ID: `OMNIVERSE-06-DATA` | Status: APPROVED | Mode: OMNI-X PRODUCTION

---

## 1. Universal Data Fabric Architecture

The Omniverse Data Fabric provides a unified access, storage, and lineage layer across all structured and unstructured data assets:
- Relational SQLite WAL stores (`omega_platform.db`, `nexus.db`, `sovereign_platform.db`)
- Knowledge Graph Engine with 17 first-class entities and 18 typed relations
- Normalized Vector Embedding Store for semantic RAG and skill matching
- Multi-tier memory engine spanning 7 cognitive layers

---

## 2. Standard Provenance Metadata Envelope

Every record or document entering the Omniverse fabric is wrapped in an immutable Provenance Envelope:
- `data_id`: Unique identifier
- `source`: Authoritative origin
- `source_url`: Verifiable URL
- `source_date`: Publication date
- `license`: Usage and attribution license
- `confidence_score`: Score between 0.0 and 1.0
- `transformation_history`: Complete pipeline lineage
- `access_policy`: Permission constraint
- `last_verified`: Timestamp of verification
- `cryptographic_sha256`: Tamper-evident checksum

---

## 3. Global Knowledge Graph Schema

- **17 Entities**: Company, Person, Product, Technology, Country, City, Industry, Market, Dataset, Organization, Regulation, Patent, ResearchPaper, Project, Software, API, EconomicIndicator.
- **18 Relations**: OWNS, BUILDS, COMPETES_WITH, PARTNERS_WITH, ACQUIRED, INVESTED_IN, USES, DEPENDS_ON, LOCATED_IN, SERVES, EMPLOYS, FUNDED_BY, RELATED_TO, DERIVED_FROM, CITES, MEASURES, CAUSES, CORRELATES_WITH.

---

## 4. The 7-Tier Memory Architecture

- Working Memory: Current process state
- Project Memory: Active mission & WBS status
- Long-Term Memory: User preferences & verified profile
- Organizational Memory: Cross-mission rules & Codex
- Technical Memory: Tool directory & API contracts
- Decision Memory: Rulings & trade-off records
- Failure Memory: Post-mortem insights & bug patterns
