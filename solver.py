from re import L
from typing import List, Tuple
import numpy as np
from blocks import blocks
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

def draw_map():
    return np.zeros((9,9)) 


def pick_one_block() -> np.array:
    """Returns one random block"""
    block = blocks[np.random.randint(0,len(blocks))]

    # rotate for 0, 90, 180, 270 degrees
    rotations = np.random.randint(0,4) 
    block = np.rot90(block,rotations)

    return block


def pick_multiple_blocks(num: int = 3):
    return tuple(pick_one_block() for i in range(num))


def check_placement(map:List[List[int]], block:np.array):
    """Checks overlaps of two binary arrays"""
    # map with block (locical and) should have all places False (no overlap)
    return not np.any(np.logical_and(map,block))


def place_block(map:List[List[int]]=None, block:List[int]=None ) -> Tuple[List[List[List[int]]],List[Tuple[int,int]]]:
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
            if check_placement(map=map,block=block):
                possible_maps.append(block_mask)
                possible_placements.append((x,y))

    return possible_maps, possible_placements


def one_round(map: List[List[int]]=None, blocks: List[List[List[int]]] = None) -> List[Tuple[int,int]]:
    """Does one round of placing blocks and returns best positions (in order of blocks)"""
    
    intermediate_maps = []
    for block in blocks:
        possible_maps, possible_placements = place_block(map=map, block=block)
        


# Solution
# BFS - limited depth - only 5 steps
# best step = the one which achieved biggest score after 5 steps
if __name__=="__main__":
    map = example_map

    blocks = pick_multiple_blocks()

    print(blocks)

    best_positions = one_round(map=map,blocks=blocks)

    print(best_positions)


