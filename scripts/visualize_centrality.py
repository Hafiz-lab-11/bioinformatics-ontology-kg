import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from config import EDGES_CSV, NODES_CSV, VISUALS_DIR, OUTPUT_DIR
from utils import logger

def compute_centrality():
    """Compute centrality metrics and save top nodes."""
    if not EDGES_CSV.exists() or not NODES_CSV.exists():
        logger.error("CSVs missing.")
        return

    logger.info("Computing centrality metrics (this may take a moment)...")
    edges_df = pd.read_csv(EDGES_CSV)
    nodes_df = pd.read_csv(NODES_CSV)
    
    G = nx.from_pandas_edgelist(edges_df, 'source_id', 'target_id')
    
    # 1. Degree Centrality
    logger.info("Calculating Degree Centrality...")
    deg_centrality = nx.degree_centrality(G)
    
    # 2. Betweenness Centrality (using sampling for performance)
    logger.info("Calculating Betweenness Centrality (sampled for speed)...")
    # k=100 nodes sampled to estimate betweenness
    bet_centrality = nx.betweenness_centrality(G, k=100, seed=42)
    
    # Merge metrics
    metrics = []
    for node_id in G.nodes():
        metrics.append({
            "node_id": node_id,
            "degree_centrality": deg_centrality.get(node_id, 0),
            "betweenness_centrality": bet_centrality.get(node_id, 0)
        })
    
    metrics_df = pd.DataFrame(metrics)
    
    # Add node names and types for context
    nodes_df_clean = nodes_df[['node_id', 'node_name', 'node_type']]
    final_df = pd.merge(metrics_df, nodes_df_clean, on='node_id', how='left')
    
    # Save top 50 to CSV
    top_nodes = final_df.sort_values(by='degree_centrality', ascending=False).head(50)
    centrality_csv = OUTPUT_DIR / "top_nodes_by_centrality.csv"
    top_nodes.to_csv(centrality_csv, index=False)
    logger.info(f"Saved top 50 central nodes to {centrality_csv}")
    
    # Plot top 10 Degree Centrality
    plt.figure(figsize=(12, 6))
    top_10_deg = top_nodes.head(10)
    plt.barh(top_10_deg['node_name'], top_10_deg['degree_centrality'], color='lightcoral')
    plt.title('Top 10 Nodes by Degree Centrality')
    plt.xlabel('Centrality Score')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "top_centrality_hubs.png")
    plt.close()

    logger.info("visualize_centrality.py complete.")

def main():
    compute_centrality()

if __name__ == "__main__":
    main()
