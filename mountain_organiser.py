from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    
    def _compare_mountains(self, m1: Mountain, m2: Mountain) -> int:
        if m1.length == m2.length:
            if m1.name < m2.name:
                return -1
            elif m1.name > m2.name:
                return 1
            else:
                return 0
        return -1 if m1.length < m2.length else 1
    
    
    
    def _binary_search(self, mountain: Mountain) -> int:
        left, right = 0, len(self.mountains) - 1

        while left <= right:
            mid = (left + right) // 2
            comp = self._compare_mountains(self.mountains[mid], mountain)
            if comp < 0:
                left = mid + 1
            elif comp > 0:
                right = mid - 1
            else:
                return mid
        return left

    def cur_position(self, mountain: Mountain) -> int:
        index = self._binary_search(mountain)
        if index != len(self.mountains) and self.mountains[index].name == mountain.name:
            return index  
        raise KeyError("Mountain not found")


    def add_mountains(self, mountains: list[Mountain]) -> None:
        for mountain in mountains:
            index = self._binary_search(mountain)
            self.mountains.insert(index, mountain)
