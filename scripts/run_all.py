from utils import ensure_directories, logger
import parse_ontology
import parse_gene2go
import build_kg
import validate_kg
import visualize_kg
import visualize_relationships
import visualize_degree_distribution
import visualize_centrality
import visualize_paths
import generate_summary
import sys

def main():
    """Main execution entry point for the BioKG pipeline."""
    try:
        # Step 0: Setup environment
        logger.info("Starting Bioinformatics Knowledge Graph Pipeline")
        ensure_directories()

        # Step 1: Parse Ontologies
        logger.info("[STEP 1/10] Parsing ontology files (GO, HP, DOID, UBERON)...")
        parse_ontology.main()

        # Step 2: Parse Gene Associations
        logger.info("[STEP 2/10] Parsing gene-to-GO associations (Human genes)...")
        parse_gene2go.main()

        # Step 3: Build Knowledge Graph & Export CSVs
        logger.info("[STEP 3/10] Merging data and building final Knowledge Graph...")
        build_kg.main()

        # Step 4: Validate Result
        logger.info("[STEP 4/10] Running health and schema validation...")
        validate_kg.main()

        # Step 5: Visualize Core Distribution & Subgraph
        logger.info("[STEP 5/10] Generating core visualizations...")
        visualize_kg.main()
        
        # Step 6: Visualize Relationships & Schema
        logger.info("[STEP 6/10] Generating relationship distribution and schema plots...")
        visualize_relationships.main()
        
        # Step 7: Visualize Degree Distribution
        logger.info("[STEP 7/10] Generating degree distribution plots...")
        visualize_degree_distribution.main()
        
        # Step 8: Centrality Analysis
        logger.info("[STEP 8/10] Computing graph centrality metrics...")
        visualize_centrality.main()
        
        # Step 9: Path Analysis
        logger.info("[STEP 9/10] Performing shortest path analysis between entities...")
        visualize_paths.main()
        
        # Step 10: Summary Report Generation
        logger.info("[STEP 10/10] Generating biological interpretation summary report...")
        generate_summary.main()

        logger.info("Full Pipeline Execution Successfully Completed.")

    except KeyboardInterrupt:
        logger.warning("\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Pipeline crashed due to an unhandled error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()