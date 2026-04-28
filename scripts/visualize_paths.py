import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from config import EDGES_CSV, NODES_CSV, VISUALS_DIR
from utils import logger
import random

def analyze_shortest_paths():
    """Find and visualize the shortest path between a gene and a relevant ontology term."""
    if not EDGES_CSV.exists() or not NODES_CSV.exists():
        logger.error("CSVs missing.")
        return

    logger.info("Initializing path analysis (Optimized)...")
    edges_df = pd.read_csv(EDGES_CSV)
    nodes_df = pd.read_csv(NODES_CSV)
    
    # Use undirected graph for shortest path analysis to find connectivity
    G = nx.from_pandas_edgelist(edges_df, 'source_id', 'target_id')
    node_names = nodes_df.set_index('node_id')['node_name'].to_dict()
    node_types = nodes_df.set_index('node_id')['node_type'].to_dict()

    # Optimization: Sort genes by degree to find "Hub Genes" which are more likely to have paths
    logger.info("Selecting hub genes for faster path discovery...")
    gene_nodes = [n for n in G.nodes() if node_types.get(n) == 'Gene']
    if not gene_nodes:
        logger.warning("No Gene nodes found.")
        return
        
    # Get top 10 hubs among genes
    gene_degrees = {g: G.degree(g) for g in gene_nodes}
    top_genes = sorted(gene_degrees, key=gene_degrees.get, reverse=True)[:10]
    
    found_path = None
    source_node = None
    target_node = None
    
    # Search for a path from a hub gene to a random ontology term
    logger.info("Searching for a path from hub genes...")
    all_onto_terms = [n for n in G.nodes() if node_types.get(n) != 'Gene']
    random.shuffle(all_onto_terms)
    
    for g in top_genes:
        # Search against a small subset of ontology terms to keep it fast
        for t in all_onto_terms[:200]:
            try:
                if nx.has_path(G, g, t):
                    path = nx.shortest_path(G, g, t)
                    if 2 < len(path) <= 6: # Find a path of "interesting" length
                        found_path = path
                        source_node = g
                        target_node = t
                        break
            except:
                continue
        if found_path: break

    if not found_path:
        logger.warning("No suitable path found within search limits.")
        return

    logger.info(f"Visualizing path of length {len(found_path)}: {node_names.get(source_node)} -> {node_names.get(target_node)}")
    
    try:
        # Create a subgraph for the path
        subG = nx.Graph()
        path_edges = list(zip(found_path, found_path[1:]))
        subG.add_edges_from(path_edges)
        
        plt.figure(figsize=(10, 5))
        pos = nx.spring_layout(subG, seed=42)
        
        # Prepare labels with names
        labels = {n: f"{node_names.get(n, n)}\n({n})" for n in subG.nodes()}
        
        # Color nodes by type
        colors = ['lightgreen' if node_types.get(n) == 'Gene' else 'orange' for n in subG.nodes()]
        
        nx.draw(subG, pos, with_labels=True, labels=labels, node_color=colors, 
                node_size=3000, font_size=8, font_weight='bold', edge_color='gray', width=2)
        
        plt.title(f"Bio-Ontology Path: {node_names.get(source_node)} → {node_names.get(target_node)}")
        plt.tight_layout()
        
        path_visual_path = VISUALS_DIR / "shortest_path_analysis.png"
        plt.savefig(path_visual_path)
        plt.close()

        # Save textual path analysis
        sample_path_txt = VISUALS_DIR / "sample_paths.txt"
        with open(sample_path_txt, 'w') as f:
            f.write(f"Discovery Path from {node_names.get(source_node)} ({source_node}) to {node_names.get(target_node)} ({target_node}):\n")
            for i, node in enumerate(found_path):
                f.write(f"  Step {i}: {node_names.get(node)} ({node})\n")
        
        logger.info(f"Path visualization saved to {path_visual_path}")
        logger.info(f"Sample paths text saved to {sample_path_txt}")
        
    except Exception as e:
        logger.error(f"Error visualizing path: {e}")

def main():
    analyze_shortest_paths()

if __name__ == "__main__":
    main()
