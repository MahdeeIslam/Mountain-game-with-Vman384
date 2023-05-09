from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        self.mountain_store = LinearProbeTable()

    def add_mountain(self, mountain: Mountain)-> None:
        '''
        Add a mountain to the manager

        Complexity : O(1)
        '''
        try: #Constant --> O(1)
            self.mountain_store[mountain.name] = mountain #Assignment is constant --> O(1)
        except: #Constant --> O(1)
            print("Error: could not add mountain to manager, table is full")  #Constant --> O(1)

    def remove_mountain(self, mountain: Mountain)-> None:
        '''
        Remove a mountain from the manager

        Complexity : The best-case time complexity of remove_mountain is O(1) when the Mountain object 
                     to be removed is in the first position of the hash table bucket 
                     (i.e., no other objects have collided in the same bucket).

                     The worst-case time complexity of remove_mountain is O(Nhash(key) + N^2comp(K)), where N is the 
                     size of the hash table, hash(key) is the time complexity of computing the hash function for the 
                     Mountain object's name, and comp(K) is the time complexity of comparing the names of Mountain objects. 
                     This occurs when the Mountain object to be removed is in the middle of a long chain of collided objects 
                     in the same hash table bucket. In this case, the method needs to probe N positions until it finds the 
                     object's name, and each probe takes O(hash(key)) time to compute the hash function and O(comp(K)) time to 
                     compare names.
        
        
        '''
        try: #Constant --> O(1)
            del self.mountain_store[mountain.name] # O(1) or O(N*hash(key) + N^2comp(K))
        except KeyError: #Constant --> O(1)
            print("mountain not in list") #Constant --> O(1)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        '''
        edits the mountain

        Complexity: Best-case time complexity: O(1)
                    The best case occurs when the hash function for the old mountain's name maps 
                    to the same index as the new mountain's name. In this case, the update operation 
                    takes constant time since the hash table lookup and the assignment operation takes constant time.

                    Worst-case time complexity: O(Nhash(key) + N^2comp(K))
                    The worst case occurs when the hash function for the old mountain's name 
                    maps to the same index as a long chain of collided items, and the old mountain is 
                    at the end of the chain. In this case, the method needs to probe N positions until 
                    it finds the old mountain's name, and each probe takes O(hash(key)) time to compute 
                    the hash function and O(comp(K)) time to compare names. Once the old mountain is found, 
                    the update operation takes constant time since the hash table lookup and the assignment
                    operation takes constant time.
        '''
        try: #Constant --> O(1)
            self.mountain_store[old.name] = new #O(1) or O(Nhash(key) + N^2comp(K))
        except KeyError: #Constant --> O(1)
            print("mountain not in list") #Constant --> O(1)

    def mountains_with_difficulty(self, diff: int)-> list[Mountain]:
        '''
        Return a list of all mountains with this difficulty.

        Complexity : Best-case time complexity: O(N)
                    Will always have to check the whole hash table therefore is O(N), 
                    where N is the number of Mountain objects in the hash table.)
                    
                    Worst-case time complexity: O(N)
                    Will always have to check the whole hash table therefore is O(N), 
                    where N is the number of Mountain objects in the hash table.
                            
        '''
        self.matching_difficulty = [] #Assignment is constant --> O(1)
        for mountian in self.mountain_store.array: #Constant --> O(N)
            if mountian == None: #Checking is constant --> O(1)
                pass #Constant --> O(1)
            elif mountian[1].difficulty_level == diff:  #Checking is constant --> O(1)
                self.matching_difficulty.append(mountian[1]) #Appending is constant --> O(1)

        return self.matching_difficulty #Retunring is constant --> O(1)
 

    def group_by_difficulty(self) -> list[list[Mountain]]:
        '''
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.

        Complexity : Best-case time complexity: O(N log N)
                     The best case and worst case are the same as will always have to use merge sort and since it is not
                     incremental it will have to run all over again. N is the number of values.
                     
                     Worst-case time complexity: O(N log N)
                     The worst case occurs when the Mountain objects in the hash table are unsorted, and all Mountain objects 
                     have a unique difficulty level. In this case, the mergesort method takes O(N log N) time to sort the Mountain 
                     objects, and the method needs to traverse the array of sorted Mountain objects once to group them by 
                     difficulty level, which takes O(N) time.
                            
        '''
        self.grouped = [] #Assignment is constant --> O(1)
        self.tmp = self.mountain_store.values() #O(N)
        self.sorted = mergesort(self.tmp) #O(N log N)
        self.current_difficulty_list = [] #Assignment is constant --> O(1)
        for mountain in self.sorted: #O(N)
            if len(self.current_difficulty_list) == 0:  #Checking is constant --> O(1)
                self.current_difficulty = mountain.difficulty_level #Assignment is constant --> O(1)
            if mountain.difficulty_level == self.current_difficulty:
                self.current_difficulty_list.append(mountain)  #Appending is constant --> O(1)
            else:  #Checking is constant --> O(1)
                self.grouped.append(self.current_difficulty_list)  #Appending is constant --> O(1)
                self.current_difficulty_list = [mountain] #Assignment is constant --> O(1)
                self.current_difficulty = mountain.difficulty_level #Assignment is constant --> O(1)
        self.grouped.append(self.current_difficulty_list)  #Appending is constant --> O(1)
        return self.grouped #Retunring is constant --> O(1)



