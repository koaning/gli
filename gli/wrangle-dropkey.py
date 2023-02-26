import json
from pathlib import Path

import srsly

# cli.py
from radicli import Radicli, Arg

cli = Radicli()


@cli.command(
    "wrangle.setkey",
    # fmt: off
    input_path=Arg(help="Path to .jsonl file"),
    out_path=Arg("--out-path", help="Output file. Will print if not provided."),
    keys=Arg("--keys", help="Key to override, like 'foo,bar,buz'"),
    # fmt: on
)
def wrangle_dropkey(input_path: Path, out_path: Path = None, keys: str = None):
    """Turns a text file into a jsonl file for you."""
    stream = srsly.read_jsonl(input_path)
    to_delete = keys.split(",")

    def remove_keys(item):
        for k in to_delete:
            del item[k]
        return item

    g = (remove_keys(ex) for ex in stream)

    if out_path:
        srsly.write_jsonl(out_path, g)
    else:
        for ex in g:
            print(json.dumps(ex))


if __name__ == "__main__":
    cli.run()
