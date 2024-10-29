"""do SHACL and other validations here"""

import logging

from dirs import background_dir, output_dir
from labelify import find_missing_labels
from logs import setup_logging
from rdflib import Graph, Dataset

setup_logging()

logger = logging.getLogger(__name__)


def check_labels():
    """Ensure that all resources are properly labelled"""
    logger.info("loading background data")
    cg = Graph()
    for file in background_dir.glob("*.ttl"):
        cg.parse(file)

    logger.info("loading output data")
    d = Dataset()
    for file in output_dir.glob("*.trig"):
        d.parse(file, format="trig")

    # BUG: something wrong with the trig parser
    assert d.value(None, None, default=None), "Error: output graph is empty"

    logger.info("looking for labels")
    missing_labels = find_missing_labels(graph=d, context_graph=cg)
    if missing_labels:
        raise Exception(
            "The following resources do not have labels:\n" + "\n".join(missing_labels)
        )
    logger.info("all resources have labels")


if __name__ == "__main__":
    check_labels()
