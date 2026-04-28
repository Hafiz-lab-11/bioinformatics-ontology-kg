import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from config import EDGES_CSV, VISUALS_DIR
from utils import logger

def visualize_relationships():
    """Plot relationship distribution and a meta-graph schema."""
    if not EDGES_CSV.exists():
        logger.error("Edges CSV missing.")
        return

    edges_df = pd.read_csv(EDGES_CSV)
    
    # 1. Relationship Distribution
    logger.info("Plotting relationship distribution...")
    plt.figure(figsize=(12, 7))
    edges_df['relation'].value_counts().plot(kind='bar', color='salmon', edgecolor='black')
    plt.title('Knowledge Graph: Relationship Distribution', fontsize=14)
    plt.xlabel('Relationship Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "relationship_distribution.png")
    plt.close()

    # 2. Meta-Graph (Schema)
    logger.info("Creating meta-graph (schema) visualization...")
    # Group by source_type, target_type, and relation to see the schema
    meta_df = edges_df.groupby(['source_type', 'target_type', 'relation']).size().reset_index(name='count')
    
    MetaG = nx.DiGraph()
    for _, row in meta_df.iterrows():
        MetaG.add_edge(row['source_type'], row['target_type'], relation=row['relation'])
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(MetaG, seed=42)
    nx.draw(MetaG, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', arrowsize=20)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(MetaG, 'relation')
    nx.draw_networkx_edge_labels(MetaG, pos, edge_labels=edge_labels, font_size=9)
    
    plt.title("Knowledge Graph Schema (Meta-Graph)", fontsize=15)
    plt.savefig(VISUALS_DIR / "schema_relationship_graph.png")
    plt.close()
    
    logger.info("visualize_relationships.py complete.")

def main():
    visualize_relationships()

if __name__ == "__main__":
    main()
