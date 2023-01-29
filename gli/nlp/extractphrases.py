import spacy 
import itertools as it
import json
from pathlib import Path

import srsly
import typer


def fetch_phrases(stream, nlp):
    for doc in nlp.pipe(stream):
        print(doc.text)
        print([c.text for c in doc.noun_chunks])
        for chunk in doc.noun_chunks:
            yield {"text": chunk.text}
            
def extract_phrases(
    # fmt: off
    file_in: Path = typer.Argument(..., help="A .json file with texts"),
    file_out: Path = typer.Argument(..., help="Output file for phrases. Will print if not provided."),
    model: str = typer.Option(..., help="A spaCy model to load."),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
    # fmt: on
):
    stream = (ex['text'] for ex in srsly.read_jsonl(file_in))
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["tok2vec", "ents", "tagger", "attribute_ruler", "lemmatizer"])
    stream = fetch_phrases(stream, nlp)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))

if __name__ == "__main__":
    typer.run(extract_phrases)