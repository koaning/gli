import inspect

from text2jsonl import main as text2jsonl


def generate_docs(func):
    out = f"\n\n{func.__doc__}\n"
    arguments = []
    options = [{"name": "help", "type": "", "help": "Show this message and exit."}]
    for k, v in inspect.signature(text2jsonl).parameters.items():
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
        out += "\n**Arguments**\n\n"
        for arg in arguments:
            out += f"* `{arg['name'].replace('_', '-')} {arg['type'].upper()}`: {arg['help']}"
        out += "\n"
    if options:
        out += "\n**Arguments**\n\n"
        for opt in reversed(options):
            name = f"--{opt['name'].replace('_', '-')} {opt['type'].upper()}"
            out += f"* `{name.strip()}`: {opt['help']}\n"
    print(out)


if __name__ == "__main__":
    generate_docs(text2jsonl)
