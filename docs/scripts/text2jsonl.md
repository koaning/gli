# text2jsonl 

Turns a text file into a jsonl file for you.

## **Arguments**

* `txt-path PATH`: A .txt file

## **Options**

* `--n` **int**: Only consider top `n` texts.
* `--out-path` **Path**: Output file. Will print if not provided.
* `--help`: Show this message and exit.

## Implementation

```python 
import itertools as it
import json
from pathlib import Path

import srsly
import typer


def text2jsonl(
    # fmt: off
    txt_path: Path = typer.Argument(..., help="A .txt file"),
    out_path: Path = typer.Option(None, help="Output file. Will print if not provided."),
    n: int = typer.Option(None, help="Only consider top `n` texts."),
    # fmt: on
):
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
    typer.run(text2jsonl)
```