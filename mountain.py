from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: int
    difficulty_level : int
    length: int

    def __hash__(self) -> int:
        return hash(Mountain)
    
    
    def __eq__(self, other):
        return self.name == other.name and self.difficulty_level == self.difficulty_level and self.length == other.length

    def __ne__(self, other):
        if self.length == other.length:
            return self.name != other.name
        return self.length != other.length

    def __lt__(self, other):
        if self.length == other.length:
            return self.name < other.name
        return self.length < other.length

    def __le__(self, other):
        if self.length == other.length:
            return self.name <= other.name
        return self.length <= other.length

    def __gt__(self, other):
        if self.length == other.length:
            return self.name > other.name
        return self.length > other.length

    def __ge__(self, other):
        if self.length == other.length:
            return self.name >= other.name
        return self.length >= other.length
