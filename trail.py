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
        """Removes the branch, should just leave the remaining following trail."""
        self.path_bottom = Trail(None)
        self.path_top = Trail(None)
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail


    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        if self.following == None:
            return None
        self.new_trail = Trail(self.following)
        return self.new_trail.store


    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        self.new_trail = Trail(TrailSeries(mountain, Trail(TrailSeries(self.mountain,self.following))))
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
        
        self.new_trail = Trail(TrailSeries(self.mountain,Trail(TrailSplit(Trail(None),Trail(None),Trail(None))))) #Might have to change path_follow to self.following
        return self.new_trail.store

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:
    
    store: TrailStore = None


    
    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain,Trail(None)))
        
        

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None),Trail(None),Trail(None)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        self.frontier = LinkedStack(1000)
        self.frontier.push(self)
        while not self.frontier.is_empty():
            self.trail_to_explore = self.frontier.pop()
            while self.trail_to_explore.store != None:
                if isinstance(self.trail_to_explore.store,TrailSplit):
                    is_top = personality.select_branch(self.trail_to_explore.store.path_top,self.trail_to_explore.store.path_bottom)
                    if is_top:
                        self.frontier.push(self.trail_to_explore.store.path_follow)
                        self.trail_to_explore = self.trail_to_explore.store.path_top
                    else:
                        self.frontier.push(self.trail_to_explore.store.path_follow)
                        self.trail_to_explore = self.trail_to_explore.store.path_bottom
                else:
                    personality.add_mountain(self.trail_to_explore.store.mountain)
                    if self.trail_to_explore.store.following.store == None:
                        if self.frontier.is_empty():
                            break    
                        self.trail_to_explore = self.frontier.pop()
                    else:
                        self.trail_to_explore = self.trail_to_explore.store.following 
            

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
