from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import NamespaceManager

# The dataset being created
BASE = Namespace("http://example.com/dataset/112-222-333/")
DS = URIRef("http://example.com/dataset/112-222-333")

# Custom Vocabularies
ROLES = Namespace("http://example.com/roles/")
VOCAB = Namespace("http://example.com/vocab/")

# External Ontologies not in rdflib
QUDT = Namespace("http://qudt.org/schema/qudt/")


# Bindings
graph = Graph()
graph.base = BASE

nsm = NamespaceManager(graph)
nsm.bind("roles", ROLES)
nsm.bind("vocab", VOCAB)
nsm.bind("qudt", QUDT)
