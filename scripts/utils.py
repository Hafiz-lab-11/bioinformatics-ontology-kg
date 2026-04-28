import logging
import sys
from config import LOG_DIR, PROCESSED_DIR, OUTPUT_DIR

def setup_logger():
    """Configure and return the pipeline logger."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler(LOG_DIR / "pipeline.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("BioKG")

logger = setup_logger()

def ensure_directories():
    """Ensure that all necessary directories exist using pathlib."""
    from config import VISUALS_DIR, SUBGRAPH_DIR
    for d in [LOG_DIR, PROCESSED_DIR, OUTPUT_DIR, VISUALS_DIR, SUBGRAPH_DIR]:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {d}")
        else:
            logger.debug(f"Directory verified: {d}")