import difflib
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


def fuzzy_match(
    input_string: str, list_of_strings: list[str], threshold: int = 0.93
) -> list[tuple]:
    """Get a list of potential duplicates using pythons sequence matcher.

    :param input_string: the string to search for.
    :param list_of_strings: a list of strings to search for duplicates in.
    :param theshold: similarity threshold [0-1].
    :returns: A list of tuples containing potential matches and their similarity score.
    """
    matches = []
    for candidate in list_of_strings:
        sm = difflib.SequenceMatcher(None, input_string, candidate)
        upper_bound = sm.real_quick_ratio()
        if upper_bound > threshold:
            ratio = sm.ratio()
            if ratio > threshold:
                matches.append((candidate, ratio))
    return matches


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


def iri_normalize(text: str) -> str:
    """Remove illegal URL characters from a string."""
    # as per section 2.3 of https://www.ietf.org/rfc/rfc3986.txt
    legal_chars = string.ascii_letters + string.digits + "-" + "_" + "." + "~"
    # replace illegal characters with a dash
    for char in text:
        if char not in legal_chars:
            text = text.replace(char, "-")
    # clean up leading / trailing / repeated dashes
    text = re.sub(r"-+", "-", text).lstrip("-").rstrip("-")
    return text


def isnull(text: str) -> bool:
    """check if a cell is some representation of null"""
    if not text:
        return True
    text = text.strip().lower()
    nas = ["na", "null", "nan", "n.a", "n.d.", "n/a"]
    if text in nas or text == "":
        return True
    return False


def write_progress(i: int, total: int | None = None, message: str = "") -> None:
    """Write progress to stdout.

    :param i: number of thing currently being processed.
    :param total: total number of things to be processed.
    :param message: a description of the task being done.
    """
    if total:
        pc_complete = round((i / total) * 100)
    else:
        pc_complete = "?"
    print(
        f"    {message}: [{str(pc_complete).center(5)}% ] {str(i).rjust(len(str(total)))}/{total if total else '?'}",
        end="\r",
        flush=True,
    )
    if total and i == total:
        print("\n", end="")
    return
