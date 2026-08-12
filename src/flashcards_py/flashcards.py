import inspect
import os
import shlex
from types import FunctionType

from . import commands

type Tree = dict[str, dict[str, FunctionType]]


def build_command_tree() -> Tree:
    tree = {}

    for modname, mod in inspect.getmembers(commands, inspect.ismodule):
        tree[modname] = {
            cmdname[3:]: cmd
            for cmdname, cmd in inspect.getmembers(mod, inspect.isfunction)
            if cmdname.startswith("do_")
        }

    return tree


def command_not_found(input: str, *, is_module: bool = True):
    if is_module:
        print(f"ERROR: Command '{input}' does not exist.")
    else:
        print(f"ERROR: Subcommand '{input}' does not exist.")


def cmdloop(tree: Tree) -> None:
    intro = "Welcome to flashcards.py. Enter a command or type 'help' for a list of commands."
    prompt = "> " if os.name == "nt" else "$ "

    print(intro)

    while True:
        command = input(prompt)
        if not command:
            continue

        split = shlex.split(command)

        if split[0] not in tree:
            command_not_found(split[0])
            continue

        if len(split) == 1:
            # help logic here
            pass

        if len(split) == 2:
            if split[1] in tree[split[0]]:
                # dispatch logic here
                pass
            else:
                command_not_found(split[1], is_module=False)


if __name__ == "__main__":
    tree = build_command_tree()

    try:
        cmdloop(tree)
    except KeyboardInterrupt:
        pass
