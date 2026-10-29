"""
CS Courses Roadmaps Engine - Curated Degree-Grade Career Pathways
Synthesizes university-level curricula for 9 high-impact technology disciplines
using verified courses from Developer-Y/cs-video-courses.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3

WORKSPACE_ROOT = Path(__file__).resolve().parent
DATA_DIR = WORKSPACE_ROOT / "data"
ROADMAPS_JSON_PATH = DATA_DIR / "cs_role_roadmaps.json"
CURRICULA_DIR = WORKSPACE_ROOT / "docs" / "curricula"
DB_PATH = DATA_DIR / "cs_video_courses.db"

ROLE_DEFINITIONS = [
    {
        "role_id": "genai-llm-engineer",
        "title": "Generative AI & LLM Systems Engineer",
        "description": "Master transformer architectures, large language model fine-tuning, retrieval systems, GPU distributed training, and deep probabilistic generative models.",
        "tiers": [
            {
                "tier_name": "Tier 1: Mathematical Foundations & Programming",
                "level": "Introductory (L1)",
                "target_queries": ["Linear Algebra", "Python", "Multivariable Calculus", "Computational Thinking"],
                "required_competencies": ["Linear Algebra (Strang matrix decomposition)", "Vector Calculus", "High-performance Python"]
            },
            {
                "tier_name": "Tier 2: Core Machine Learning & Probability",
                "level": "Core Intermediate (L2)",
                "target_queries": ["CS 229", "10-601", "Statistical Learning", "Probabilistic Graphical"],
                "required_competencies": ["Supervised/Unsupervised learning proofs", "Bayesian inference", "Convex optimization"]
            },
            {
                "tier_name": "Tier 3: Deep Learning, CNNs & Sequence Models",
                "level": "Advanced (L3)",
                "target_queries": ["CS231n", "CS224N", "Deep Learning", "Neural Networks"],
                "required_competencies": ["Backpropagation engines", "Attention mechanisms", "PyTorch autograd semantics"]
            },
            {
                "tier_name": "Tier 4: Transformers, Diffusion & LLM Infrastructure",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Transformers United", "Deep Generative Models", "Large Scale Machine Learning", "CS25"],
                "required_competencies": ["Transformer scaling laws", "Diffusion formulation", "Distributed tensor parallelism"]
            }
        ]
    },
    {
        "role_id": "systems-distributed-engineer",
        "title": "Systems & Distributed Infrastructure Architect",
        "description": "Architect planetary-scale cloud systems, low-latency operating system kernels, distributed consensus protocols (Raft/Paxos), and high-throughput networking.",
        "tiers": [
            {
                "tier_name": "Tier 1: Systems Programming & C/Rust Fundamentals",
                "level": "Introductory (L1)",
                "target_queries": ["Rust Programming", "Computer Programming", "Programming Paradigms", "CS 107"],
                "required_competencies": ["Manual memory management", "Pointers and ABI", "Rust ownership and concurrency"]
            },
            {
                "tier_name": "Tier 2: Computer Systems & Architecture",
                "level": "Core Intermediate (L2)",
                "target_queries": ["15-213", "Computer Systems", "Machine Organization", "Computer Architecture"],
                "required_competencies": ["x86/ARM assembly", "CPU caching hierarchy", "Virtual memory paging"]
            },
            {
                "tier_name": "Tier 3: Operating Systems Internals & Networking",
                "level": "Advanced (L3)",
                "target_queries": ["CS 162", "Operating Systems", "CS 144", "Computer Networks"],
                "required_competencies": ["Thread scheduling & synchronization primitives", "TCP/IP implementation", "File systems & VFS"]
            },
            {
                "tier_name": "Tier 4: Distributed Systems & Planetary Consensus",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["6.824", "Distributed Systems", "Distributed Operating Systems", "CS 677"],
                "required_competencies": ["Raft consensus engine", "Linearizability & CAP theorem", "Two-phase commit & fault tolerance"]
            }
        ]
    },
    {
        "role_id": "database-storage-architect",
        "title": "Database Engine & Storage Systems Architect",
        "description": "Design high-performance relational storage managers, B-Tree and LSM indexing engines, buffer pool managers, vector databases, and distributed query execution.",
        "tiers": [
            {
                "tier_name": "Tier 1: Algorithms & Data Structures Core",
                "level": "Introductory (L1)",
                "target_queries": ["CS 61B", "Data Structures", "Programming Fundamentals", "Sedgewick"],
                "required_competencies": ["Hash tables & trees", "Algorithmic complexity", "Memory bounds"]
            },
            {
                "tier_name": "Tier 2: Relational Theory & Database Systems",
                "level": "Core Intermediate (L2)",
                "target_queries": ["Database Management Systems", "Database Systems", "Penn State", "Relational"],
                "required_competencies": ["Relational algebra", "SQL internals & normalization", "Index lookups"]
            },
            {
                "tier_name": "Tier 3: Database Internals & Storage Managers",
                "level": "Advanced (L3)",
                "target_queries": ["15-445", "Database Systems - Fall", "Andy Pavlo", "Concurrency"],
                "required_competencies": ["Disk-oriented storage engines", "B+ Trees & Hash indices", "Buffer pool replacement (LRU/Clock)"]
            },
            {
                "tier_name": "Tier 4: Advanced OLAP, Vector & Distributed DBMS",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["15-721", "Advanced Database", "Large Datasets", "Distributed Systems"],
                "required_competencies": ["Vectorized & columnar execution", "Write-Ahead Logging & ARIES recovery", "Multi-version concurrency control (MVCC)"]
            }
        ]
    },
    {
        "role_id": "algorithms-competitive-quant",
        "title": "Algorithms, Theoretical CS & Quantitative Engineer",
        "description": "Master algorithmic problem solving, graph theory, randomized algorithms, NP-completeness, and computational mathematics for quant trading and algorithm optimization.",
        "tiers": [
            {
                "tier_name": "Tier 1: Foundations of Algorithms",
                "level": "Introductory (L1)",
                "target_queries": ["6.006", "CS 161", "Introduction to Algorithms", "Sedgewick"],
                "required_competencies": ["Asymptotic notation", "Sorting & searching bounds", "Basic dynamic programming"]
            },
            {
                "tier_name": "Tier 2: Advanced Design & Graph Algorithms",
                "level": "Core Intermediate (L2)",
                "target_queries": ["6.046J", "Graph Algorithms", "Data Structures and Algorithms", "Algorithms"],
                "required_competencies": ["Network flows (Ford-Fulkerson)", "Greedy algorithm proofs", "Advanced amortized analysis"]
            },
            {
                "tier_name": "Tier 3: Theory of Computation & Discrete Mathematics",
                "level": "Advanced (L3)",
                "target_queries": ["Theory of Computation", "Automata", "Discrete Mathematics", "18.404J"],
                "required_competencies": ["Turing machines & decidability", "P vs NP & Cook-Levin reduction", "Space & time complexity classes"]
            },
            {
                "tier_name": "Tier 4: Approximation, Randomized & Quantum Algorithms",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Approximation Algorithms", "Randomized", "Quantum Computation", "15-859BB"],
                "required_competencies": ["LP relaxation & primal-dual", "Monte Carlo & Las Vegas guarantees", "Quantum circuit complexity"]
            }
        ]
    },
    {
        "role_id": "applied-ml-data-scientist",
        "title": "Applied Machine Learning & Data Scientist",
        "description": "Build production predictive pipelines, statistical hypothesis tests, time-series forecasting, and scalable data mining engines across massive datasets.",
        "tiers": [
            {
                "tier_name": "Tier 1: Python for Data Science & Linear Algebra",
                "level": "Introductory (L1)",
                "target_queries": ["Python Boot Camp", "Computational Linear Algebra", "ROB 101", "Data Science"],
                "required_competencies": ["Numpy/Pandas data vectorization", "Matrix operations", "Exploratory data analysis"]
            },
            {
                "tier_name": "Tier 2: Statistical Modeling & Classical ML",
                "level": "Core Intermediate (L2)",
                "target_queries": ["CS 156", "Learning from Data", "Statistical Learning", "CPSC 340"],
                "required_competencies": ["Vapnik-Chervonenkis (VC) dimension", "Regularization (L1/L2)", "Ensemble methods (Random Forests, XGBoost)"]
            },
            {
                "tier_name": "Tier 3: Mining Massive Datasets & Time Series",
                "level": "Advanced (L3)",
                "target_queries": ["Data Mining", "Applied Machine Learning", "Time Series", "CS 5787"],
                "required_competencies": ["Locality-Sensitive Hashing (LSH)", "PageRank & graph embeddings", "ARIMA & State Space models"]
            },
            {
                "tier_name": "Tier 4: Enterprise Scale ML & Evaluation",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Large Scale Machine Learning", "10-605", "Advanced Machine Learning", "STA 4273H"],
                "required_competencies": ["Feature store architecture", "A/B testing methodology", "Distributed data pipelines (Spark/Ray)"]
            }
        ]
    },
    {
        "role_id": "security-cryptography-engineer",
        "title": "Information Security & Cryptography Engineer",
        "description": "Protect systems against adversarial vectors, engineer zero-knowledge proofs, audit protocol cryptographic invariants, and harden operating system seams.",
        "tiers": [
            {
                "tier_name": "Tier 1: Computer Systems & Assembly Fundamentals",
                "level": "Introductory (L1)",
                "target_queries": ["Introduction to Computer Systems", "15-213", "Programming Paradigms", "C++"],
                "required_competencies": ["Stack frame layouts", "Memory buffer safety", "Assembly execution"]
            },
            {
                "tier_name": "Tier 2: Network & Application Security",
                "level": "Core Intermediate (L2)",
                "target_queries": ["Security", "Computer Networks", "Web Security", "Stanford CS"],
                "required_competencies": ["TLS/SSL handshake", "Web vulnerability vectors (CSRF, XSS, SSRF)", "Firewalls & VPN architecture"]
            },
            {
                "tier_name": "Tier 3: Modern Cryptography & Security Protocols",
                "level": "Advanced (L3)",
                "target_queries": ["Cryptography", "CS 255", "Dan Boneh", "Security Protocols"],
                "required_competencies": ["Symmetric encryption (AES-GCM)", "Public key cryptography (RSA, ECC, Ed25519)", "Zero-Knowledge proofs basics"]
            },
            {
                "tier_name": "Tier 4: Hardware Security & Binary Exploitation",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Advanced Security", "Hardware Security", "Blockchain Development", "Cryptography"],
                "required_competencies": ["Side-channel attacks (Spectre/Meltdown)", "Fuzzing & binary analysis", "Post-quantum cryptographic primitives"]
            }
        ]
    },
    {
        "role_id": "embedded-robotics-autonomy",
        "title": "Robotics & Autonomous Systems Engineer",
        "description": "Construct real-time robotic controllers, SLAM (Simultaneous Localization and Mapping), motion planning algorithms, and embedded microkernel firmware.",
        "tiers": [
            {
                "tier_name": "Tier 1: Computational Mathematics & Programming",
                "level": "Introductory (L1)",
                "target_queries": ["ROB 101", "ROB 102", "Robotics 201", "Calculus"],
                "required_competencies": ["Rigid body transformations (SO3, SE3)", "Calculus for kinematics", "C++ for robotics"]
            },
            {
                "tier_name": "Tier 2: Embedded Systems & Microcontrollers",
                "level": "Core Intermediate (L2)",
                "target_queries": ["Embedded Systems", "Real-Time Systems", "Computer Architecture", "Microcontroller"],
                "required_competencies": ["Interrupt service routines", "SPI/I2C/CAN bus interfaces", "RTOS task scheduling"]
            },
            {
                "tier_name": "Tier 3: Robotics Mechanics, Perception & Control",
                "level": "Advanced (L3)",
                "target_queries": ["Robotics and Control", "Modern Robotics", "Computer Vision", "Control Systems"],
                "required_competencies": ["PID & LQR control", "Forward/Inverse kinematics", "Kalman filters (EKF, UKF)"]
            },
            {
                "tier_name": "Tier 4: SLAM, Autonomous Navigation & Trajectory Planning",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Robotics", "Stachniss", "SLAM", "Autonomous"],
                "required_competencies": ["Graph-based SLAM", "Particle filters & point clouds", "Motion planning (RRT*, A*, trajectory optimization)"]
            }
        ]
    },
    {
        "role_id": "computer-vision-multimodal",
        "title": "Computer Vision & Multimodal Perception Engineer",
        "description": "Develop 3D neural reconstruction systems, multi-view geometry, generative diffusion vision, and real-time visual-inertial odometry.",
        "tiers": [
            {
                "tier_name": "Tier 1: Linear Algebra & Signal Processing",
                "level": "Introductory (L1)",
                "target_queries": ["Linear Algebra", "Computational Thinking", "Signal Processing", "Python"],
                "required_competencies": ["Eigenvalues & SVD", "2D Convolution operations", "Fourier transforms"]
            },
            {
                "tier_name": "Tier 2: Classical Computer Vision & 3D Geometry",
                "level": "Core Intermediate (L2)",
                "target_queries": ["Computer Vision", "Image Processing", "CS231A", "Graphics"],
                "required_competencies": ["Epipolar geometry & essential matrix", "Feature detectors (SIFT, ORB)", "Camera calibration models"]
            },
            {
                "tier_name": "Tier 3: Deep Visual Recognition & CNNs",
                "level": "Advanced (L3)",
                "target_queries": ["CS231n", "Visual Recognition", "Deep Learning", "Convolutional"],
                "required_competencies": ["Residual networks (ResNets)", "Object detection (YOLO, Faster-RCNN)", "Semantic & instance segmentation"]
            },
            {
                "tier_name": "Tier 4: Neural Radiance Fields, 3D Vision & Diffusion",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Computer Graphics", "CS 184", "Deep Generative Models", "Vision"],
                "required_competencies": ["NeRF & 3D Gaussian Splatting", "Latent diffusion models", "Vision-Language models (CLIP, multimodal transformers)"]
            }
        ]
    },
    {
        "role_id": "software-architect-fullstack",
        "title": "Principal Software Architect & Full-Stack Engineer",
        "description": "Design modular, resilient enterprise software architectures, API contracts, high-load web systems, compiler optimizations, and scalable data layers.",
        "tiers": [
            {
                "tier_name": "Tier 1: Programming Fundamentals & Clean Code",
                "level": "Introductory (L1)",
                "target_queries": ["CS 50", "CS 61A", "Programming Fundamentals", "COMP1511"],
                "required_competencies": ["Polymorphism & data abstraction", "Testing & debugging harnesses", "Data structuring"]
            },
            {
                "tier_name": "Tier 2: Object-Oriented Design & Architecture",
                "level": "Core Intermediate (L2)",
                "target_queries": ["Software Engineering", "Object Oriented Design", "Software Architecture", "Concurrency"],
                "required_competencies": ["SOLID principles & GoF design patterns", "Domain-Driven Design (DDD) seams", "Concurrent memory models"]
            },
            {
                "tier_name": "Tier 3: Web Systems, Databases & Compilers",
                "level": "Advanced (L3)",
                "target_queries": ["Web Programming", "Database Systems", "Compilers", "CS 143"],
                "required_competencies": ["REST/GraphQL API protocols", "Lexing, parsing & AST compilation", "Indexing & query execution"]
            },
            {
                "tier_name": "Tier 4: Distributed Cloud Systems & High Availability",
                "level": "Graduate / Mastery (L4)",
                "target_queries": ["Distributed Systems", "Cloud", "Operating Systems", "6.824"],
                "required_competencies": ["Microservices vs Modular Monolith", "Event sourcing & CQRS", "Zero-downtime rolling deploys"]
            }
        ]
    }
]


class CSRoadmapsEngine:
    """Builds and resolves role roadmaps using indexed database courses."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH

    def resolve_tier_courses(self, target_queries: List[str], limit_per_tier: int = 5) -> List[Dict[str, Any]]:
        """Find the best representative courses matching a tier's search queries."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        matched_courses = []
        seen_ids = set()

        for q in target_queries:
            safe_q = q.replace('"', '').replace("'", "")
            sql = """
                SELECT c.*
                FROM courses c
                JOIN courses_fts f ON c.id = f.id
                WHERE courses_fts MATCH ?
                ORDER BY c.has_video DESC, c.video_count DESC
                LIMIT 4;
            """
            try:
                cur.execute(sql, (f'"{safe_q}"',))
                rows = cur.fetchall()
                for r in rows:
                    if r["id"] not in seen_ids:
                        seen_ids.add(r["id"])
                        item = dict(r)
                        item["video_urls"] = json.loads(item["video_urls_json"])
                        del item["video_urls_json"]
                        item["has_video"] = bool(item["has_video"])
                        matched_courses.append(item)
            except Exception:
                continue

        conn.close()
        return matched_courses[:limit_per_tier]

    def build_all_roadmaps(self) -> List[Dict[str, Any]]:
        """Synthesize degree-grade roadmaps for all 9 master roles."""
        roadmaps = []
        for role_def in ROLE_DEFINITIONS:
            role_data = {
                "role_id": role_def["role_id"],
                "title": role_def["title"],
                "description": role_def["description"],
                "total_tiers": len(role_def["tiers"]),
                "tiers": []
            }

            total_courses = 0
            for tier in role_def["tiers"]:
                courses = self.resolve_tier_courses(tier["target_queries"], limit_per_tier=4)
                total_courses += len(courses)
                role_data["tiers"].append({
                    "tier_name": tier["tier_name"],
                    "level": tier["level"],
                    "required_competencies": tier["required_competencies"],
                    "courses": courses
                })

            role_data["course_count"] = total_courses
            roadmaps.append(role_data)

        # Save to JSON
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(ROADMAPS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(roadmaps, f, indent=2, ensure_ascii=False)

        # Export individual markdown curricula
        CURRICULA_DIR.mkdir(parents=True, exist_ok=True)
        for r in roadmaps:
            self._export_markdown_curriculum(r)

        return roadmaps

    def _export_markdown_curriculum(self, roadmap: Dict[str, Any]):
        """Export a clean, clickable markdown syllabus for a role."""
        md_path = CURRICULA_DIR / f"{roadmap['role_id']}.md"
        lines = [
            f"# University Curriculum Roadmap: {roadmap['title']}",
            "",
            f"> **Role Archetype**: `{roadmap['role_id']}`  ",
            f"> **Overview**: {roadmap['description']}  ",
            f"> **Total Curated Courses**: {roadmap['course_count']} courses across 4 progressive tiers.",
            "",
            "---",
            ""
        ]

        for i, tier in enumerate(roadmap["tiers"], start=1):
            lines.append(f"## {tier['tier_name']}")
            lines.append(f"**Target Level**: `{tier['level']}`  ")
            lines.append("**Key Competencies**:")
            for comp in tier["required_competencies"]:
                lines.append(f"- {comp}")
            lines.append("")
            lines.append("### Recommended University Video Courses:")
            lines.append("")

            for c in tier["courses"]:
                code_badge = f"`[{c['code']}]` " if c['code'] else ""
                inst_badge = f"**{c['institution']}**"
                title_link = f"[{c['title']}]({c['primary_url']})" if c['primary_url'] else c['title']
                video_str = f" | [Watch Lectures ({c['video_count']} video sources)]({c['video_urls'][0]['url']})" if c['video_urls'] else ""
                instructor_str = f" (Prof. {c['instructor']})" if c['instructor'] else ""
                lines.append(f"- {code_badge}{title_link} — {inst_badge}{instructor_str}{video_str}")

            lines.append("")
            lines.append("---")
            lines.append("")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    builder = CSRoadmapsEngine()
    print("Building role-based academic curricula...")
    roadmaps = builder.build_all_roadmaps()
    print(f"Generated {len(roadmaps)} comprehensive roadmaps in {ROADMAPS_JSON_PATH} and {CURRICULA_DIR}!")
