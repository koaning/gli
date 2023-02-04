import inspect
from pathlib import Path

from dropkey import dropkey
from extract_phrases import extract_phrases
from model_filter import model_filter
from rename_ner import rename_ner
from text2jsonl import text2jsonl


def generate_docs(func):
    """Can generate a doc file from a func."""
    out = f"# {func.__name__} \n\n{func.__doc__}\n"
    arguments = []
    options = [{"name": "help", "type": "", "help": "Show this message and exit."}]
    for k, v in inspect.signature(func).parameters.items():
        item = {
            "name": k,
            "type": v.annotation.__name__,
            "help": v.default.help,
        }
        if "Option" in v.default.__class__.__name__:
            options.append(item)
        else:
            arguments.append(item)
    out += "\n"
    if arguments:
        out += "## **Arguments**\n\n"
        for arg in arguments:
            out += f"* `{arg['name'].replace('_', '-')} {arg['type'].upper()}`: {arg['help']}"
        out += "\n"
    if options:
        out += "\n## **Options**\n\n"
        for opt in reversed(options):
            name = f"`--{opt['name'].replace('_', '-')}`"
            if opt["type"].upper():
                name += f" **{opt['type']}**"
            out += f"* {name.strip()}: {opt['help']}\n"
    out += "\n## Implementation\n\n"
    pypath = Path("gli") / f"{func.__name__}.py"
    out += "```python \n"
    out += pypath.read_text()
    out += "```"
    out_file = Path("docs") / "scripts" / f"{func.__name__}.md"
    out_file.write_text(out)


if __name__ == "__main__":
    funcs = [extract_phrases, text2jsonl, rename_ner, model_filter, dropkey]
    for func in funcs:
        generate_docs(func)
