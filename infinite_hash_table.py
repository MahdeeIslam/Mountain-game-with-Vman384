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
        """
        index = self.hash(key)
        entry = self.table[index]

        if isinstance(entry, InfiniteHashTable):
            return entry[key]

        if entry is not None and entry[0] == key:
            return entry[1]

        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            self.table[index] = (key, value)
            self.size += 1
        elif isinstance(entry, InfiniteHashTable):
            old_size = len(entry)
            entry[key] = value
            self.size += len(entry) - old_size
        else:
            if entry[0] == key:
                self.table[index] = (key, value)
            else:
                new_table = self._create_subtable()
                new_table[entry[0]] = entry[1]
                new_table[key] = value
                self.table[index] = new_table
                self.size += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            raise KeyError(key)

        if isinstance(entry, InfiniteHashTable):
            old_size = len(entry)
            del entry[key]

            if len(entry) == 1:
                for e in entry.table:
                    if e is not None:
                        self.table[index] = e
                        break

            self.size -= old_size - len(entry)

        elif entry[0] == key:
            self.table[index] = None
            self.size -= 1
        else:
            raise KeyError(key)

    def __len__(self):
        return self.size

    
    def _create_subtable(self) -> InfiniteHashTable:
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
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            raise KeyError(key)

        if isinstance(entry, InfiniteHashTable):
            location = [index]
            location.extend(entry.get_location(key))
            return location
        elif entry[0] == key:
            return [index]
        else:
            raise KeyError(key)

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
