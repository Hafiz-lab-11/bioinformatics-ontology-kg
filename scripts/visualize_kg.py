import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random
from config import NODES_CSV, EDGES_CSV, VISUALS_DIR, SUBGRAPH_DIR
from utils import logger

def visualize_summary():
    """Plot node type distribution and a sample subgraph."""
    if not NODES_CSV.exists() or not EDGES_CSV.exists():
        logger.error("CSVs missing. Run build_kg first.")
        return

    logger.info("Generating node type distribution plot...")
    nodes_df = pd.read_csv(NODES_CSV)
    
    # Node Type Distribution
    plt.figure(figsize=(10, 6))
    nodes_df['node_type'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Knowledge Graph: Node Type Distribution', fontsize=14)
    plt.xlabel('Node Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "node_type_distribution.png")
    plt.close()

    # Sample Subgraph Visualization
    logger.info("Creating sample subgraph visualization...")
    edges_df = pd.read_csv(EDGES_CSV)
    
    # Pick a sample of 50 edges to keep it readable
    sample_edges = edges_df.sample(min(50, len(edges_df)))
    G = nx.from_pandas_edgelist(sample_edges, 'source_id', 'target_id', edge_attr='relation')
    
    # Add node types as attributes for coloring
    node_types = nodes_df.set_index('node_id')['node_type'].to_dict()
    nx.set_node_attributes(G, node_types, 'type')
    
    color_map = {'Gene': 'lightgreen', 'OntologyTerm': 'orange'}
    node_colors = [color_map.get(node_types.get(node, 'Unknown'), 'gray') for node in G.nodes()]
    
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=8, edge_color='gray', alpha=0.8)
    
    # Draw edge labels (relations)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title("Sample Knowledge Graph Subset (50 Edges)", fontsize=15)
    plt.savefig(VISUALS_DIR / "kg_sample_network.png")
    plt.close()
    
    logger.info("visualize_kg.py: Summary and Subgraph visualizations complete.")

def main():
    visualize_summary()

if __name__ == "__main__":
    main()
