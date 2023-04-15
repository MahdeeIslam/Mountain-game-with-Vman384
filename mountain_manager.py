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
        self.mountain_store.__delitem__(mountain.name)

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
        self.grouped = []
        self.temp_store = self.mountain_store.values()
        for index in range(len(self.temp_store)):
            if self.temp_store[index] == None:
                pass
            else:
                self.current_difficulty_list = [self.temp_store[index]]
                self.current_difficulty = self.temp_store[index].difficulty_level
                self.temp_store[index] = None
                for index_to_compare in range(len(self.temp_store)):
                    if self.temp_store[index_to_compare] == None:
                        pass
                    elif self.temp_store[index_to_compare].difficulty_level == self.current_difficulty:
                        self.current_difficulty_list.append(self.temp_store[index_to_compare])
                        self.temp_store[index_to_compare] = None
                if len(self.grouped) == 0:
                    self.grouped.append(self.current_difficulty_list)
                else:
                    for i in range(len(self.grouped)):
                        if self.grouped[i][0].difficulty_level > self.current_difficulty:
                            self.temp = self.grouped[i]
                            self.grouped[i] = self.current_difficulty_list
                            self.current_difficulty_list = self.temp
                            self.current_difficulty = self.current_difficulty_list[0].difficulty_level
                    if self.grouped[-1] != self.current_difficulty_list:    
                        self.grouped.append(self.current_difficulty_list)
        return self.grouped


