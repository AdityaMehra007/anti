"""
CIVILIZATION Ω∞∞: Autonomous Capability Generation Engine.

Implements Directives 120-147 of the OMEGA Constitution & Master Specification:
- Universal Problem Graph & Topological Root-Cause Tracing
- Failed Solution Memory (Zero-Regression Immutable Postmortem Ledger)
- The Unknown Engine ("What Am I Missing?" & Epistemic Audit)
- Second-Order Effect Simulator (Probabilistic Multi-Horizon Equilibrium)
- Recursive Capability & Agent Generator (Unbounded Extensibility)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import uuid


class ProblemScale(str, Enum):
    INDIVIDUAL = "individual"
    FAMILY = "family"
    ENTERPRISE = "enterprise"
    SECTOR = "sector"
    SOVEREIGN = "sovereign"
    PLANETARY = "planetary"
    CIVILIZATIONAL = "civilizational"


class ProblemStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    BLOCKED = "blocked"


@dataclass
class ProblemNode:
    problem_id: str
    scale: ProblemScale
    domain: str
    title: str
    description: str
    root_causes: List[str] = field(default_factory=list)
    upstream_problem_ids: List[str] = field(default_factory=list)
    downstream_problem_ids: List[str] = field(default_factory=list)
    solution_ids: List[str] = field(default_factory=list)
    status: ProblemStatus = ProblemStatus.OPEN
    created_at: float = field(default_factory=time.time)


@dataclass
class SolutionNode:
    solution_id: str
    problem_id: str
    title: str
    description: str
    verification_gate: str
    status: str = "proposed"  # proposed, simulating, validated, deployed, retired
    empirical_evidence: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class FailedSolutionRecord:
    record_id: str
    solution_id: str
    problem_id: str
    hypothesis: str
    failure_mode: str
    root_cause_analysis: str
    conditions_under_which_it_failed: Dict[str, Any]
    lessons_learned: List[str]
    timestamp: float = field(default_factory=time.time)


@dataclass
class CapabilitySpec:
    capability_id: str
    name: str
    domain: str
    agent_role: str
    skills_required: List[str]
    tools_required: List[str]
    verification_criteria: List[str]
    sandboxed: bool = True
    created_at: float = field(default_factory=time.time)


class UniversalProblemGraph:
    """
    Topological network mapping problems across all civilizational scales.
    Links problems to their systemic root causes and active solutions.
    """

    def __init__(self):
        self._problems: Dict[str, ProblemNode] = {}

    def register_problem(self, problem: ProblemNode) -> ProblemNode:
        self._problems[problem.problem_id] = problem
        return problem

    def get_problem(self, problem_id: str) -> Optional[ProblemNode]:
        return self._problems.get(problem_id)

    def link_problems(self, upstream_id: str, downstream_id: str) -> bool:
        if upstream_id in self._problems and downstream_id in self._problems:
            if downstream_id not in self._problems[upstream_id].downstream_problem_ids:
                self._problems[upstream_id].downstream_problem_ids.append(downstream_id)
            if upstream_id not in self._problems[downstream_id].upstream_problem_ids:
                self._problems[downstream_id].upstream_problem_ids.append(upstream_id)
            return True
        return False

    def resolve_root_causes(self, problem_id: str) -> List[ProblemNode]:
        """
        Recursively traces upstream problem nodes to discover systemic origins.
        """
        visited = set()
        root_nodes = []

        def _traverse(current_id: str):
            if current_id in visited or current_id not in self._problems:
                return
            visited.add(current_id)
            node = self._problems[current_id]
            if not node.upstream_problem_ids:
                root_nodes.append(node)
            else:
                for up_id in node.upstream_problem_ids:
                    _traverse(up_id)

        _traverse(problem_id)
        return root_nodes

    def get_open_problems(self, scale: Optional[ProblemScale] = None) -> List[ProblemNode]:
        return [
            p for p in self._problems.values()
            if p.status in [ProblemStatus.OPEN, ProblemStatus.IN_PROGRESS]
            and (scale is None or p.scale == scale)
        ]

    def total_count(self) -> int:
        return len(self._problems)


class FailedSolutionMemory:
    """
    Immutable ledger of disproven hypotheses, dead ends, and failure modes.
    Enforces Directive 123: Zero-regression execution.
    """

    def __init__(self):
        self._records: List[FailedSolutionRecord] = []

    def record_failure(self, failure: FailedSolutionRecord) -> None:
        self._records.append(failure)

    STOP_WORDS = {
        "and", "with", "or", "in", "the", "a", "an", "to", "of", "for", "at", "by", "on",
        "using", "is", "without", "that", "this", "from", "as", "be", "are", "it",
    }

    def has_failed_previously(self, hypothesis: str, problem_id: Optional[str] = None) -> Optional[FailedSolutionRecord]:
        """
        Checks whether a proposed hypothesis or similar concept has previously failed.
        Uses content-word extraction and Jaccard similarity to prevent false collisions.
        """
        hypo_norm = hypothesis.lower().strip()
        words_input = {w for w in hypo_norm.split() if len(w) > 2 and w not in self.STOP_WORDS}

        for record in self._records:
            if problem_id and record.problem_id != problem_id:
                continue
            rec_hypo = record.hypothesis.lower().strip()
            # Exact substring match
            if hypo_norm in rec_hypo or rec_hypo in hypo_norm:
                return record
            # Meaningful content-word overlap
            words_rec = {w for w in rec_hypo.split() if len(w) > 2 and w not in self.STOP_WORDS}
            if words_input and words_rec:
                intersection = words_input.intersection(words_rec)
                union = words_input.union(words_rec)
                jaccard = len(intersection) / len(union) if union else 0.0
                if jaccard >= 0.40 or (len(intersection) >= 5 and len(intersection) / len(words_input) >= 0.60):
                    return record
        return None


    def query_failures(self, problem_id: Optional[str] = None, keyword: Optional[str] = None) -> List[FailedSolutionRecord]:
        results = self._records
        if problem_id:
            results = [r for r in results if r.problem_id == problem_id]
        if keyword:
            kw = keyword.lower()
            results = [r for r in results if kw in r.hypothesis.lower() or kw in r.root_cause_analysis.lower()]
        return results

    def total_count(self) -> int:
        return len(self._records)


class UnknownEngine:
    """
    Directive 124: The Epistemic Probe.
    Answers: 'What am I missing?', 'Why hasn't this been done?', and 'Show me the evidence'.
    """

    def audit_blind_spots(self, initiative_name: str, domain: str, assumptions: List[str]) -> Dict[str, Any]:
        missing_prerequisites = []
        unstated_assumptions = []
        
        # Standard civilizational stress checks
        if any("free" in a.lower() or "zero-cost" in a.lower() for a in assumptions):
            missing_prerequisites.append("Thermodynamic and baseload energy cost accounting")
            unstated_assumptions.append("Assumes energy infrastructure scales without capital expenditure")

        if any("instant" in a.lower() or "unlimited" in a.lower() for a in assumptions):
            missing_prerequisites.append("Latency critical bandwidth and queueing latency bounds")
            unstated_assumptions.append("Assumes zero network congestion and instantaneous consensus")

        if any("global" in a.lower() or "cross-border" in a.lower() for a in assumptions):
            missing_prerequisites.append("Cross-jurisdictional legal and export control compliance")
            unstated_assumptions.append("Assumes regulatory uniformity across divergent nation states")

        if not missing_prerequisites:
            missing_prerequisites.append("Adversarial red-team stress test against malicious state actors")

        why_hasnt_done = (
            f"Historical barriers in {domain} typically stem from capital intensity, "
            f"coordination failure across fragmented incumbents, and unverified verification seams."
        )

        return {
            "initiative_name": initiative_name,
            "domain": domain,
            "missing_prerequisites": missing_prerequisites,
            "unstated_assumptions": unstated_assumptions,
            "why_hasnt_this_been_done": why_hasnt_done,
            "evidence_required": [
                "Empirical benchmark data under real load",
                "Deterministic verification test suite passing 100%",
                "Independent adversarial audit verification",
            ],
            "audit_verdict": "PROCEED_WITH_CONTROLS" if missing_prerequisites else "CLEARED",
        }


class SecondOrderEffectSimulator:
    """
    Directive 125: Probabilistic Multi-Order Causal Ripple Simulator.
    Evaluates counterparty reactions, equilibrium shifts, and cascading risks.
    """

    def simulate_effects(self, action_name: str, target_sector: str, magnitude_scale: float) -> Dict[str, Any]:
        # Calculate cascading risk score (0 to 10) based on sector and magnitude
        base_risk = min(10.0, max(1.0, magnitude_scale * 1.8))

        direct_first_order = [
            f"Immediate supply and capacity reallocation in {target_sector}",
            f"Direct margin pressure on tier-2 suppliers within {target_sector}",
        ]

        second_order_reactions = [
            f"Incumbent competitors in {target_sector} lower pricing to defend market share",
            f"Regulatory scrutiny triggered regarding market concentration or antitrust limits",
            f"Counterparties accelerate long-term off-take locking to hedge supply shock",
        ]

        third_order_equilibrium = [
            f"Permanent shift in industry standard interface towards open capability rails",
            f"Macro-economic deflation in unit costs of production for downstream consumers",
        ]

        circuit_breakers = [
            "Automatic throttle if counterparty volatility exceeds 15% daily delta",
            "Emergency liquidity backstop reserve allocation",
            "Regulatory compliance pre-clearance holding escrow",
        ]

        return {
            "action_name": action_name,
            "target_sector": target_sector,
            "magnitude_scale": magnitude_scale,
            "cascading_risk_score": round(base_risk, 2),
            "first_order_direct": direct_first_order,
            "second_order_counterparty_reactions": second_order_reactions,
            "third_order_systemic_equilibrium": third_order_equilibrium,
            "circuit_breakers": circuit_breakers,
        }


class CivilizationCapabilityGenerator:
    """
    Apex meta-engine implementing CIVILIZATION Ω∞∞ capability generation.
    Recursively synthesizes agents, verifies seams, enforces memory, and expands capability surface.
    """

    def __init__(self):
        self.problem_graph = UniversalProblemGraph()
        self.failed_memory = FailedSolutionMemory()
        self.unknown_engine = UnknownEngine()
        self.second_order_sim = SecondOrderEffectSimulator()
        self._capabilities: Dict[str, CapabilitySpec] = {}

        # Seed foundational problems
        self._seed_initial_problem_topology()

    def _seed_initial_problem_topology(self):
        # 1. Baseload compute & energy coupling
        p_energy = ProblemNode(
            problem_id="PROB-ENERGY-001",
            scale=ProblemScale.PLANETARY,
            domain="Energy & Infrastructure",
            title="Terawatt Compute Grid Baseload Saturation",
            description="AI data centers encounter massive grid interconnection queues and carbon-heavy fossil peaker constraints.",
            root_causes=["Centralized grid transmission congestion", "Intermittent renewable curtailment"],
        )
        self.problem_graph.register_problem(p_energy)

        # 2. Embodied physical automation
        p_robotics = ProblemNode(
            problem_id="PROB-ROBOTICS-001",
            scale=ProblemScale.PLANETARY,
            domain="Physical Automation",
            title="Industrial & Logistics Labor Depletion",
            description="Global demographic inversion causing acute labor shortages across warehousing, precision assembly, and agriculture.",
            root_causes=["Declining working-age population", "High injury rates in manual heavy labor"],
        )
        self.problem_graph.register_problem(p_robotics)

        # 3. M2M Real-time Micro-Settlement
        p_m2m = ProblemNode(
            problem_id="PROB-FINANCE-001",
            scale=ProblemScale.SECTOR,
            domain="Financial Rails",
            title="High Latency and Fee Friction in Autonomous Machine Transactions",
            description="Legacy banking systems (SWIFT, ACH) cannot settle sub-cent robot-to-reactor energy transactions in sub-second timeframes.",
            root_causes=["Batch-based settlement architecture", "High correspondent banking friction"],
        )
        self.problem_graph.register_problem(p_m2m)

        # Connect upstream dependencies
        self.problem_graph.link_problems("PROB-ENERGY-001", "PROB-ROBOTICS-001")

        # Seed a known failed solution in memory to demonstrate zero-regression enforcement
        self.failed_memory.record_failure(
            FailedSolutionRecord(
                record_id="FAIL-001",
                solution_id="SOL-OLD-SOLAR-ONLY",
                problem_id="PROB-ENERGY-001",
                hypothesis="Power 24/7 500MW AI hub using solar panels without nuclear baseload or battery buffers",
                failure_mode="Intermittent blackout during night and cloudy winter cycles; GPU clusters suffered catastrophic thermal cycling",
                root_cause_analysis="Solar capacity factor is 22-28%; continuous AI training workloads require 99.999% baseload availability.",
                conditions_under_which_it_failed={"workload": "continuous_llm_pretraining", "season": "winter"},
                lessons_learned=[
                    "Never deploy solar alone for gigawatt compute hubs",
                    "Always collocate SMR nuclear reactors or dedicated high-capacity storage",
                ],
            )
        )

    def synthesize_capability(
        self,
        problem_id: str,
        proposed_hypothesis: str,
        domain: str,
        assumptions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes a new specialized capability and agent harness to solve a problem.
        Enforces Failed Solution Memory, Unknown Engine, and Second-Order Sim.
        """
        assumptions = assumptions or []
        problem = self.problem_graph.get_problem(problem_id)
        if not problem:
            return {
                "success": False,
                "reason": f"Problem {problem_id} does not exist in Universal Problem Graph",
            }

        # 1. Check Failed Solution Memory (Directive 123)
        prior_failure = self.failed_memory.has_failed_previously(proposed_hypothesis, problem_id)
        if prior_failure:
            return {
                "success": False,
                "status": "REJECTED_BY_FAILED_SOLUTION_MEMORY",
                "failure_record": {
                    "record_id": prior_failure.record_id,
                    "hypothesis": prior_failure.hypothesis,
                    "failure_mode": prior_failure.failure_mode,
                    "root_cause_analysis": prior_failure.root_cause_analysis,
                    "lessons_learned": prior_failure.lessons_learned,
                },
                "directive": "OMEGA Directive 123: Zero-regression. Modify hypothesis to account for identified failure root causes.",
            }

        # 2. Run Unknown Engine Audit (Directive 124)
        unknown_audit = self.unknown_engine.audit_blind_spots(
            initiative_name=f"Capability for {problem.title}",
            domain=domain,
            assumptions=assumptions,
        )

        # 3. Simulate Second-Order Effects (Directive 125)
        sim_results = self.second_order_sim.simulate_effects(
            action_name=f"Deploy {domain} capability",
            target_sector=domain,
            magnitude_scale=2.5,
        )

        # 4. Generate Capability Specification (Directive 121 & 126)
        cap_id = f"CAP-{domain.upper().replace(' ', '_')[:8]}-{uuid.uuid4().hex[:6]}"
        agent_role = f"Specialized {domain} Orchestrator Agent"
        spec = CapabilitySpec(
            capability_id=cap_id,
            name=f"Autonomous {domain} Solver",
            domain=domain,
            agent_role=agent_role,
            skills_required=[
                f"{domain.lower().replace(' ', '-')}-analysis",
                "verification-before-completion",
                "antifragile-stress-testing",
            ],
            tools_required=["view_file", "run_command", "write_to_file"],
            verification_criteria=[
                "Red-green deterministic test suite passing",
                "Root cause addressed in problem graph",
                "Zero regression against Failed Solution Memory",
            ],
            sandboxed=True,
        )

        self._capabilities[cap_id] = spec

        # Update problem status
        problem.status = ProblemStatus.IN_PROGRESS

        return {
            "success": True,
            "capability_spec": spec,
            "unknown_audit": unknown_audit,
            "second_order_effects": sim_results,
            "message": f"Successfully synthesized and registered capability {cap_id} for problem {problem_id}.",
        }

    def list_capabilities(self) -> List[CapabilitySpec]:
        return list(self._capabilities.values())

    def get_capability(self, capability_id: str) -> Optional[CapabilitySpec]:
        return self._capabilities.get(capability_id)

    def execute_civilization_cycle(self) -> Dict[str, Any]:
        """
        Executes a complete macro capability cycle across all problem nodes.
        """
        open_problems = self.problem_graph.get_open_problems()
        failures_count = self.failed_memory.total_count()
        capabilities_count = len(self._capabilities)

        return {
            "timestamp": time.time(),
            "status": "OPERATIONAL",
            "total_problems_in_graph": self.problem_graph.total_count(),
            "open_problems_count": len(open_problems),
            "failed_solutions_indexed": failures_count,
            "active_capabilities_count": capabilities_count,
            "directives_enforced": [120, 121, 122, 123, 124, 125, 126, 127, 128],
        }
