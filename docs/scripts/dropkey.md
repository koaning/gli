# dropkey 

Drop a few keys from a .jsonl file.

## **Arguments**

* `file-in PATH`: .jsonl path to load in

## **Options**

* `--keys` **str**: Keys to drop
* `--file-out` **Path**: Path to write jsonl out
* `--help`: Show this message and exit.

## Implementation

```python 
import json
from pathlib import Path

import srsly
import typer


def _drop_keys(item, keys):
    for key in keys:
        if key in item:
            del item[key]
    return item


def dropkey(
    # fmt: off
    file_in: Path = typer.Argument(..., help=".jsonl path to load in"),
    file_out: Path = typer.Option(None, help="Path to write jsonl out"),
    keys: str = typer.Option(..., help="Keys to drop"),
    # fmt: on
):
    """Drop a few keys from a .jsonl file."""
    keys = keys.split(",")
    stream = (_drop_keys(ex, keys) for ex in srsly.read_jsonl(file_in))
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for item in stream:
            print(json.dumps(item))


if __name__ == "__main__":
    typer.run(dropkey)
```