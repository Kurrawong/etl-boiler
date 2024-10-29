"""Namespace declarations and bindings go here.

These will need to be updated on a per project basis.
"""

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import NamespaceManager

# The dataset being created
BASE = Namespace("http://example.com/dataset/example-dataset/")
DS = URIRef("http://example.com/dataset/example-dataset")

# Custom Vocabularies
ROLES = Namespace("http://example.com/roles/")
VOCAB = Namespace("http://example.com/vocab/")

# External Ontologies not in rdflib
QUDT = Namespace("http://qudt.org/schema/qudt/")

# A namespace for named graphs
NAMED_GRAPH = Namespace("http://example.com/graphs/")


# Bindings
ns_graph = Graph()
ns_graph.base = BASE

nsm = NamespaceManager(ns_graph)
nsm.bind("roles", ROLES)
nsm.bind("vocab", VOCAB)
nsm.bind("qudt", QUDT)
