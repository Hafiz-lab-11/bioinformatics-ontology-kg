import pandas as pd
from config import GENE2GO_FILE, GENE_GO_MAPPING, TARGET_TAXON_ID, CHUNK_SIZE, GO_RELATION_MAP
from utils import logger

def parse_gene2go():
    """Speed-optimized parser for gene2go.gz with memory-efficient chunking."""
    if not GENE2GO_FILE.exists():
        logger.error(f"Missing input file: {GENE2GO_FILE}")
        return

    logger.info(f"Parsing gene2go associations for Human (9606)...")
    
    first_chunk = True
    total_associations = 0
    unique_genes = set()

    try:
        # Optimization: usecols narrows down the data loaded into memory
        chunks = pd.read_csv(
            GENE2GO_FILE, 
            sep='\t', 
            compression='gzip', 
            chunksize=CHUNK_SIZE,
            usecols=['#tax_id', 'GeneID', 'GO_ID', 'Category']
        )
        
        for chunk in chunks:
            # Filter human early
            filtered = chunk[chunk['#tax_id'] == TARGET_TAXON_ID].copy()
            
            if not filtered.empty:
                # Map categories to relations
                filtered['relation'] = filtered['Category'].map(GO_RELATION_MAP).fillna("associated_with")
                
                # Standardize schema
                # source = Gene, target = GO Term
                filtered['source_id'] = filtered['GeneID'].apply(lambda x: f"NCBIGene:{x}")
                filtered['target_id'] = filtered['GO_ID']
                filtered['source_type'] = "Gene"
                filtered['target_type'] = "OntologyTerm"
                
                output_cols = ['source_id', 'target_id', 'relation', 'source_type', 'target_type']
                
                # Append to output CSV
                mode = 'w' if first_chunk else 'a'
                header = first_chunk
                filtered[output_cols].to_csv(GENE_GO_MAPPING, index=False, mode=mode, header=header)
                
                total_associations += len(filtered)
                unique_genes.update(filtered['source_id'].tolist())
                first_chunk = False
                
        logger.info(f"Gene2GO parsing complete. Extracted {total_associations} associations for {len(unique_genes)} unique genes.")

    except Exception as e:
        logger.error(f"Error parsing gene2go: {e}")

def main():
    parse_gene2go()

if __name__ == "__main__":
    main()