"""Common RDF modelling patterns

Usage of these patterns will enforce best practice and standardization
for common modelling scenarios.

These should be added to as needed.
"""

import logging

from namespaces import QUDT
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import DCAT, GEO, PROV, RDF, SDO, SKOS, SOSA, TIME
from utils import isnull

logger = logging.getLogger(__name__)


def qualified_association(subject: URIRef, agent: URIRef, role: URIRef) -> Graph:
    """A prov qualified association

        {subject} prov:qualifiedAssociation [
            a prov:Association ;
            prov:agent {agent} ;
            prov:hadRole {role}
        ] .

    :param subject: The subject of the association.
    :param agent: The agent associated with the subject.
    :param role: The role that agent played with respect the subject.
    :return: A Graph containing the triples.

    See: https://www.w3.org/TR/2013/REC-prov-o-20130430/#qualifiedAssociation
    """
    g = Graph()
    if isnull([subject, agent, role], any=True):
        logger.error("qualified_association requires subject, agent, and role")
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
    """A sosa Observation

        {subject} sosa:isFeatureOfInterestOf [
            a sosa:Observation ;
            sosa:observedProperty {observed_property} ;
            sosa:hasResult [
                a sosa:Result ;
                sosa:hasValue {value} ;
                sosa:hasUnit {units}
            ]
        ].

    :param subject: the feature of interest
    :param observed_property: the observed property
    :param value: a numerical value
    :param units: the unit of measurement
    :return: a graph containing the triples

    See: https://www.w3.org/TR/vocab-ssn/#Observations
    """
    g = Graph()
    if isnull([subject, observed_property, value, units], any=True):
        logger.error("observation requires subject, observed_property, value, and units")
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


def temporal_interval(subject: URIRef, start: Literal, end: Literal) -> Graph:
    """A time temporal interval

        {subject} time:hasTime [
            a time:Interval ;
            time:intervalStarts {start} ;
            time:intervalFinishes {end}
        ].

    :param subject: the subject of the temporal interval
    :param start: start of the interval
    :param end: end of the interval
    :return: a graph containing the triples

    See: https://www.w3.org/TR/owl-time/#time:Interval
    """
    g = Graph
    if isnull([subject, start, end], any=True):
        return g
    interval = BNode()
    g.add((interval, RDF.type, TIME.Interval))
    g.add((subject, TIME.hasTime, interval))
    g.add((interval, TIME.intervalStarts, start))
    g.add((interval, TIME.intervalFinishes, end))
    return g


def geometry(subject: URIRef, wkt: Literal) -> Graph:
    """A geo geometry

        {subject} geo:hasGeometry [
            a geo:Geometry ;
            geo:asWKT {wkt}
        ].

    :param subject: the subject of the geometry
    :param wkt: well known text literal for the geometry
    :return: a graph containing the triples

    See: https://opengeospatial.github.io/ogc-geosparql/geosparql10/geo.html#Geometry
    """
    g = Graph()
    if isnull([subject, wkt], any=True):
        return g
    geom = BNode()
    g.add((geom, RDF.type, GEO.Geometry))
    g.add((subject, GEO.hasGeometry, geom))
    g.add((geom, GEO.asWKT, wkt))
    return g


def concept(subject: URIRef, label: Literal, concept_scheme: URIRef):
    """A skos concept

        {subject} a skos:Concept ;
            skos:inScheme {concept_scheme} ;
            skos:prefLabel {label} .

    :param subject: the concept iri
    :param label: a label for the concept
    :param concept_scheme: A concept scheme to which the concept belongs
    :return: a graph containing the triples

    See: https://www.w3.org/TR/skos-reference/#concepts
    """
    g = Graph()
    if isnull([subject, label, concept_scheme], any=True):
        return g
    g.add((subject, RDF.type, SKOS.Concept))
    g.add((subject, SKOS.inScheme, concept_scheme))
    g.add((subject, SKOS.prefLabel, label))
    return g


def agent(subject: URIRef, agent_type: URIRef, name: Literal):
    """an sdo agent

    :param subject: the iri of the agent
    :param agent_type: an sdo class (eg. sdo:Person or sdo:Organization)
    :param name: the agents name
    :return: a graph containing the triples
    """
    g = Graph()
    if isnull([subject, name], any=True):
        return g
    g.add((subject, RDF.type, agent_type))
    g.add((subject, SDO.name, name))
    return g
