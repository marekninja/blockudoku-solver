from dataclasses import dataclass
from itertools import combinations
from re import L
from typing import List, Tuple
import numpy as np
from blocks import blocks, combinations
# in future rewrite whole solution to bit operations, hopefully will be fast

# 9 x 9 example map, 1 is full, 0 is empty
example_map = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0, 1, 0],
                        [1, 1, 1, 0, 0, 0, 1, 1, 1]])

num_cols = 9
num_rows = 9


@dataclass
class Map:
    """Simple class to store map and steps to achieve it, by placing all picked blocks
    """
    map: np.array(np.array(int))
    steps: List[np.array]


def draw_map():
    return np.zeros((9,9)) 

def random_rotation(block, rot: int = None):
    # rotate for 0, 90, 180, 270 degrees

    rotations = rot if rot is not None else np.random.randint(0,4) 

    return np.rot90(block,rotations)


def pick_one_block() -> np.array:
    """Returns one random block"""
    block = blocks[np.random.randint(0,len(blocks))]

    return random_rotation(block=block)


def pick_multiple_blocks(num: int = 3) -> Tuple[List]:
    """Picks number of blocks at random

    Args:
        num (int, optional): Number of blocks to pick. Defaults to 3. If 0, then returns all blocks

    Returns:
        Tuple[List]: Tuple of picked blocks
    """
    if num == 0:
        return tuple(random_rotation(b) for b in blocks)
        
    return tuple(pick_one_block() for i in range(num))


def check_placement(map:List[List[int]], block:np.array):
    """Checks overlaps of two binary arrays"""
    # map with block (logical and) should have all places False (no overlap)
    return not np.any(np.logical_and(map,block))

def check_combination(map:List[List[int]], block:np.array):
    """Checks whether map has combination of block type"""
    return np.array_equal(np.bitwise_and(map,block),block)

def handle_combinations(map:List[List[int]]=None) -> List[List[int]]:
    """Handles achieved combinations of squares and lines 

    Args:
        map (List[List[int]], optional): Map to check. Defaults to None.

    Returns:
        List[List[int]]: New map - without achieved combinations
    """
    block = combinations['full_square']
    block_size_x = block.shape[1] # num cols of block
    block_size_y = block.shape[0] # num rows of block

    transforms_to_apply = []
    # check full square
    for x in range(0,num_cols - block_size_x+1,block_size_x):
        for y in range(0,num_rows - block_size_y+1,block_size_y):
            block_mask = np.pad(block,[(y, num_rows - block_size_y - y),(x,num_cols - block_size_x - x)],'constant',constant_values=0)
            if check_combination(map,block_mask):
                transforms_to_apply.append(lambda m=map, b = block_mask: np.bitwise_xor(m,b))
            
    # check horizontal lines
    block = combinations['horizontal_line']
    block_size_x = block.shape[1] # num cols of block
    block_size_y = block.shape[0] # num rows of block

    x = 0
    for y in range(0,num_rows - block_size_y+1,block_size_y):
        block_mask = np.pad(block,[(y, num_rows - block_size_y - y),(x,num_cols - block_size_x - x)],'constant',constant_values=0)
        if check_combination(map,block_mask):
            transforms_to_apply.append(lambda m=map, b = block_mask: np.bitwise_xor(m,b))

    # check vertical lines
    block = combinations['vertical_line']
    block_size_x = block.shape[1] # num cols of block
    block_size_y = block.shape[0] # num rows of block

    y = 0
    for x in range(0,num_cols - block_size_x+1,block_size_x):
        block_mask = np.pad(block,[(y, num_rows - block_size_y - y),(x,num_cols - block_size_x - x)],'constant',constant_values=0)
        if check_combination(map,block_mask):
            transforms_to_apply.append(lambda m=map, b = block_mask: np.bitwise_xor(m,b))

    for transformation in transforms_to_apply:
        map = transformation()
        # print("Achieved score: ",map, f"Now has score {map.sum()}")

    return map


