from mountain import Mountain
from data_structures.hash_table import LinearProbeTable

class MountainManager:

    def __init__(self) -> None:
        self.mountain_store = LinearProbeTable()

    def add_mountain(self, mountain: Mountain):
        '''
        Add a mountain to the manager
        '''
        self.mountain_store[mountain.name] = mountain
    def remove_mountain(self, mountain: Mountain):
        '''
        Remove a mountain from the manager
        '''
        self.mountain_store[mountain.name] = None

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''
        edits the mountain
        '''
        self.mountain_store[old.name] = new

    def mountains_with_difficulty(self, diff: int):
        '''
        Return a list of all mountains with this difficulty.
        '''
        self.matching_difficulty = []
        for mountian in self.mountain_store.values():
            if mountian.difficulty_level == diff:
                self.matching_difficulty.append(mountian)

        return self.matching_difficulty


    def group_by_difficulty(self):
        '''
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        '''
        raise NotImplementedError()
