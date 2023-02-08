import itertools as it
import json
from pathlib import Path

import srsly
import typer

# cli.py
from radicli import Radicli, Arg

cli = Radicli()

@cli.command(
    "text2jsonl",
    # fmt: off
    txt_path=Arg(help="Path to .txt file"),
    out_path=Arg("--out-path", help="Output file. Will print if not provided."),
    n=Arg("--n", help="Number of lines to use"),
    # fmt: on
)
def text2jsonl(txt_path: Path, out_path: Path = None, n: int=None):
    """Turns a text file into a jsonl file for you."""

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
    cli.run()
