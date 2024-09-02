from namespaces import QUDT
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import DCAT, GEO, PROV, RDF, SOSA, TIME
from utils import isnull


def qualified_association(subject: URIRef, agent: URIRef, role: URIRef) -> Graph:
    g = Graph()
    if any([isnull(subject), isnull(agent), isnull(role)]):
        return g
    assoc = BNode()
    g.add((subject, PROV.qualifiedAssociation, assoc))
    g.add((assoc, RDF.type, PROV.Association))
    g.add((assoc, PROV.agent, agent))
    g.add((assoc, DCAT.hadRole, role))
    return g


def observation(
    subject: URIRef,
    observed_property: URIRef,
    value: Literal,
    units: URIRef,
) -> Graph:
    g = Graph()
    if any([isnull(subject), isnull(observed_property), isnull(value), isnull(units)]):
        return g
    obs = BNode()
    res = BNode()
    g.add((obs, RDF.type, SOSA.Observation))
    g.add((res, RDF.type, SOSA.Result))
    g.add((subject, SOSA.isFeatureOfInterestOf, obs))
    g.add((obs, SOSA.observedProperty, observed_property))
    g.add((obs, SOSA.hasResult, res))
    g.add((res, QUDT.numericValue, value))
    g.add((res, QUDT.unit, units))
    return g


def interval(subject: URIRef, start: Literal, end: Literal):
    g = Graph
    if any([isnull(subject), isnull(start), isnull(end)]):
        return g
    interval = BNode()
    g.add((interval, RDF.type, TIME.Interval))
    g.add((subject, TIME.hasTime, interval))
    g.add((interval, TIME.intervalStarts, start))
    g.add((interval, TIME.intervalFinishes, end))
    return g


def geometry(subject: URIRef, wkt: Literal) -> Graph:
    g = Graph()
    if any([isnull(subject), isnull(wkt)]):
        return g
    geom = BNode()
    g.add((geom, RDF.type, GEO.Geometry))
    g.add((subject, GEO.hasGeometry, geom))
    g.add((geom, GEO.asWKT, wkt))
    return g