# def place_block(map:List[List[int]]=None, block:List[int]=None ) -> Tuple[List[List[List[int]]],List[Tuple[int,int]]]:
def place_block(map:Map=None, block:List[int]=None ) -> Tuple[List[List[List[int]]],List[Tuple[int,int]]]:
    """Places block on map and returns all possible maps and positions (maps, positions"""
    block_size_x = block.shape[1] # num cols of block
    block_size_y = block.shape[0] # num rows of block

    possible_maps = []
    possible_placements = []
    for x in range(num_cols - block_size_x+1):
        for y in range(num_rows - block_size_y+1):
            # padding of block to the size of map
            # padding for both dimensions [], each dimension has tuple (before,after)
            block_mask = np.pad(block,[(y, num_rows - block_size_y - y),(x,num_cols - block_size_x - x)],'constant',constant_values=0)
            # if check_placement(map=map,block=block_mask):
            if check_placement(map=map.map,block=block_mask):
                
                new_map = Map(map=np.bitwise_or(map.map,block_mask),steps=map.steps.copy())
                new_map.steps.append(block_mask)
                possible_maps.append(new_map)
                # possible_maps.append()
                # possible_placements.append(block_mask)
            
    # handle deletion if square/lines detected
    for idx in range(len(possible_maps)):
        # one_map = possible_maps[idx]
        one_map = possible_maps[idx].map
        # print(f"Map {idx} with score {one_map.sum()}")
        # possible_maps[idx] = handle_combinations(one_map)
        possible_maps[idx].map = handle_combinations(one_map)
        
    return possible_maps, possible_placements


def evaluate_greedy(maps: List[List[int]]=None,) -> List[int]:
    """Greedy evaluation function: 
        - lower score = better
        - Each full point +1

        Extensions - support big open spaces and penalise thin or dots 
            Maybe do One round into future?

    Args:
        maps (List[List[int]], optional): Maps to evaluate. Defaults to None.

    Returns:
        List[int]: List of points for each map (sorted by regions)
    """

    # return [ m.sum() for m in maps]
    return [ m.map.sum() for m in maps]


def one_round(map: List[List[int]]=None, blocks: List[List[List[int]]] = None) -> Tuple[List[List[int]],List[Tuple[int,int]]]:
    """Does one round of placing blocks and returns best positions (in order of blocks) and new map

    Args:
        map (List[List[int]], optional): Map to start from. Defaults to None.
        blocks (List[List[List[int]]], optional): Blocks available in this turn. Defaults to None.

    Returns:
        Tuple[List[List[int]],
            List[Tuple[int,int]]
            ]: Tuple of Map and Positions(x,y for each block in order) to which to put the blocks
    """

    intermediate_maps = []
    intermediate_placements = []
    for block in blocks:
        if not len(intermediate_maps):
            intermediate_maps = [Map(map.copy(),[])]

        possible_maps = []
        # possible_placements = []
        for one_map in intermediate_maps:
            possible_maps, possible_placements = place_block(map=one_map, block=block)
            
        intermediate_maps = possible_maps
        intermediate_placements.append(possible_placements)

    # evaluate all generated maps, return the one with lowest score
    # evaluation function = sum of:
    # number of full regions
    value_of_maps = evaluate_greedy(intermediate_maps)

    # intermediate_placements
    combination = zip(value_of_maps, intermediate_maps)
    all = sorted(combination,key=lambda x: x[0])

    # best_map = 
    # best_positions

    return all


def main():
    map = example_map

    picked_blocks = pick_multiple_blocks()

    print(picked_blocks)

    best_positions = one_round(map=map,blocks=picked_blocks)

    print(best_positions[0])

# Solution
# BFS - limited depth - only 5 steps
# best step = the one which achieved biggest score after 5 steps
if __name__=="__main__":
    main()