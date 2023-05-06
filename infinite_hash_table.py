from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.level = 0
        self.table = [None] * self.TABLE_SIZE
        self.size = 0


    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity: Best Case: O(1)
                    When the key is found immediately in the table.
                    
                    Worst Case: O(n)
                    When the key is at the deepest level of nested subtables. Here, n is the number of nested subtables.



        """
        index = self.hash(key) #Assignment is constant --> O(1)
        entry = self.table[index] #Assignment is constant --> O(1)

        if isinstance(entry, InfiniteHashTable): #Checking is constant --> O(1)
            return entry[key] #Returning is constant --> O(1)

        if entry is not None and entry[0] == key: #Checking is constant --> O(1)
            return entry[1] #Returning is constant --> O(1)

        raise KeyError(key) #Raising doesn't have a complexity

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity: Best Case: O(1)
                    In the best case, the key is hashed to an empty index or to an index with a matching key. 
                    In either case, the operation takes constant time.
                    
                    Worst Case: O(n)
                    In the worst case, the key is hashed to an index with a non-matching key or an InfiniteHashTable instance. 
                    In such cases, the function may need to create or update subtables. The worst-case complexity occurs when 
                    there are n nested subtables, resulting in O(n) time complexity.



        """
        index = self.hash(key) #Assignment is constant --> O(1)
        entry = self.table[index] #Assignment is constant --> O(1)

        if entry is None: #Checking is constant --> O(1)
            self.table[index] = (key, value) #Assignment is constant --> O(1)
            self.size += 1 #Incrementing is constant --> O(1)
        elif isinstance(entry, InfiniteHashTable): #Checking is constant --> O(1)
            old_size = len(entry) #Assignment is constant --> O(1)
            entry[key] = value #Assignment is constant --> O(1)
            self.size += len(entry) - old_size #Constant --> O(1)
        else: #Checking is constant --> O(1)
            if entry[0] == key: #Checking is constant --> O(1)
                self.table[index] = (key, value) #Assignment is constant --> O(1)
            else: #Checking is constant --> O(1)
                new_table = self._create_subtable() #Assignment is constant --> O(1)
                new_table[entry[0]] = entry[1] #Assignment is constant --> O(1)
                new_table[key] = value #Assignment is constant --> O(1)
                self.table[index] = new_table #Assignment is constant --> O(1)
                self.size += 1 #Incrementing is constant --> O(1)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity: Best Case: O(1)
                    In the best case, the key is hashed to an index with a matching key, and the key-value pair 
                    is deleted directly in constant time.
                    
                    Worst Case: O(n)
                    In the worst case, the key is hashed to an index containing an InfiniteHashTable instance. 
                    The function then needs to recursively delete the key-value pair from the subtable. 
                    The worst-case complexity occurs when there are n nested subtables, resulting in O(n) time complexity.



        """
        index = self.hash(key) #Assignment is constant --> O(1)
        entry = self.table[index] #Assignment is constant --> O(1)

        if entry is None: #Checking is constant --> O(1)
            raise KeyError(key) #Raising does not have a complexity

        if isinstance(entry, InfiniteHashTable):
            old_size = len(entry) #Assignment is constant --> O(1)
            del entry[key] #Deleting is constant --> O(1)

            if len(entry) == 1: #Checking is constant --> O(1)
                for e in entry.table: #Constant --> O(1)
                    if e is not None: #Checking is constant --> O(1)
                        self.table[index] = e #Assignment is constant --> O(1)
                        break #Constant --> O(1)

            self.size -= old_size - len(entry) #Constant --> O(1)

        elif entry[0] == key: #Checking is constant --> O(1)
            self.table[index] = None  #Assignment is constant --> O(1)
            self.size -= 1 #Decrementig constant --> O(1)
        else: #Checking is constant --> O(1)
            raise KeyError(key) #Raising does not have a complexity

    def __len__(self):
        """
        Complexity: O(1)
        """
        return self.size

    
    def _create_subtable(self) -> InfiniteHashTable:
        """
        Complexity : O(1)

        """
        subtable = InfiniteHashTable()
        subtable.level = self.level + 1
        return subtable
    
    
    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Complexity: Best case complexity: O(1)
                    In the best case scenario, the key is directly found in the first-level hash table, 
                    and there is no need for recursion or traversing further subtables. This would result in 
                    constant time complexity.

                    Worst case complexity: O(L)
                    In the worst case scenario, the key is located deep within nested subtables, and the function 
                    would need to traverse through each level, calling get_location recursively for each level. The maximum 
                    number of levels is represented by L. The worst case complexity would then be linear with respect to the 
                    maximum depth L. 




        """
        index = self.hash(key) #Assignment is constant --> O(1)
        entry = self.table[index] #Assignment is constant --> O(1)

        if entry is None: #Checking is constant --> O(1)
            raise KeyError(key) #Raising doesn't have a complexity

        if isinstance(entry, InfiniteHashTable): #Checking is constant --> O(1)
            location = [index] #Assignment is constant --> O(1)
            location.extend(entry.get_location(key)) # O(L)
            return location #Returning is constant --> O(1)
        elif entry[0] == key: #Checking is constant --> O(1)
            return [index] #Returning is constant --> O(1)
        else: #Checking is constant --> O(1)
            raise KeyError(key) #Raising doesn't have a complexity

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

