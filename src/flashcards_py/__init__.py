from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import FunctionType

type Tree = dict[str, dict[str, "FunctionType"]]
