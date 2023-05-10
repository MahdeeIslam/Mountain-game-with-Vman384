from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __hash__(self) -> int:
        return hash(Mountain)
 