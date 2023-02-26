import itertools as it
import json
from pathlib import Path

import srsly
import typer

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
def text2jsonl(txt_path: Path, out_path: Path = None, n: int = None):
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


def mkline(arg):
    if arg["option"]:
        return f"* `--{arg['name']}`: {arg['help']}\n"
    return f"* `{arg['name']}`: {arg['help']}\n"


def parse_command(cmd):
    msg = f"\n## {cmd.name}\n\n"
    msg += f"{cmd.func.__doc__}\n"
    parsed_args = []
    for arg in cmd.args:
        parsed_args.append(
            {
                "name": arg.id,
                "type": arg.type.__name__,
                "help": arg.arg.help,
                "option": arg.arg.option,
                "short": arg.arg.short,
                "default": arg.arg.short,
            }
        )
    if any([not a["option"] for a in parsed_args]):
        msg += "\n**Arguments**\n\n"
        for arg in parsed_args:
            if not arg["option"]:
                msg += mkline(arg)
    if any([a["option"] for a in parsed_args]):
        msg += "\n**Options**\n\n"
        for arg in parsed_args:
            if arg["option"]:
                msg += mkline(arg)
        # msg += f"* `{arg['id}` **{arg.type.__name__}**: {arg.arg.help}\n"
    print(msg)


cmd = cli.commands["text2jsonl"]

parse_command(cmd)
