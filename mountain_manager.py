from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import mergesort

class MountainManager:

    def __init__(self) -> None:
        self.mountain_store = LinearProbeTable()

    def add_mountain(self, mountain: Mountain):
        '''
        Add a mountain to the manager
        '''
        try:
            self.mountain_store[mountain.name] = mountain
        except:
            print("Error: could not add mountain to manager, table is full")

    def remove_mountain(self, mountain: Mountain):
        '''
        Remove a mountain from the manager
        '''
        try:
            self.mountain_store.__delitem__(mountain.name)
        except KeyError:
            print("mountain not in list")

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''
        edits the mountain
        '''
        try:
            self.mountain_store[old.name] = new
        except KeyError:
            print("mountain not in list")

    def mountains_with_difficulty(self, diff: int):
        '''
        Return a list of all mountains with this difficulty.
        '''
        self.matching_difficulty = []
        for mountian in self.mountain_store.array:
            if mountian == None:
                pass
            elif mountian[1].difficulty_level == diff:
                self.matching_difficulty.append(mountian[1])

        return self.matching_difficulty


    def group_by_difficulty(self):
        '''
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        '''
        self.grouped = []
        self.tmp = self.mountain_store.values() #O(N)
        self.sorted = mergesort(self.tmp) #O(N log N)
        self.current_difficulty_list = []
        for mountain in self.sorted: #O(N)
            if len(self.current_difficulty_list) == 0:
                self.current_difficulty = mountain.difficulty_level
            if mountain.difficulty_level == self.current_difficulty:
                self.current_difficulty_list.append(mountain)
            else:
                self.grouped.append(self.current_difficulty_list)
                self.current_difficulty_list = [mountain]
                self.current_difficulty = mountain.difficulty_level
        self.grouped.append(self.current_difficulty_list)
        return self.grouped



