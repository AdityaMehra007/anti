import sovereign_continuum.capability_engine as ce

gen = ce.CivilizationCapabilityGenerator()
open_problems = gen.problem_graph.get_open_problems()
print('Initial Open Problems:', len(open_problems))

for p in open_problems:
    res = gen.synthesize_capability(
        problem_id=p.problem_id,
        proposed_hypothesis=f'Deploy recursive autonomous capability solver for {p.title}',
        domain=p.domain,
        assumptions=['Unbounded compute verification', 'Zero-latency neural state routing']
    )
    cap = res.get('capability_spec')
    if cap:
        print(f"Synthesized: {cap.capability_id} | Domain: {cap.domain} | Problem: {p.title}")

print("Final Active Capability Registry Size:", len(gen.list_capabilities()))
