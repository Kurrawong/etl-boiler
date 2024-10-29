"""Helper classes and functions

common utilities that may help to conform to various standards
(like URL normalization, etc)
"""

import re
import string

from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import XSD


class SCM:
    """Simple Column Mapping"""

    col: int
    predicate: URIRef
    obj_func: object

    def __init__(self, col, predicate, obj_func):
        self.col = col
        self.predicate = predicate
        self.obj_func = obj_func


def get_literals(
    text: str,
    delim: str | None = None,
    capture: str | None = None,
    datatype: URIRef = XSD.string,
) -> list[Literal]:
    """Extract RDF literals from the given text.

    :param text: the text containing a literal or literals to extract.
    :param delim: a delimeter seperating the entries.
    :param capture: a regex capture group. If given, only the matched text
                    will be included in the returned literal(s). The regex
                    pattern is applied to each substring after {text} has been
                    split by {delim}.
    :param datatype: An optional datatype to assign to the literals. defaults to xsd:string.
    :returns: A list of Literals.
    """
    text = [text] if not delim else text.split(delim)
    literals = []
    for part in text:
        if isnull(part):
            continue
        part = part.strip()
        if capture:
            matches = re.finditer(capture, part)
            try:
                match = next(matches)
                part = match.group()[0]
            except StopIteration:
                break
        literals.append(Literal(part, datatype=datatype))
    return literals


def get_iris(
    text: str,
    prefix: Namespace | URIRef | str | None = None,
    delim: str | None = None,
    capture: str | None = None,
    normalize: bool = True,
) -> list[URIRef]:
    """Extract RDF IRIs from the given text.

    :param text: the text containing an iri or iris to extract.
    :param prefix: a prefix to use for the iri(s), i.e., http://example.com/
    :param delim: a delimeter seperating the entries.
    :param capture: a regex capture group. If given, only the matched text
                    will be included in the returned iri(s). The regex
                    pattern is applied to each substring after {text} has been
                    split by {delim}.
    :param normalize: if true, normalize the extracted iri to remove any unfreindly characters.
    :returns: a list or URIRefs
    """
    text = [text] if not delim else text.split(delim)
    uris = []
    for part in text:
        if isnull(part):
            continue
        if capture:
            matches = re.finditer(capture, part)
            try:
                match = next(matches)
                part = match.group()[0]
            except StopIteration:
                break
        if normalize:
            part = iri_normalize(part)
        if prefix:
            part = str(prefix) + part
        uris.append(URIRef(part))
    return uris


def iri_normalize(text: str, replacement_char: str = "-") -> str:
    """Remove illegal URL characters from a string."""
    # as per section 2.3 of https://www.ietf.org/rfc/rfc3986.txt
    legal_chars = string.ascii_letters + string.digits + "-" + "_" + "." + "~"
    for char in text:
        if char not in legal_chars:
            text = text.replace(char, replacement_char)
    # clean up leading / trailing / repeated replacement_char
    text = (
        re.sub(rf"{replacement_char}+", replacement_char, text)
        .lstrip(replacement_char)
        .rstrip(replacement_char)
    )
    return text


def isnull(obj, any: bool = False) -> bool:
    """check if obj or any of if its members are null"""
    if not obj:
        return True
    nulls = ["na", "null", "nan", "n.a", "n.d.", "n/a"]
    if isinstance(obj, str):
        obj = [obj]
    null_count = 0
    for member in obj:
        member = member.strip().lower()
        if member in nulls or member == "":
            if any:
                return True
            null_count += 1
    if not any and null_count == len(obj):
        return True
    return False
