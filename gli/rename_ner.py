import json
from pathlib import Path

import srsly
import typer


def _replace_ents(item, table):
    for span in item["spans"]:
        for k, v in table.items():
            if span["label"] == k:
                span["label"] = v
    return item


def rename_ner(
    # fmt: off
    file_in: Path = typer.Option(None, help="Path to write text into"),
    file_out: Path = typer.Option(None, help="Path to write text into"),
    translate: str = typer.Option(..., help="Path to write text into"),
    # fmt: on
):
    """Rename a named entity label in a Prodigy .jsonl file"""
    pairs = [kv for kv in translate.split(",")]
    ent_table = dict([kv.split(":") for kv in pairs])
    stream = (_replace_ents(ex, ent_table) for ex in srsly.read_jsonl(file_in))
    if file_out:
        srsly.write_jsonl(file_out, stream)
    else:
        for item in stream:
            print(json.dumps(item))


if __name__ == "__main__":
    typer.run(rename_ner)
