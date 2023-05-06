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
        self.external_size_index = sizes if sizes is not None else self.TABLE_SIZES # Assignment is constant --> O(1)
        self.max_outer_index = len(self.external_size_index) # Assignment is constant --> O(1)

        self.outer_index = 0 # Assignment is constant --> O(1)
        self.primary_table: ArrayR(tuple[K1, LinearProbeTable]) = ArrayR(self.external_size_index[self.outer_index]) # Assignment is constant --> O(1)
        self.internal_sizes = internal_sizes if internal_sizes is not None else self.TABLE_SIZES # Assignment is constant --> O(1)
        self.top_level_table_size = self.external_size_index[0] # Assignment is constant --> O(1)

        if internal_sizes is not None:
            self.internal_table_sizes = internal_sizes # Assignment is constant --> O(1)
        else:
            self.internal_table_sizes = LinearProbeTable.TABLE_SIZES # Assignment is constant --> O(1)

        self._num_entries = 0 # Assignment is constant --> O(1)

       
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

        Complexity : Best case will be equal to O(len(key1)). This is because if the function
                     finds an empty position in the primary table in the first iteraton meaning 
                     the loop over the primary table occurs only once. The worst case is equal to
                     O(len(key1)) + self.table_size * len(key2). This is because in the worst case,
                     the function must loop over all elements in the primary table which has a size of 
                     the table size. In each iteration the function might need to call the internal linear
                     probe function with key2 , having a complexity of O(len(key2)). Therefore the worst case
                     is O(len(key1)) + self.table_size * len(key2).
        """

        position = self.hash1(key1) % self.table_size  # complexity is O(len(key1))
        for _ in self.primary_table: # Constant --> O(1)
            if self.primary_table[position] is None: # Constant --> O(1)
                if is_insert: # Constant --> O(1)
                    internal_table = LinearProbeTable(self.internal_table_sizes) #Assignment in constant --> O(1)
                    self.primary_table[position] = (key1, internal_table) #Assignment in constant --> O(1)
                    internal_table.hash = lambda k: self.hash2(k, internal_table) #Assignment in constant --> O(1)

                    if key2 is not None:  # Constant --> O(1)
                        position_for_internal_table = self.hash2(key2, self.primary_table[position][1]) #Assignment in constant --> O(1)
                        return (position, position_for_internal_table) # Returning is constant --> O(1)
                    else: # Constant --> O(1)
                        return (position, -1) # Returning is constant --> O(1)
                else: # Constant --> O(1)
                    raise KeyError(key1) # Rasing doesn't have a complexity
            elif self.primary_table[position][0] == key1: # Constant --> O(1)
                if key2 is not None: # Constant --> O(1)
                    if is_insert: # Constant --> O(1)
                        internal_insert = self.primary_table[position][1]._linear_probe(key2, True) # best case = O(len(key2)) , worst case = O(len(key2) + N * comp(K))
                        return (position, internal_insert)
                    else: # Constant --> O(1)
                        insert_index = self.primary_table[position][1]._linear_probe(key2, False)
                        return (position, insert_index) # Returning is constant --> O(1)
                else: # Constant --> O(1)
                    return (position, -1) # Returning is constant --> O(1)
            else: # Constant --> O(1)
                position = (position + 1) % self.table_size # Assignment is constant --> O(1)

        if is_insert: # Constant --> O(1)
            raise FullError("Table is full")  # Rasing doesn't have a complexity
        else: # Constant --> O(1)
            raise KeyError(key1)  # Rasing doesn't have a complexity



       
    def _index_calculator(self, key: K1) -> int:
        """
        
        Complexity : best case equal worst case == O(1)
        
        """ 
        return hash(key) % len(self.primary_table) # Returning is constant --> O(1)

    

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
           Returns an iterator of all top-level keys in hash table
        key = k:
           Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity : The Best case is when key is None. This is because the function iterates
                     over the primary table with size of the table size and yields the top-level keys,
                     in this case the complexity of the function is O(self.table_size). The worst case
                     is when The function first calls the _linear_probe method with a worst-case complexity 
                     of O(len(key)) + self.table_size * len(key2). Then, it iterates over the keys in the 
                     internal hash table. Assuming that the internal hash table has M elements, the complexity 
                     of this part will be O(M). Therefore, the overall complexity in this case will be 
                     O(len(key)) + self.table_size * len(key2) + K, where K is an element of the real numbers

        """
      

        if key is None: # Checks are constant --> O(1)
            for i in range(len(self.primary_table)): # Constant --> O(1)
                if self.primary_table[i] is not None:  # Checks are constant --> O(1)
                    yield self.primary_table[i][0] # Yielding is constant --> O(1)
        else:  # Checks are constant --> O(1)
            outer,outer2 = self._linear_probe(key,None,False) # O(linear_probe) , refer to linear probe function complexity
            for i in self.primary_table[outer][1].keys():  # O(keys) , refer to keys complexity 
                yield i # Yielding is constant --> O(1)

                    

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity : 
                    If key is None:
                    Best case: There are no top-level keys in the table, so the 
                    function doesn't have to iterate through any elements. The 
                    complexity in this case is O(1).
                    Worst case: The function has to iterate through all top-level keys in the table. 
                    The complexity of self.iter_keys(key) in this case will be O(N), where N is the 
                    number of top-level keys. Since you're appending each key to the keys_result list, 
                    the complexity of this loop will also be O(N).     

                    If key is not None:
                    Best case: There are no bottom-level keys for the specified top-level key, so the 
                    function doesn't have to iterate through any elements. The complexity in this case is O(1).
                    Worst case: The function has to iterate through all bottom-level keys for the specified top-level key. 
                    The complexity of self.iter_keys(key) in this case depends on the number of keys in the bottom-level hash table. 
                    If M is the number of keys in the bottom-level hash table, the complexity will be O(M). Since you're appending 
                    each key to the keys_result list, the complexity of this loop will also be O(M).               
        """
        

        keys_result = [] # Assignment is constant --> O(1)
        for i in self.iter_keys(key): # Refer to complexity analysis
            keys_result.append(i) #Appending in constant -- O(1)
        return keys_result # Returning is constant --> O(1)


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
        Returns an iterator of all values in hash table
        key = k:
        Returns an iterator of all values in the bottom-hash-table for k.
        
        Complexity :Best case:
                    If key is None: The best case occurs when the primary table is empty or has a 
                    small number of top-level keys with very few values in their respective bottom-level 
                    hash tables. In this case, the complexity is close to O(1).
                    If key is not None: The best case happens when the specified top-level key has a small 
                    number of values or no values in its associated bottom-level hash table. In this case, 
                    the complexity is close to O(1).
                    
                    Worst case:
                    If key is None: The worst case occurs when there are many top-level keys in the primary table 
                    and each key has a large number of values in their associated bottom-level hash tables. In this case, 
                    the complexity is O(N * M) where N is the number of top-level keys and M is the maximum number of values 
                    in any bottom-level hash table.
                    If key is not None: The worst case happens when the specified top-level key has a large number of values 
                    in its associated bottom-level hash table. In this case, the complexity is O(M), where M is the number of values 
                    in the bottom-level hash table for the specified key.
                            
        
        """
        
        
        if key is None: #Checking is constant --> O(1)
            for i in range(len(self.primary_table)): #Constant --> O(1)
                if self.primary_table[i] is not None: #Checking is constant --> O(1)
                    for i in self.primary_table[i][1].values():  #Constant --> O(1)
                        yield i  # Yielding is constant --> O(1)
        else:
            outer,outer2 = self._linear_probe(key,None,False) # O(_linear_probe) , refer to linear probe complexity analysis
            for i in self.primary_table[outer][1].values():  #Constant --> O(1)
                yield i  # Yielding is constant --> O(1)
      
         

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity : 
                    Best case:

                    If key is None, there are no elements in the primary table, so the function will not 
                    enter the loop, resulting in a complexity of O(1).
                    If key is provided and there are no elements in the internal table, the function will not enter 
                    the loop, resulting in a complexity of O(1).
                    
                    Worst case:

                    If key is None, and all positions in the primary table are occupied, the function will iterate through 
                    all elements in the primary table and all elements in each of the internal tables. The complexity will 
                    be O(P + P * M), where P is the size of the primary table and M is the maximum size of the internal tables.
                    If key is provided, and the internal table corresponding to that key has all its positions occupied, the function will iterate through all elements in the internal table. The complexity will be O(M), where M is the size of the internal table.


        """
        values_result = [] # Assignment is constant --> O(1)
        for i in self.iter_values(key): # O(iter_keys) , refer to iter_keys complexity analysis
            values_result.append(i) #Appending is constant --> O(1)
        return values_result # Returning is constant --> O(1)
    
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

        Complexity : Best case:

                    The _linear_probe function finds the key pair in the first iteration of its loop. The best case 
                    complexity of _linear_probe is O(len(key[0])).Accessing the value from the primary table using the 
                    returned indices takes constant time O(1). So, the best case complexity is O(len(key[0])).

                    Worst case:

                    The _linear_probe function has to loop through all elements in the primary table and perform the linear
                     probing for each key2 in the internal tables. The worst case complexity of
                      _linear_probe is O(len(key[0]) + self.table_size * len(key[1])).
                    Accessing the value from the primary table using the returned indices takes constant time O(1).
                        
       
       
        """
        indices = self._linear_probe(key[0], key[1], False) #Assignment is constant -> O(1)
        return self.primary_table[indices[0]][1][key[1]] # Returning is constant --> O(1)

    



    def __setitem__(self, key: tuple[K1, K2], data: V , during_rehash: bool = False) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity: Best-case complexity:

                    In the best case, the _linear_probe function finds an empty position in the primary table in the first iteration,
                     so the best case for _linear_probe is O(len(key[0])). The _rehash function will not be called since the table is not 
                     over its load factor. The loop for counting non-empty elements will still be executed, with a complexity of O(self.table_size). 
                     Thus, the best-case complexity is: O(len(key[0]) + self.table_size)

                    Worst-case complexity:

                    The worst-case complexity for _linear_probe is O(len(key[0]) + self.table_size * len(key[1])). In the worst case,
                     the _rehash function is called, with a complexity of O(N * hash(K) + N^2 * comp(K)). The loop for counting 
                     non-empty elements will still be executed, with a complexity of O(self.table_size). So, the 
                     worst-case complexity is: O(len(key[0]) + self.table_size * len(key[1]) + self.table_size + N * hash(K) + N^2 * comp(K))

                    note that the worst-case complexity will rarely be encountered since the _rehash function is called only 
                    when the primary table's load factor exceeds 0.5.





        """
        
        primary_key,secondary_key = self._linear_probe(key[0],key[1],True) # Assignment is constant --> O(1)

        try: #Constant --> O(1)
            self.primary_table[primary_key][1][key[1]] #Checking is consant -- O(1)
        except KeyError: #Constant --> O(1)
            self._num_entries+=1 # Incrementing is constant --> O(1)
        
        self.primary_table[primary_key][1][key[1]] = data #Assignment is constant --> O(1)

        amount_key1 = 0 #Assignment is constant --> O(1)
        for keys in self.primary_table: #Constant --> O(1)
            if keys is not None: #Constant --> O(1)
                amount_key1+=1 # Incrementing is constant --> O(1)
        
        if amount_key1 > self.table_size / 2: #Checking is consant -- O(1)
            self._rehash() # O(rehash) , refer to rehash complexity analysis


        


        
           
    
    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity: Best-case complexity:

                    In the best case, the _linear_probe function finds the position in the primary table in the first iteration, 
                    so the best case for _linear_probe is O(len(key[0])). The condition len(self.primary_table[p1][1]) > 1 is True, 
                    so the item is deleted with no reinsertion process, which has a constant complexity. Thus, 
                    the best-case complexity is: O(len(key[0]))

                    Worst-case complexity:

                    In the worst case, the _linear_probe function has a complexity of O(len(key[0]) + self.table_size * len(key[1])). 
                    The condition len(self.primary_table[p1][1]) > 1 is False, so the item is deleted, and the reinsertion process happens. 
                    In the worst case, every entry in the primary table needs to be reinserted, which would involve calling the __setitem__ function 
                    with a complexity of O(len(key[0]) + self.table_size * len(key[1])). Since there are at most self.table_size entries, the total 
                    complexity of reinsertion would be O(self.table_size * (len(key[0]) + self.table_size * len(key[1]))). 
                    So, the worst-case complexity is: O(len(key[0]) + self.table_size * len(key[1]) + self.table_size * (len(key[0]) + self.table_size * len(key[1])))




        """
    
        p1, p2 = self._linear_probe(key[0], key[1], False) #Assignment is constant --> O(1)

        if len(self.primary_table[p1][1]) > 1: #Constant --> O(1)
            del self.primary_table[p1][1][key[1]] # O(1) or O(N) depending on where it is being deleted
            self._num_entries -= 1 # Decrementing is constant --> O(1)

        else: #Constant --> O(1)
            self.primary_table[p1] = None  #Assignment is constant --> O(1)
            self._num_entries -= 1 # Decrementing is constant --> O(1)
            p1 = (p1 + 1) % self.table_size #Assignment is constant --> O(1)

            while self.primary_table[p1] is not None: #Checking is constant --> O(1)
                key1 = self.primary_table[p1][0] #Assignment is constant --> O(1)
                key2_list = list(self.primary_table[p1][1].keys()) #Assignment is constant --> O(1)
                values = list(self.primary_table[p1][1].values()) #Assignment is constant --> O(1)
                self.primary_table[p1] = None #Assignment is constant --> O(1)

                for i in range(len(key2_list)): #Constant --> O(1)
                    self[key1, key2_list[i]] = values[i]  ##Assignment is constant --> O(1)

                p1 = (p1 + 1) % self.table_size #Assignment is constant --> O(1)


        


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)


        My complexity analysis :Best case:

                                Initializing a new primary table and other assignments: O(1)
                                Looping through all the elements in the old primary table: O(N), where N is the number of 
                                entries in the table
                                Hashing the keys while re-inserting the key-value pairs without probing: O(N * hash(K))
                                Re-inserting key-value pairs: O(N)
                                So, the best case complexity is O(N * hash(K))

                                Worst case:

                                Initializing a new primary table and other assignments: O(1)
                                Looping through all the elements in the old primary table: O(N), where N is the number of entries in the table
                                Hashing the keys while re-inserting the key-value pairs with lots of probing: O(N * hash(K) + N^2 * comp(K))
                                Re-inserting key-value pairs: O(N)
                                So, the worst case complexity is O(N * hash(K) + N^2 * comp(K))
        
        Therefore, complexities match
        
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

        Complexity : Constant 
        """
        return len(self.primary_table)

    
    
    def __iter__(self) -> Iterator[tuple[K1, K2]]:
        """
        Iterate through the keys of the table.

        :return: An iterator over the keys.

        Complexity: The complexity of this function depends on the number of elements in the primary table (outer hash table) and the number of elements in each inner hash table.

                    Let m be the number of elements in the primary table and let n_i be the number of elements in the i-th inner 
                    hash table. The function iterates over each element in the primary table and then iterates over each element 
                    in the inner hash table.The complexity can be represented as: O(m * (n_1 + n_2 + ... + n_m))

                    In the worst case, all elements are evenly distributed across all inner hash tables, resulting in a complexity 
                    of: O(m * n)

                    where n is the average number of elements per inner hash table.
                    In the best case, there is only one non-empty inner hash table, and the complexity would be: O(m + n) 
                    where n is the number of elements in that single inner hash table.




        """
        for primary_table_entry in self.primary_table:
            if primary_table_entry is not None:
                key1, inner_table = primary_table_entry
                for key2 in inner_table.keys():
                    yield key1, inner_table[key2]


    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Complexity : constant
        """
        return self._num_entries 

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        items = [f"{k}: {v}" for k, v in self]
        return "{" + ", ".join(items) + "}"



