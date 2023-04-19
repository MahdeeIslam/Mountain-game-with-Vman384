from __future__ import annotations

from typing import Generic, TypeVar, Iterator,Tuple
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')








class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31
    
    MAX_LOAD_FACTOR = 0.5

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        self.primary_table = LinearProbeTable(sizes=sizes)
        self.internal_sizes = internal_sizes if internal_sizes is not None else self.TABLE_SIZES
        self._table = [[None for _ in range(10)] for _ in range(10)]
        self.top_level_table_size = self.TABLE_SIZES[0]
        self.internal_table_sizes = [self.internal_sizes[i % len(self.internal_sizes)] for i in range(self.primary_table.table_size)]
        self._load_factor = 0  
        self._num_entries = 0
        if sizes is None:
            sizes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
        if internal_sizes is None:
            internal_sizes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
        elif isinstance(internal_sizes, list):
            internal_sizes = internal_sizes[0]  # Extract the first element from the list
        self.internal_table_sizes = [self.internal_sizes[i % len(self.internal_sizes)] for i in range(self.primary_table.table_size)]

        
    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.
        :complexity: O(len(key))
        """
        if isinstance(key, int):
            value = key
        else:
            value = 0
            a = 31415
            for char in key:
                value = (ord(char) + a * value) % self.primary_table.table_size
                a = a * self.HASH_BASE % (self.primary_table.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.
        :complexity: O(len(key))
        """

        if isinstance(key, int):
            value = key
        else:
            value = 0
            a = 31415
            for char in key:
                value = (ord(char) + a * value) % sub_table.table_size
                a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    
    

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.
        
        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        
        :raises FullError: When a table is full and cannot be inserted.
        """
        hashed_key1 = self.hash1(str(key1))
        sub_table = self.primary_table[hashed_key1]

        # If the sub-table is not created yet, create a new one.
        if sub_table is None:
            if is_insert:
                sub_table = LinearProbeTable(sizes=self.internal_table_sizes)
                self.primary_table[str(hashed_key1)] = sub_table
            else:
                raise KeyError(f"Key pair ({key1}, {key2}) not found in the table")

        hashed_key2 = self.hash2(key2, sub_table)  # Pass the sub_table parameter here

        if is_insert:
            index = sub_table.insert(key2, None)
        else:
            try:
                index = sub_table.index(hashed_key2)
            except KeyError:
                raise KeyError(f"Key pair ({key1}, {key2}) not found in the table")

        return (hashed_key1, index)
       

        
    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
           Returns an iterator of all top-level keys in hash table
        key = k:
           Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is not None:
            sub_table = self.primary_table[str(self.hash1(key))]
            if isinstance(sub_table, LinearProbeTable):
                yield from sub_table.keys()
            else:
                yield key
        else:
            for row in self.primary_table.array:
                if row is not None and row[0] is not None and row[1] is not None:
                    yield row[0]
                    

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            return list(self.iter_keys())

        try:
            primary_table_item = self.primary_table[key]
        except KeyError:
            return []

        if isinstance(primary_table_item, LinearProbeTable):
            internal_table = primary_table_item
            return list(internal_table.keys())
        else:
            return []


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
        Returns an iterator of all values in hash table
        key = k:
        Returns an iterator of all values in the bottom-hash-table for k.

        """
        
        if key is not None:
            sub_table = self.primary_table[str(self.hash1(key))]
            if isinstance(sub_table, LinearProbeTable):
                yield from sub_table.values()
            else:
                yield sub_table
        else:
            for primary_key, value in self:
                yield value
      
         

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key is None:
            all_values = []
            for primary_key in self.primary_table.keys():
                internal_table = self.primary_table[primary_key]
                all_values.extend(internal_table.values())
            return all_values

        try:
            primary_table_item = self.primary_table[key]
        except KeyError:
            return []

        if isinstance(primary_table_item, LinearProbeTable):
            internal_table = primary_table_item
            return list(internal_table.values())
        else:
            return []
    
    
    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        if isinstance(key, tuple) and len(key) == 2:
            position = self._linear_probe(key[0], key[1], False)
        else:
            raise KeyError("Invalid key format")

        if position:
            sub_table = self.primary_table[position[0]]  # Fix this line
            return sub_table[position[1]][1]
        else:
            raise KeyError(key)

    



    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        primary_key, secondary_key = key

        try:
            internal_table = self.primary_table[str(primary_key)]
        except KeyError:
            # Primary key is not present in hash table, create new internal table
            internal_table = LinearProbeTable(sizes=self.internal_sizes)
            self.primary_table[primary_key] = internal_table

        internal_table[secondary_key] = data
        
           
    
    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        if not isinstance(key, tuple):
            key = (key,)

        primary_key, secondary_key = key

        try:
            primary_position, secondary_position = self._linear_probe(primary_key, secondary_key, False)
        except KeyError:
            raise KeyError(f"Key pair {key} not found")

        try:
            primary_table_item = self.primary_table[primary_key]
        except KeyError:
            raise KeyError(f"Key pair ({primary_key}, {secondary_key}) not found")

        if isinstance(primary_table_item, LinearProbeTable):
            internal_table = primary_table_item
            del internal_table[secondary_key]

            if len(internal_table) == 0:
                del self.primary_table[primary_key]

        else:
            raise KeyError(f"Key pair ({primary_key}, {secondary_key}) not found")

        if len(internal_table) == 0:
            del self.primary_table[self.hash1(primary_key)]

        self._load_factor -= 1 / self._num_entries if self._num_entries != 0 else 0
        if self._load_factor < self.MIN_LOAD_FACTOR and self._num_entries > self.MIN_CAPACITY:
            self._shrink_table()
            
        

        
    
    def delete_top_level_key(self, key: K1) -> None:
        """
        Deletes all entries associated with the top-level key.

        :raises KeyError: when the key doesn't exist.
        """
        index1, _ = self._linear_probe(key, None, False)

        if index1 is None:
            raise KeyError("Top-level key not found in the table")

        self.num_keys -= self.num_keys_subtables[index1]
        self.num_keys_subtables[index1] = 0
        self.array[index1] = None        


    def _rehash(self,is_top_level:bool,index:int) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_primary_table = self.primary_table
        old_internal_sizes = self.internal_table_sizes

        # Compute the new size of the top-level table
        if is_top_level:
            new_top_level_table_size = self.TABLE_SIZES[self.TABLE_SIZES.index(self.top_level_table_size) + 1]
        else:
            new_top_level_table_size = self.top_level_table_size

        # Create a new primary table with the new top-level table size
        self.primary_table = LinearProbeTable(sizes=[new_top_level_table_size])

        # Create new internal table sizes list if we're rehashing a sub-table
        if not is_top_level:
            self.internal_table_sizes = [old_internal_sizes[index]] * new_top_level_table_size

        # Reinsert all the elements into the new table
        for key1 in old_primary_table.keys():
            sub_table = old_primary_table[key1]
            if sub_table is not None:
                for index in range(len(sub_table._table)):
                    entry = sub_table._table[index]
                    if entry is not None and entry != sub_table._TOMBSTONE:
                        key2, value = entry
                        self[key1, key2] = value

        # Update the top-level table size and internal table sizes list
        self.top_level_table_size = new_top_level_table_size
        if not is_top_level:
            self.internal_table_sizes[index] = self.TABLE_SIZES[0]


        
    
    def table_size(self,is_top_level:bool,index:int) -> int:
        """
        Return the current size of the table (different from the length)
        """
        if index is None:
            return self.primary_table.table_size
        else:
            return self.internal_table_sizes[index]

    
    
    def __iter__(self) -> Iterator[tuple[K1, K2]]:
        """
        Iterate through the keys of the table.

        :return: An iterator over the keys.
        """
        for key1 in self.primary_table.keys():
            sub_table = self.primary_table[key1]
            if sub_table is not None:
                for key2 in sub_table.keys():
                    value = sub_table[key2]  # Retrieve the value from the sub_table
                    yield (key1, key2)


    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self._num_entries

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        items = [f"{k}: {v}" for k, v in self]
        return "{" + ", ".join(items) + "}"



    