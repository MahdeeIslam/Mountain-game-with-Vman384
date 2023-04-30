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
        sets are hash tables in python so checking if in is O(1)
        '''
        self.grouped = []
        self.checked = set()
        self.temp_store = self.mountain_store.array
        for index in range(len(self.temp_store)):
            if self.temp_store[index] == None or index in self.checked:
                pass
            else:
                self.current_difficulty_list = [self.temp_store[index][1]]
                self.current_difficulty = self.temp_store[index][1].difficulty_level
                self.checked.add(index)
                for index_to_compare in range(len(self.temp_store)):
                    if self.temp_store[index_to_compare] == None:
                        pass
                    elif self.temp_store[index_to_compare][1].difficulty_level == self.current_difficulty:
                        self.current_difficulty_list.append(self.temp_store[index_to_compare][1])
                        self.checked.add(index_to_compare)
                self.grouped.append(self.current_difficulty_list)
        return mergesort(self.grouped)


