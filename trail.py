from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack
# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) ->  TrailStore:
        """Removes the branch, should just leave the remaining following trail.

           Complexity : Best case will be equal to the worst case which would amount to
                        O(1)
        
        """
        self.path_bottom = Trail(None) # Assignment is constant --> O(1)
        self.path_top = Trail(None) # Assignment is constant --> O(1) 
        return self.path_follow.store # Assignment is constant --> O(1)

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """
    def __hash__(self) -> int:
        return hash(TrailSeries)

    mountain: Mountain
    following: Trail


    def remove_mountain(self) -> TrailStore:
        """
        Removes the mountain at the beginning of this series.
        
        Complexity : Best case is equal to worst case which amounts to  
                     O(1).
        """
        if self.following == None: # Assignment is constant --> O(1)
            return None # Returning is constant --> O(1)
        self.new_trail = Trail(self.following) # Assignment is constant --> O(1)
        return self.new_trail.store # Returning is constant --> O(1)


    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        self.new_trail = Trail(TrailSeries(mountain, Trail(TrailSeries(self.mountain,self.following)))) # Assignment is c 
        return self.new_trail.store
        
        

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        self.next_trail = Trail(TrailSplit(Trail(None),Trail(None),Trail(TrailSeries(self.mountain,self.following))))
        return self.next_trail.store


    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        self.new_trail = Trail(TrailSeries(self.mountain,Trail(TrailSeries(mountain,self.following))))
        return self.new_trail.store


    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        
        self.new_trail = Trail(TrailSeries(self.mountain,Trail(TrailSplit(Trail(None),Trail(None),self.following)))) #Might have to change path_follow to self.following
        return self.new_trail.store

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:
    
    store: TrailStore = None

    def __hash__(self) -> int:
        return hash(TrailStore)
    
    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain,Trail(None)))
        
        

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail.

           Complexity : As the linked stack that is being used is a singly linked stack
                        all pushing and popping methods will be of constant time as it 
                        only involves pushing to the node of the stack. Due to this the best case
                        is equal to the worst case which is O(1 + add_mountains) == O(1) 
        
        """
        return Trail(TrailSplit(Trail(None),Trail(None),Trail(None)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        self.frontier = LinkedStack(1000) #Assignment is constant --> O(1)
        self.frontier.push(self) # Pushing is constant in singly linked stack --> O(1)
        while not self.frontier.is_empty(): # Checks is constant --> O(1)
            self.trail_to_explore = self.frontier.pop() # Popping is constant in a singly linked stack --> O(1)
            while self.trail_to_explore.store != None: #Checking is constant --> O(1)
                if isinstance(self.trail_to_explore.store,TrailSplit): #Checking is instant --> O(1)
                    is_top = personality.select_branch(self.trail_to_explore.store.path_top,self.trail_to_explore.store.path_bottom) #Assignment is constant --> O(1)
                    if is_top: # Constant --> O(1)
                        self.frontier.push(self.trail_to_explore.store.path_follow) # Pushing is constant in singly linked stack --> O(1)
                        self.trail_to_explore = self.trail_to_explore.store.path_top #Assignment is constant --> O(1)
                    else: # Constant --> O(1)
                        self.frontier.push(self.trail_to_explore.store.path_follow) # Pushing is constant in singly linked stack --> O(1)
                        self.trail_to_explore = self.trail_to_explore.store.path_bottom #Assignment is constant --> O(1)
                else: # Constant --> O(1)
                    personality.add_mountain(self.trail_to_explore.store.mountain) # O(add_mountain) == O(1)
                    if self.trail_to_explore.store.following.store == None: 
                        if self.frontier.is_empty(): #Checking is instant --> O(1)
                            break  # Constant --> O(1)
                        self.trail_to_explore = self.frontier.pop() # Popping is constant in a singly linked stack --> O(1)
                    else: # Constant --> O(1)
                        self.trail_to_explore = self.trail_to_explore.store.following #Assignment is constant --> O(1)
            

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail.

           Complexity : The best case of this is equal to the worst case. This is because the add function 
                        in a set is always O(n) as the we would first need to iterate through the entire set
                        to check if the element is already added. Due to this in the best case and the worst case 
                        both need to iterate through the list . Due to this, Best case = Worst case = O(n + k) where k 
                        is an integer of real numbers.

        """
        self.frontier = LinkedStack() #Assignment is constant --> O(1)
        self.visited = set() #Assignment is constant --> O(1)
        self.current_path = [] #Assignment is constant --> O(1)
        self.trail_to_explore = self #Assignment is constant --> O(1)
        while self.trail_to_explore.store != None: #Checking is instant --> O(1)
            if isinstance(self.trail_to_explore.store,TrailSplit): # Constant --> O(1)
                if self.trail_to_explore.store.path_top not in self.visited: # Constant --> O(1)
                    self.frontier.push(self.trail_to_explore.store.path_follow) # Pushing is constant in singly linked stack --> O(1)
                    self.trail_to_explore = self.trail_to_explore.store.path_top  #Assignment is constant --> O(1)
                elif self.trail_to_explore.store.path_bottom not in self.visited: # Constant --> O(1)
                    self.frontier.push(self.trail_to_explore.store.path_follow)  # Pushing is constant in singly linked stack --> O(1)
                    self.trail_to_explore = self.trail_to_explore.store.path_bottom #Assignment is constant --> O(1)
                
                else: # Constant --> O(1)
                    self.visited.add(self.trail_to_explore) # Adding is linear time --> O(n)
                    self.trail_to_explore = self #Assignment is constant --> O(1)
                    continue # Constant --> O(1)
            else: # Constant --> O(1)
                if self.trail_to_explore.store not in self.visited: # Constant --> O(1)
                    self.visited.add( self.trail_to_explore.store)
                    self.current_path.append(self.trail_to_explore.store.mountain) # Appending in a list is constant --> O(1)
                if self.trail_to_explore.store.following.store == None: # Constant --> O(1)
                    self.visited.add(self.trail_to_explore)  # Adding is linear time --> O(n)
                    if not self.frontier.is_empty(): # Constant --> O(1)
                        self.trail_to_explore = self.frontier.pop()  # Popping is constant in a singly linked stack --> O(1)
                        if not self.frontier.is_empty() and self.trail_to_explore.store == None: # Constant --> O(1)
                            self.trail_to_explore = self.frontier.pop()  # Popping is constant in a singly linked stack --> O(1)

                    else: # Constant --> O(1)
                        self.trail_to_explore = self #Assignment is constant --> O(1)

                else: # Constant --> O(1)
                    self.trail_to_explore = self.trail_to_explore.store.following #Assignment is constant --> O(1)
        return self.current_path # Returning is constant --> O(1)

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        if k<=0:
            return []
        self.frontier = LinkedStack()
        self.visited = set()
        self.current_path = []
        self.all_paths = []
        self.trail_to_explore = self
        while self.trail_to_explore.store is not None:
            if len(self.current_path) == k and self.frontier.is_empty():
                self.all_paths.append(self.current_path)
                self.current_path = []
            elif len(self.current_path) > k or (len(self.current_path) < k and self.frontier.is_empty() and self.trail_to_explore.store is None):
                self.current_path = []
                self.frontier = LinkedStack() #creating a new stack is better than clearing old one as we save time complexity and python will clear up the objects anyway
                self.trail_to_explore = self
            if isinstance(self.trail_to_explore.store,TrailSplit):
                if self.trail_to_explore.store.path_top not in self.visited:
                    self.frontier.push(self.trail_to_explore.store.path_follow)
                    self.trail_to_explore = self.trail_to_explore.store.path_top
                elif self.trail_to_explore.store.path_bottom not in self.visited:
                    self.frontier.push(self.trail_to_explore.store.path_follow)
                    self.trail_to_explore = self.trail_to_explore.store.path_bottom
                
                else:
                    self.visited.add(self.trail_to_explore)
                    self.trail_to_explore = self
                    self.frontier = LinkedStack()
            else:
                self.current_path.append(self.trail_to_explore.store.mountain)
                if self.trail_to_explore.store.following.store is None:
                    self.visited.add(self.trail_to_explore)
                    if not self.frontier.is_empty():
                        self.trail_to_explore = self.frontier.pop()
                        if not self.frontier.is_empty() and self.trail_to_explore.store is None:
                            self.trail_to_explore = self.frontier.pop()
                    else:
                        self.trail_to_explore = self

                else:
                    self.trail_to_explore = self.trail_to_explore.store.following
        return self.all_paths


