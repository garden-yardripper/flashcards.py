from html import escape
from typing import Any, Callable

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML

success = "<ansigreen>SUCCESS:</ansigreen>"
error = "<ansired>ERROR:</ansired>"
warning = "<ansiyellow>WARNING:</ansiyellow>"
info = "<ansigray>INFO:</ansigray>"


def command_not_found(input: str, *, is_module: bool = True):
    if is_module:
        print(HTML(f"{warning} Command '{input}' does not exist."))
    else:
        print(HTML(f"{warning} Subcommand '{input}' does not exist."))


def tag(name: str, *, escape_text: bool = True) -> Callable[[Any], str]:
    def wrapper(text: Any) -> str:
        t = escape(str(text)) if escape_text else str(text)
        return f"<{name}>{t}</{name}>"

    return wrapper


gray = tag("ansiblack")
red = tag("ansired")
green = tag("ansigreen")
yellow = tag("ansiyellow")
blue = tag("ansiblue")
magenta = tag("ansimagenta")
cyan = tag("ansicyan")
white = tag("ansiwhite")
