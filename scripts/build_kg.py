import json

import networkx as nx
import pandas as pd

from config import FINAL_KG_PATH, GENE_GO_MAPPING, ONTOLOGY_JSON
from utils import logger

def build_kg():
    """Build the final Knowledge Graph merging genes and ontologies."""
    if not ONTOLOGY_JSON.exists() or not GENE_GO_MAPPING.exists():
        logger.error("Required intermediate files missing. Run parsers first.")
        return

    logger.info("Initializing Knowledge Graph construction...")
    # Use MultiDiGraph to allow multiple relationship types between same nodes if needed
    kg = nx.MultiDiGraph()

    # 1. Load Ontology Terms
    logger.info("Adding Ontology nodes and edges...")
    with open(ONTOLOGY_JSON, 'r') as f:
        onto_data = json.load(f)
    
    ontology_ids = set()
    ontology_node_types = {}
    for node in onto_data['nodes']:
        ontology_ids.add(node['id'])
        ontology_node_types[node['id']] = node.get('label', 'OntologyTerm')
        kg.add_node(
            node['id'],
            node_name=node['name'],
            node_type=node.get('label', 'OntologyTerm'),
            source=node.get('source', 'unknown'),
            namespace=node.get('namespace', '')
        )
    
    for edge in onto_data['edges']:
        kg.add_edge(
            edge['source'],
            edge['target'],
            relation=edge['type'],
            source_type=ontology_node_types.get(edge['source'], 'OntologyTerm'),
            target_type=ontology_node_types.get(edge['target'], 'OntologyTerm')
        )

    # 2. Load Gene Mappings
    logger.info("Adding Gene nodes and associations...")
    gene_df = pd.read_csv(GENE_GO_MAPPING).drop_duplicates()
    
    # Track unique genes to avoid redundant node additions
    processed_genes = set()
    missing_go_ids = set()
    
    for _, row in gene_df.iterrows():
        gene_id = row['source_id']
        go_id = row['target_id']
        
        # Add Gene Node if not already present
        if gene_id not in processed_genes and not kg.has_node(gene_id):
            kg.add_node(
                gene_id, 
                node_name=gene_id.split(':')[-1], # Use numeric ID as name
                node_type="Gene"
            )
            processed_genes.add(gene_id)
            
        # Add association edge
        # Check if target GO ID exists in the graph
        if go_id in ontology_ids:
            kg.add_edge(
                gene_id,
                go_id,
                relation=row['relation'],
                source_type="Gene",
                target_type=ontology_node_types.get(go_id, "OntologyTerm")
            )
        else:
            missing_go_ids.add(go_id)

    if missing_go_ids:
        logger.warning(
            f"Skipped {len(missing_go_ids)} gene2go rows whose GO term was missing from the ontology parse. "
            f"Sample: {sorted(missing_go_ids)[:10]}"
        )

    logger.info(f"KG construction complete: {kg.number_of_nodes()} nodes, {kg.number_of_edges()} edges.")
    
    # 3. Export to GraphML
    logger.info(f"Exporting to {FINAL_KG_PATH}...")
    # Ensure all attributes are strings for GraphML compatibility
    nx.write_graphml(kg, str(FINAL_KG_PATH))
    logger.info("Final GraphML export successful.")

    # 4. Export to CSV (Nodes and Edges)
    from config import NODES_CSV, EDGES_CSV, OUTPUT_DIR
    logger.info(f"Exporting CSVs to {OUTPUT_DIR}...")
    
    # Nodes CSV
    nodes_data = []
    for node_id, data in kg.nodes(data=True):
        nodes_data.append({
            "node_id": node_id,
            "node_name": data.get("node_name", ""),
            "node_type": data.get("node_type", "")
        })
    pd.DataFrame(nodes_data).to_csv(NODES_CSV, index=False)
    
    # Edges CSV
    edges_data = []
    for u, v, data in kg.edges(data=True):
        edges_data.append({
            "source_id": u,
            "target_id": v,
            "relation": data.get("relation", ""),
            "source_type": data.get("source_type", ""),
            "target_type": data.get("target_type", "")
        })
    pd.DataFrame(edges_data).to_csv(EDGES_CSV, index=False)
    
    logger.info(f"Exported {len(nodes_data)} nodes to {NODES_CSV.name}")
    logger.info(f"Exported {len(edges_data)} edges to {EDGES_CSV.name}")

def main():
    build_kg()

if __name__ == "__main__":
    main()
