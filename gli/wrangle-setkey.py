import itertools as it
import json
from pathlib import Path

import srsly
import typer

# cli.py
from radicli import Radicli, Arg

cli = Radicli()


@cli.command(
    "wrangle.setkey",
    # fmt: off
    input_path=Arg(help="Path to .jsonl file"),
    out_path=Arg("--out-path", help="Output file. Will print if not provided."),
    keys=Arg("--keys", help="Key to override, like 'foo:bar,buz:bla'"),
    # fmt: on
)
def wrangle_setkey(input_path: Path, out_path: Path = None, keys: str = None):
    """Turns a text file into a jsonl file for you."""
    stream = srsly.read_jsonl(input_path)
    translator = {}
    for pair in keys.split(","):
        k, v = pair.split(":")
        translator[k] = v

    def replace_keys(item):
        for k, v in translator.items():
            item[k] = v
        return item

    g = (replace_keys(ex) for ex in stream)

    if out_path:
        srsly.write_jsonl(out_path, g)
    else:
        for ex in g:
            print(json.dumps(ex))


if __name__ == "__main__":
    cli.run()
