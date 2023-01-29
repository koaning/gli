import itertools as it
import json
from pathlib import Path

import srsly
import typer


def text2jsonl(
    txt_path: Path = typer.Argument(..., help="A .txt file"),
    out_path: Path = typer.Option(
        None, help="Output file. Will print if not provided."
    ),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
):
    """This prints your name"""

    with open(txt_path, "r") as f:
        lines = f.readlines()

    g = ({"text": text.replace("\n", "")} for text in lines)
    if n:
        g = it.islice(g, n)
    if out_path:
        srsly.write_jsonl(out_path, g)
    else:
        for ex in g:
            print(json.dumps(ex))


if __name__ == "__main__":
    typer.run(text2jsonl)
