import json
from pathlib import Path

import spacy
import srsly
import typer


def _filter_categories(docs, cats, threshold):
    for doc, context in docs:
        found_all = all([doc.cats[c] > threshold for c in cats])
        if found_all:
            yield doc, context


def _filter_entities(docs, ents):
    for doc, context in docs:
        found_ents = [_.label_ for _ in doc.ents]
        found_all = all([ent in found_ents for ent in ents])
        if found_all:
            yield doc, context


def model_filter(
    # fmt: off
    file_in: Path = typer.Option(..., help="Path to write text into"),
    file_out: Path = typer.Option(..., help="Path to write text into"),
    spacy_model: Path = typer.Option(..., help="Path to write text into"),
    cat: str = typer.Option(..., help="Path to write text into"),
    threshold: float = typer.Option(0.5, help="threshold"),
    ent: str = typer.Option(..., help="Path to write text into"),
    # fmt: on
):
    """Filter a .jsonl file to only return content where a spaCy
    model is able to detect something of interest.
    """
    nlp = spacy.load(spacy_model)
    stream = (
        (doc, context)
        for doc, context in nlp.pipe(srsly.read_jsonl(file_in), as_tuples=True)
    )
    if cat:
        stream = _filter_categories(stream, cats=cat.split(","), threshold=threshold)
    if ent:
        stream = _filter_entities(stream, cats=cat.split(","), threshold=threshold)
    stream = (context for doc, context in stream)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for item in stream:
            print(json.dumps(item))


if __name__ == "__main__":
    typer.run(model_filter)
