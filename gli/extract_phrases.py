import itertools as it
import json
from pathlib import Path
from typing import Any, Generator

import spacy
import srsly
import typer


def fetch_phrases(stream, nlp, hide_det=False):
    for doc in nlp.pipe(stream):
        for chunk in doc.noun_chunks:
            if hide_det:
                yield {"text": " ".join([t for t in chunk if t.pos_ != "DET"])}
            else:
                yield {"text": chunk.text}


def extract_phrases(
    # fmt: off
    file_in: Path = typer.Argument(..., help="A .json file with texts"),
    file_out: Path = typer.Argument(..., help="Output file for phrases. Will print if not provided."),
    model: str = typer.Option(..., help="A spaCy model to load."),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
    hide_det: int = typer.Option(False, help="Only consider top `n` texts.", is_flag=True),
    # fmt: on
):
    stream = (ex["text"] for ex in srsly.read_jsonl(file_in))
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["ents"])
    stream = fetch_phrases(stream, nlp, hide_det=hide_det)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))


if __name__ == "__main__":
    typer.run(extract_phrases)
