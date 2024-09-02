import csv
from pathlib import Path
from uuid import uuid4

from dirs import input_dir, output_dir
from namespaces import BASE, DS, ROLES, VOCAB, graph
from patterns import observation, qualified_association
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCAT, DCTERMS, RDF, XSD
from utils import SCM, get_iris, get_literals, write_progress


def convert(source: Path, id_col: int | None = 0) -> Graph:
    g = Graph()
    simple_mappings = [
        SCM(col=1, predicate=DCTERMS.title, obj_func=lambda x: get_literals(x)),
        SCM(col=2, predicate=DCTERMS.description, obj_func=lambda x: get_literals(x)),
        SCM(
            col=3,
            predicate=DCTERMS.creator,
            obj_func=lambda x: get_iris(x, delim="||", normalize=True),
        ),
        SCM(
            col=4,
            predicate=DCTERMS.created,
            obj_func=lambda x: get_literals(x, datatype=XSD.gYear),
        ),
    ]
    with open(source, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for i, row in enumerate(reader, start=1):
            write_progress(i, message=f"Processing {source.name}")

            # if the source does not contain a unique identifier, create one
            if not id_col:
                s = BASE[str(uuid4())]
            else:
                s = BASE[row[str(id_col)]]

            # add row metadata
            g.add((s, RDF.type, DCAT.Resource))
            g.add((s, DCTERMS.isPartOf, DS))

            # simple column mappings
            for mapping in simple_mappings:
                p = mapping.predicate
                objs = mapping.obj_func(row[mapping.col])
                for o in objs:
                    g.add((s, p, o))

            # a qualified relation
            for agent in get_iris(row[6]):
                g += qualified_association(subject=s, agent=agent, role=ROLES.reviewer)

            # a sosa observation
            op = URIRef(s + "/" + header[5])
            value = Literal(row[5], datatype=XSD.float)
            g += observation(
                subject=s, observed_property=op, value=value, units=VOCAB.stars
            )
    return g


if __name__ == "__main__":
    graph += convert(input_dir / "example.csv")
    graph.serialize(destination=output_dir / "example.ttl", format="turtle")
