from __future__ import annotations

from mountain import Mountain

from algorithms.binary_search import binary_search
from algorithms.mergesort import mergesort,merge


class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = [] 
      

    def cur_position(self, mountain: Mountain) -> int:
        """
        Complexity: Best case equal to worst case
                    

                    The best-case and worst-case complexities for 
                    the cur_position function are the same because the 
                    function's behavior does not depend on the input 
                    values' specific properties. The binary search algorithm
                    always takes O(log N) steps to find an element or its proper 
                    insertion point, regardless of the input data. Therefore, 
                    the best-case and worst-case complexities for the cur_position function are both O(log N),
                    where N is the total number of mountains included so far (the length of self.mountains).
        
        """

        index =  binary_search(self.mountains, mountain) #O(log(N))
        if self.mountains[index] != mountain:
            raise KeyError
        return index

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        
        Complexity : Best-case: 
                    The best case occurs when each new mountain is inserted at the end of the 
                    list, so no shifting of elements is needed. In this case, the complexity would 
                    be O(M * (1 + log N)) = O(M * log N).
                    
                    Worst-case: The worst case occurs when each new mountain is inserted at the beginning of 
                    the list, causing all the elements in the list to be shifted. In this case, 
                    the complexity would be O(M * (1 + log N + N)) = O(M * (N + log N)).
                    

        """   
        input_sorted = mergesort(mountains)
        self.mountains = merge(input_sorted,self.mountains)