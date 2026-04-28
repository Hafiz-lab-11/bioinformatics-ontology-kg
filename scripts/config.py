from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
LOG_DIR = BASE_DIR / "logs"

# Data Files
ONTOLOGY_FILES = {
    "go": RAW_DIR / "go.obo",
    "hp": RAW_DIR / "hp.obo",
    "uberon": RAW_DIR / "uberon.obo",
    "disease": RAW_DIR / "disease.obo",
}
GENE2GO_FILE = RAW_DIR / "gene2go.gz"

# Output Files
ONTOLOGY_JSON = PROCESSED_DIR / "ontologies.json"
GENE_GO_MAPPING = PROCESSED_DIR / "gene_go_mapping.csv"
NODES_CSV = OUTPUT_DIR / "nodes.csv"
EDGES_CSV = OUTPUT_DIR / "edges.csv"
FINAL_KG_PATH = OUTPUT_DIR / "bio_kg.graphml"
VISUALS_DIR = OUTPUT_DIR / "visuals"
SUBGRAPH_DIR = OUTPUT_DIR / "subgraph"

# Parameters
TARGET_TAXON_ID = 9606  # Human
CHUNK_SIZE = 100000     # Memory efficiency for large files

# Mapping GO categories to biological relations
GO_RELATION_MAP = {
    "Process": "involved_in",
    "Function": "enables",
    "Component": "part_of"
}

# Validation Constants
ALLOWED_NODE_TYPES = {
    "Gene",
    "OntologyTerm",
    "Disease",
    "Phenotype",
    "Anatomy",
    "BiologicalProcess",
    "MolecularFunction",
    "CellularComponent",
}
ALLOWED_RELATIONS = {
    "is_a",
    "part_of",
    "regulates",
    "positively_regulates",
    "negatively_regulates",
    "develops_from",
    "involved_in",
    "enables",
}
