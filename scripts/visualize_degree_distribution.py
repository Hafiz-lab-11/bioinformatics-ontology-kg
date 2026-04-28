import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from config import EDGES_CSV, VISUALS_DIR
from utils import logger

def visualize_degree_distribution():
    """Calculate and plot the degree distribution of the Knowledge Graph."""
    if not EDGES_CSV.exists():
        logger.error("Edges CSV missing.")
        return

    logger.info("Computing degree distribution...")
    edges_df = pd.read_csv(EDGES_CSV)
    G = nx.from_pandas_edgelist(edges_df, 'source_id', 'target_id')
    
    degrees = [d for n, d in G.degree()]
    
    plt.figure(figsize=(10, 6))
    plt.hist(degrees, bins=50, color='mediumpurple', edgecolor='black', log=True)
    plt.title('Knowledge Graph: Degree Distribution (Log Scale)', fontsize=14)
    plt.xlabel('Degree', fontsize=12)
    plt.ylabel('Frequency (Log)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plt.savefig(VISUALS_DIR / "degree_distribution.png")
    plt.close()
    
    logger.info(f"visualize_degree_distribution.py complete. Max degree: {max(degrees)}")

def main():
    visualize_degree_distribution()

if __name__ == "__main__":
    main()
