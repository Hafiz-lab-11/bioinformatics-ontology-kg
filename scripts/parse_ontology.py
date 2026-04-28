import obonet
import json
from config import ONTOLOGY_FILES, ONTOLOGY_JSON
from utils import logger

VALID_ONTOLOGY_RELATIONS = {
    "is_a",
    "part_of",
    "regulates",
    "positively_regulates",
    "negatively_regulates",
    "develops_from",
}

ONTOLOGY_LABELS = {
    "hp": "Phenotype",
    "uberon": "Anatomy",
    "disease": "Disease",
}

GO_LABELS = {
    "biological_process": "BiologicalProcess",
    "molecular_function": "MolecularFunction",
    "cellular_component": "CellularComponent",
}


def resolve_node_type(onto_name, data):
    if onto_name == "go":
        return GO_LABELS.get(str(data.get("namespace", "")).strip(), "OntologyTerm")
    return ONTOLOGY_LABELS.get(onto_name, "OntologyTerm")

def parse_ontology():
    """Extract nodes and edges from OBO files with standardized schema."""
    all_nodes = {}
    all_edges = []
    
    for onto_name, file_path in ONTOLOGY_FILES.items():
        if not file_path.exists():
            logger.warning(f"Ontology file missing: {file_path}")
            continue
            
        logger.info(f"Parsing {onto_name} ontology: {file_path.name}")
        try:
            graph = obonet.read_obo(str(file_path))
            
            # Extract nodes
            for node_id, data in graph.nodes(data=True):
                # Optimize: only store if not already seen or to update info
                if node_id not in all_nodes:
                    all_nodes[node_id] = {
                        "id": node_id,
                        "name": data.get("name", "Unknown"),
                        "label": resolve_node_type(onto_name, data),
                        "source": onto_name,
                        "namespace": data.get("namespace", onto_name)
                    }
            
            # Extract edges
            skipped_relations = 0
            for source, target, key, data in graph.edges(keys=True, data=True):
                # Standardize relation: 'is_a' is default key in many obonet versions
                relation = key if key else "is_a"
                if relation not in VALID_ONTOLOGY_RELATIONS:
                    skipped_relations += 1
                    continue
                
                all_edges.append({
                    "source": source,
                    "target": target,
                    "type": relation
                })

            if skipped_relations:
                logger.info(f"Skipped {skipped_relations} non-ontology relations from {onto_name}")
                
        except Exception as e:
            logger.error(f"Failed to parse {onto_name}: {e}")

    # Save to intermediate JSON
    output_data = {
        "nodes": list(all_nodes.values()),
        "edges": all_edges
    }
    
    with open(ONTOLOGY_JSON, 'w') as f:
        json.dump(output_data, f, indent=2)
        
    logger.info(f"Ontology parsing complete. Extracted {len(all_nodes)} nodes and {len(all_edges)} edges.")

def main():
    parse_ontology()

if __name__ == "__main__":
    main()
