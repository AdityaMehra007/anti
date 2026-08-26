import json
from datetime import datetime

class OmegaKnowledgeGraph:
    '''Multi-Entity Interconnected Knowledge Graph Engine.'''
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, node_type, properties):
        self.nodes[node_id] = {"id": node_id, "type": node_type, "properties": properties}

    def add_edge(self, source_id, target_id, relation_type, weight=1.0):
        self.edges.append({
            "source": source_id,
            "target": target_id,
            "relation": relation_type,
            "weight": weight,
            "created_at": datetime.now().isoformat()
        })

    def export_graph(self):
        return {
            "metadata": {"total_nodes": len(self.nodes), "total_edges": len(self.edges)},
            "nodes": list(self.nodes.values()),
            "edges": self.edges
        }
