import inspect
from typing import TYPE_CHECKING

from .utils import string_templates as st

if TYPE_CHECKING:
    from . import Tree


def _get_first_line(obj: object):
    """Get the first line of an object's docstring, or "No description available." if one does not exist."""
    import itertools

    return "".join(itertools.takewhile(lambda c: c != "\n", inspect.getdoc(obj) or "No description available."))


def _truncate_text(text: str, maxlen: int):
    return (text[: maxlen - 3] + "...") if len(text) > maxlen else text


def _space_equally(items: dict[str, str]) -> list[str]:
    import os

    # get the terminal length to get truncation length
    cols = os.get_terminal_size().columns

    # get the longest key to determine the required spacing
    space_length = len(max(items.keys(), key=len)) + 2

    lines = []
    for key, val in items.items():
        spacing = " " * (space_length - len(key))
        lines.append(_truncate_text(("  " + key + spacing + val), cols))

    return lines


def module_help(module_name: str, tree: "Tree") -> str:
    if module_name not in tree:
        st.command_not_found(module_name)
        return ""

    from . import commands

    module_name, module = next((n, m) for n, m in inspect.getmembers(commands, inspect.ismodule) if n == module_name)
    module_doc = _get_first_line(module)

    commands = {
        name[3:]: _get_first_line(func)
        for name, func in inspect.getmembers(module, inspect.isfunction)
        if name.startswith("do_")
    }

    # help command inspired by uv: https://docs.astral.sh/uv/getting-started/help/
    lines = [
        module_doc,
        "",
        f"{st.green('Usage:')} {st.blue(f'{module_name} [SUBCOMMAND] <OPTIONS>')}",
        "",
        f"{st.green('Commands:')}",
        *_space_equally(commands),
        "",
        f"Use '{st.white(f'{module_name} help')}' for more information on a specific command.",
    ]

    return "\n".join(lines)
