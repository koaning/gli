# extract_phrases 

Turns a `.jsonl` with text into a `.jsonl` with extracted phrases.

## **Arguments**

* `file-in PATH`: A .json file with texts* `file-out PATH`: Output file for phrases. Will print if not provided.

## **Options**

* `--keep-det` **int**: Only consider top `n` texts.
* `--n` **int**: Only consider top `n` texts.
* `--model` **str**: A spaCy model to load.
* `--help`: Show this message and exit.

## Implementation

```python 
import itertools as it
import json
from pathlib import Path

import spacy
import srsly
import typer


def _fetch_phrases(stream, nlp, keep_det=False):
    for doc in nlp.pipe(stream):
        for chunk in doc.noun_chunks:
            if keep_det:
                yield {"text": chunk.text}
            else:
                yield {"text": " ".join([t for t in chunk if t.pos_ != "DET"])}


def extract_phrases(
    # fmt: off
    file_in: Path = typer.Argument(..., help="A .json file with texts"),
    file_out: Path = typer.Argument(..., help="Output file for phrases. Will print if not provided."),
    model: str = typer.Option(..., help="A spaCy model to load."),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
    keep_det: int = typer.Option(False, help="Only consider top `n` texts.", is_flag=True),
    # fmt: on
):
    """Turns a `.jsonl` with text into a `.jsonl` with extracted phrases."""
    stream = (ex["text"] for ex in srsly.read_jsonl(file_in))
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["ents"])
    stream = _fetch_phrases(stream, nlp, keep_det=keep_det)
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))


if __name__ == "__main__":
    typer.run(extract_phrases)
```