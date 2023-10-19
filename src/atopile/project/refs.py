"""
Refs module provides utilities to manage references to objects in the form of `path/to/thing.ato:path.within.thing`
"""

from pathlib import Path
from typing import Optional

class Ref:
    def __init__(self, to: Optional[Path] = None, within: Optional[tuple[str]] = None) -> None:
        self.to = to
        self.within = within

    def __str__(self) -> str:
        to_str = str(self.to) if self.to else ""
        within_str = ".".join(self.within) if self.within else ""

        if within_str:
            return to_str + ":" + within_str
        return to_str

    @classmethod
    def from_str(cls, ref: str) -> "Ref":
        self = cls()
        comps = ref.split(":")
        if len(comps) == 1:
            self.to = Path(comps[0])
        elif len(comps) == 2:
            self.to = Path(comps[0])
            self.within = tuple(comps[1].split("."))
        else:
            raise ValueError(f"Malformed ref: {ref}. Too many colons")

        return self
