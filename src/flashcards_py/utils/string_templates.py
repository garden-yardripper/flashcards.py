from html import escape
from typing import Any, Callable

success = "<ansigreen>SUCCESS:</ansigreen>"
error = "<ansired>ERROR:</ansired>"
warning = "<ansiyellow>WARNING:</ansiyellow>"


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
