import inspect
import os
import shlex
from types import FunctionType

from . import commands
from .utils.string_templates import command_not_found

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


def cmdloop(tree: Tree) -> None:
    intro = "Welcome to flashcards.py. Enter a command or type 'help' for a list of commands."
    prompt = "> " if os.name == "nt" else "$ "

    print(intro)

    while True:
        command = input(prompt)
        if not command:
            continue

        split = shlex.split(command)
        module = split[0]

        if module not in tree:
            # handle uncategorized command functions defined in the any module
            if module in tree["any"]:
                tree["any"][module]()
            else:
                command_not_found(module)

            continue

        if len(split) == 1:
            # help logic here
            pass

        if len(split) == 2:
            subcmd = split[1]
            if subcmd in tree[module]:
                tree[module][subcmd]()
            else:
                command_not_found(subcmd, is_module=False)


if __name__ == "__main__":
    tree = build_command_tree()

    try:
        cmdloop(tree)
    except KeyboardInterrupt:
        pass
