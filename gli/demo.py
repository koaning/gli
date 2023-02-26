from radicli import Radicli, Arg


cli = Radicli()

@cli.command(
    "speak",
    n=Arg("--n", "-n", help="Only convert a given amount of lines"),
)
def speak(n: int):
    for _ in range(n):
        print("hello")


if __name__ == "__main__":
    cli.run()

# Feedback

# 2. being able to run a single function without calling the function name
# 3. maybe more helpful feedback when an Arg is mistaken as an Option? Something like "i got this but i need that" right now i just get `unrecognized arguments: mkdocs.yml foobar.jsonl``

