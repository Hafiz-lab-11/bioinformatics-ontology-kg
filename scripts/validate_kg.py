import networkx as nx
from config import FINAL_KG_PATH, ALLOWED_NODE_TYPES, ALLOWED_RELATIONS
from utils import logger

def validate_kg():
    """Perform strict health and schema checks on the generated Knowledge Graph."""
    if not FINAL_KG_PATH.exists():
        logger.error(f"KG not found for validation: {FINAL_KG_PATH}")
        return

    logger.info("Starting advanced KG validation...")
    
    try:
        # Load the graph
        kg = nx.read_graphml(str(FINAL_KG_PATH))
        
        errors = []
        node_counts = {t: 0 for t in ALLOWED_NODE_TYPES}
        relation_counts = {r: 0 for r in ALLOWED_RELATIONS}
        
        # 1. Validate Nodes
        for node_id, data in kg.nodes(data=True):
            ntype = data.get('node_type')
            if ntype not in ALLOWED_NODE_TYPES:
                errors.append(f"Invalid node_type '{ntype}' for node {node_id}")
            else:
                node_counts[ntype] += 1

            if data.get('node_name') in ("", "Unknown", None):
                errors.append(f"Missing or placeholder node_name for node {node_id}")
            if ntype != "Gene" and not data.get('source'):
                errors.append(f"Missing source metadata for ontology node {node_id}")
                
        # 2. Validate Edges and Connectivity
        for u, v, data in kg.edges(data=True):
            rel = data.get('relation')
            if rel not in ALLOWED_RELATIONS and rel is not None:
                errors.append(f"Invalid relation '{rel}' between {u} and {v}")
            elif rel:
                relation_counts[rel] = relation_counts.get(rel, 0) + 1
            
            # Check for hanging edges (already handled by GraphML/NetworkX during load, 
            # but we verify logical consistency of source/target types)
            stype = data.get('source_type')
            ttype = data.get('target_type')
            if stype and kg.nodes[u].get('node_type') != stype:
                errors.append(f"Source type mismatch for edge {u}->{v}")
            if ttype and kg.nodes[v].get('node_type') != ttype:
                errors.append(f"Target type mismatch for edge {u}->{v}")
                
        # 3. Connectivity
        if kg.number_of_nodes() > 0:
            isolated = list(nx.isolates(kg))
            if isolated:
                logger.warning(f"Found {len(isolated)} isolated nodes.")
            else:
                logger.info("No isolated nodes found. Good connectivity.")

        # Report Results
        logger.info("--- Validation Summary ---")
        logger.info(f"Nodes: {kg.number_of_nodes()} total")
        for t, count in node_counts.items():
            logger.info(f"  - {t}: {count}")
        
        logger.info(f"Edges: {kg.number_of_edges()} total")
        for r, count in relation_counts.items():
            if count > 0:
                logger.info(f"  - {r}: {count}")

        if errors:
            logger.error(f"Validation failed with {len(errors)} errors (first 5 shown):")
            for e in errors[:5]:
                logger.error(f"  - {e}")
        else:
            logger.info("Validation PASSED: Schema is clean and consistent.")

    except Exception as e:
        logger.error(f"Error during validation process: {e}")

def main():
    validate_kg()

if __name__ == "__main__":
    main()
