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
        self.external_size_index = sizes if sizes is not None else self.TABLE_SIZES
        self.max_outer_index = len(self.external_size_index)

        self.outer_index = 0
        self.primary_table: ArrayR(tuple[K1, LinearProbeTable]) = ArrayR(self.external_size_index[self.outer_index])
        self.internal_sizes = internal_sizes if internal_sizes is not None else self.TABLE_SIZES
        self.top_level_table_size = self.external_size_index[0]

        if internal_sizes is not None:
            self.internal_table_sizes = internal_sizes
        else:
            self.internal_table_sizes = LinearProbeTable.TABLE_SIZES

        self._num_entries = 0

       
    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.
        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.
        :complexity: O(len(key))
        """

    
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

        position = self.hash1(key1) % self.table_size
        for _ in self.primary_table:
            if self.primary_table[position] is None:
                if is_insert:
                    internal_table = LinearProbeTable(self.internal_table_sizes)
                    self.primary_table[position] = (key1, internal_table)
                    internal_table.hash = lambda k: self.hash2(k, internal_table)

                    if key2 is not None:
                        position_for_internal_table = self.hash2(key2, self.primary_table[position][1])
                        return (position, position_for_internal_table)
                    else:
                        return (position, -1)
                else:
                    raise KeyError(key1)
            elif self.primary_table[position][0] == key1:
                if key2 is not None:
                    if is_insert:
                        internal_insert = self.primary_table[position][1]._linear_probe(key2, True)
                        return (position, internal_insert)
                    else:
                        insert_index = self.primary_table[position][1]._linear_probe(key2, False)
                        return (position, insert_index)
                else:
                    return (position, -1)
            else:
                position = (position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full")
        else:
            raise KeyError(key1)



       
    def _index_calculator(self, key: K1) -> int:
        return hash(key) % len(self.primary_table)

    

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
           Returns an iterator of all top-level keys in hash table
        key = k:
           Returns an iterator of all keys in the bottom-hash-table for k.
        """
      

        if key is None:
            for i in range(len(self.primary_table)):
                if self.primary_table[i] is not None:
                    yield self.primary_table[i][0]
        else:
            outer,outer2 = self._linear_probe(key,None,False)
            for i in self.primary_table[outer][1].keys():
                yield i 

                    

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        

        keys_result = []
        for i in self.iter_keys(key):
            keys_result.append(i)
        return keys_result


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
        Returns an iterator of all values in hash table
        key = k:
        Returns an iterator of all values in the bottom-hash-table for k.

        """
        
        
        if key is None:
            for i in range(len(self.primary_table)):
                if self.primary_table[i] is not None:
                    for i in self.primary_table[i][1].values():
                        yield i
        else:
            outer,outer2 = self._linear_probe(key,None,False)
            for i in self.primary_table[outer][1].values():
                yield i 
      
         

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        values_result = []
        for i in self.iter_values(key):
            values_result.append(i)
        return values_result
    
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
        indices = self._linear_probe(key[0], key[1], False)
        return self.primary_table[indices[0]][1][key[1]]

    



    def __setitem__(self, key: tuple[K1, K2], data: V , during_rehash: bool = False) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        
        primary_key,secondary_key = self._linear_probe(key[0],key[1],True)

        try:
            self.primary_table[primary_key][1][key[1]]
        except KeyError:
            self._num_entries+=1
        
        self.primary_table[primary_key][1][key[1]] = data

        amount_key1 = 0
        for keys in self.primary_table:
            if keys is not None:
                amount_key1+=1
        
        if amount_key1 > self.table_size / 2:
            self._rehash()


        


        
           
    
    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
    
        p1, p2 = self._linear_probe(key[0], key[1], False)

        if len(self.primary_table[p1][1]) > 1:
            del self.primary_table[p1][1][key[1]]
            self._num_entries -= 1

        else:
            self.primary_table[p1] = None
            self._num_entries -= 1
            p1 = (p1 + 1) % self.table_size

            while self.primary_table[p1] is not None:
                key1 = self.primary_table[p1][0]
                key2_list = list(self.primary_table[p1][1].keys())
                values = list(self.primary_table[p1][1].values())
                self.primary_table[p1] = None

                for i in range(len(key2_list)):
                    self[key1, key2_list[i]] = values[i]  # Re-insert the entry

                p1 = (p1 + 1) % self.table_size


        


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        
        old_primary_table = self.primary_table
        self.outer_index +=1

        if self.outer_index == self.external_size_index:
            return
        self.primary_table = ArrayR(self.external_size_index[self.outer_index - 1])
        self._num_entries = 0

        for j in old_primary_table:
            if j is not None:
                key1 = j[0]
                key2 = j[1].keys()
                values = j[1].values()
                for k in range(len(key2)):
                    self[key1 , key2[k]] = values[k]

        
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.primary_table)

    
    
    def __iter__(self) -> Iterator[tuple[K1, K2]]:
        """
        Iterate through the keys of the table.

        :return: An iterator over the keys.
        """
        for primary_table_entry in self.primary_table:
            if primary_table_entry is not None:
                key1, inner_table = primary_table_entry
                for key2 in inner_table.keys():
                    yield key1, inner_table[key2]


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



