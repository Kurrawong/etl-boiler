"""Tdb loader utility

loads output data into a tdb2 database for use in the 
Apache Jena Fuseki triple store.
"""

import shutil
import logging
from subprocess import run

from dirs import background_dir, output_dir, tdb_dir
from namespaces import NAMED_GRAPH
from logs import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def validate() -> None:
    logger.info("validating data")
    for file in output_dir.glob("*.trig"):
        run([riot_binary, "--validate", file], check=True)
    for file in background_dir.glob("*.ttl"):
        run([riot_binary, "--validate", file], check=True)
    return


def clear_existing():
    if tdb_dir.exists():
        logger.info("removing existing tdb directory")
        shutil.rmtree(tdb_dir)
    logger.info("creating new tdb directory")
    tdb_dir.mkdir()
    return


def load_background():
    named_graph = NAMED_GRAPH["background"]
    files = [file for file in background_dir.glob("*.ttl")]
    if not files:
        logger.info("no background data to load")
        return
    logger.info("loading background data")
    args = [
        tdb2loader_binary,
        f"--loc={tdb_dir}",
        f"--graph={named_graph}",
        "--loader=parallel",
    ]
    [args.append(file) for file in files]
    run(args, check=True)
    return


def load_outputs():
    files = [file for file in output_dir.glob("*.trig")]
    if not files:
        logger.info("no output data to load")
        return
    logger.info("loading output data")
    args = [tdb2loader_binary, f"--loc={tdb_dir}", "--loader=parallel"]
    [args.append(file) for file in files]
    run(args, check=True)
    return


if __name__ == "__main__":
    riot_binary = "/usr/local/apache-jena-5.1.0/bin/riot"
    tdb2loader_binary = "/usr/local/apache-jena-5.1.0/bin/tdb2.tdbloader"
    validate()
    clear_existing()
    load_background()
    load_outputs()
