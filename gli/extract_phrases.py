import itertools as it
import json
from pathlib import Path

import spacy
import srsly

from radicli import Radicli, Arg

cli = Radicli()


def _fetch_phrases(stream, nlp, keep_det=False):
    for doc in nlp.pipe(stream):
        for chunk in doc.noun_chunks:
            if keep_det:
                yield chunk.text
            else:
                yield " ".join([t.text for t in chunk if t.pos_ != "DET"])


@cli.command(
    # fmt: off
    "extract-phrases",
    file_in=Arg(help="A .jsonl file with texts"),
    output=Arg("--output", help="Output .jsonl with phrases. Will print if not provided"),
    model=Arg("--model", help="spaCy model to use"),
    n=Arg("--n","-n", help="Only consider top `n` texts."),
    keep_det=Arg("--keep-det", help="Keep determinant in phrase.")
    # fmt: on
)
def extract_phrases(
    file_in: Path,
    model: str,
    n: int,
    keep_det: int,
    output: Path = None,
):
    """Turns a `.jsonl` with text into a `.jsonl` with extracted phrases."""
    stream = (ex["text"] for ex in srsly.read_jsonl(file_in))
    if n:
        stream = it.islice(stream, n)
    nlp = spacy.load(model, disable=["ents"])
    stream = set(_fetch_phrases(stream, nlp, keep_det=keep_det))
    stream = ({"text": txt} for txt in stream)
    if output:
        srsly.write_jsonl(output, stream)
    else:
        for ex in stream:
            print(json.dumps(ex))


if __name__ == "__main__":
    cli.run()
