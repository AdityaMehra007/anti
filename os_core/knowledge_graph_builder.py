from path_resolver import resolve_data_path
import os, json, csv
from datetime import datetime

class KnowledgeGraphBuilder:
    """Builds and Serializes the Multi-Entity Career Knowledge Graph."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.graph_file = os.path.join(workspace, "career_knowledge_graph.json")

    def build_graph(self):
        nodes = []
        links = []
        
        # Candidate Node
        nodes.append({"id": "CANDIDATE:Aditya_Mehra", "type": "Candidate", "name": "Aditya Mehra", "degree": "BBA International Business"})
        
        # Load top companies & matches
        matches_csv = resolve_data_path(self.workspace, "job_to_connection_matches.csv")
        if os.path.exists(matches_csv):
            with open(matches_csv, "r", encoding="utf-8", errors="replace") as f:
                matches = list(csv.DictReader(f))[:50]
                
            seen_cos = set()
            seen_jobs = set()
            seen_people = set()
            
            for m in matches:
                co = m.get("Canonical Company")
                j_id = m.get("Job ID")
                j_title = m.get("Job Title")
                p_name = m.get("Contact Name")
                p_pos = m.get("Contact Position")
                
                if co and co not in seen_cos:
                    seen_cos.add(co)
                    nodes.append({"id": f"COMPANY:{co}", "type": "Company", "name": co})
                    
                if j_id and j_id not in seen_jobs:
                    seen_jobs.add(j_id)
                    nodes.append({"id": f"JOB:{j_id}", "type": "Job", "title": j_title, "company": co})
                    links.append({"source": f"JOB:{j_id}", "target": f"COMPANY:{co}", "relation": "POSTED_BY"})
                    links.append({"source": "CANDIDATE:Aditya_Mehra", "target": f"JOB:{j_id}", "relation": "QUALIFIED_FOR"})
                    
                if p_name and p_name not in seen_people:
                    seen_people.add(p_name)
                    nodes.append({"id": f"PERSON:{p_name}", "type": "Person", "name": p_name, "position": p_pos})
                    links.append({"source": f"PERSON:{p_name}", "target": f"COMPANY:{co}", "relation": "WORKS_AT"})
                    links.append({"source": f"PERSON:{p_name}", "target": f"JOB:{j_id}", "relation": "REFERRAL_NODE"})
                    
        graph_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "node_count": len(nodes),
                "link_count": len(links)
            },
            "nodes": nodes,
            "links": links
        }
        
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2)
            
        return graph_data
