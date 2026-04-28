import pandas as pd
from config import NODES_CSV, EDGES_CSV, OUTPUT_DIR, VISUALS_DIR
from utils import logger
from datetime import datetime

def generate_report():
    """Generate a text-based summary of the Knowledge Graph and its biological significance."""
    if not NODES_CSV.exists() or not EDGES_CSV.exists():
        logger.error("CSVs missing.")
        return

    nodes_df = pd.read_csv(NODES_CSV)
    edges_df = pd.read_csv(EDGES_CSV)

    num_nodes = len(nodes_df)
    num_edges = len(edges_df)
    
    node_types = nodes_df['node_type'].value_counts().to_dict()
    relation_types = edges_df['relation'].value_counts().to_dict()

    project_name = "Bioinformatics Ontology"
    report_content = f"""# {project_name} Knowledge Graph Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Graph Statistics
- Total Nodes: {num_nodes}
- Total Edges: {num_edges}

### Node Type Breakdown:
{chr(10).join([f"  - {t}: {c}" for t, c in node_types.items()])}

### Edge Relationship Breakdown:
{chr(10).join([f"  - {r}: {c}" for r, c in relation_types.items()])}

## 2. Biological Interpretation
This Knowledge Graph (KG) represents a multi-scale biological network integrating human genetic data with formal ontologies.

- **Genetic Basis:** It contains {node_types.get('Gene', 0)} Human Genes linked to Gene Ontology (GO) terms via 'enables' (functions), 'involved_in' (processes), and 'part_of' (cellular components).
- **Functional Context:** The high frequency of ontology terms ({node_types.get('OntologyTerm', 0)}) paired with hierarchical 'is_a' relationships allows for computational reasoning across biological scales—from molecular function to cellular anatomy (UBERON) and phenotypic manifestations (HP).
- **Clinical Relevance:** By connecting human genes to Disease (DOID) and Human Phenotype (HP) ontologies, this KG serves as a framework for identifying gene-disease associations and potential pathways involved in disease etiology.

## 3. Potential Applications
- **Path Analysis:** Identifying shortest paths between genes and phenotypes to discover candidate mechanisms.
- **Centrality Analysis:** High-degree nodes (hubs) may indicate multi-functional genes or central biological processes critical to cell survival.
- **Data Mining:** A structured substrate for machine learning models (e.g., Graph Neural Networks) to predict novel gene-disease links.

---
Conclusion: This KG provides a standardized, modular representation of biological knowledge, suitable for research and clinical interpretation.
"""

    # Save to visuals directory as final_summary.txt
    summary_path = VISUALS_DIR / "final_summary.txt"
    with open(summary_path, 'w') as f:
        f.write(report_content)
    
    logger.info(f"generate_summary.py: Final summary saved to {summary_path}")

def main():
    generate_report()

if __name__ == "__main__":
    main()
