import numpy as np

blocks = [
    #dot
    np.array([[1]]),
    # L 
    np.array([[0, 1],
    [1, 1]]),
    #square
    np.array([[1, 1],
    [1, 1]]),
    # simple T
    np.array([[1, 0],
    [1, 1],
    [1, 0]]),
    # plus
    np.array([[0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]]),
    #diagonal line
    np.array([[0, 0, 1],
    [0, 1, 0],
    [1, 0, 0]]),
    #letter T
    np.array([[1, 1, 1],
    [0, 1, 0],
    [0, 1, 0]]),
    #letter C
    np.array([[1, 1],
    [1, 0],
    [1, 1]]),
    # pipe
    np.array([[1, 1],
    [1, 0],
    [1, 0]]),
    # Z
    np.array([[0, 1],
    [1, 1],
    [1, 0]]),
    # Z flipped
    np.array([[1, 0],
    [1, 1],
    [0, 1]]),
    # short diagonal
    np.array([[0, 1],
    [1, 0]]),
    # big L
    np.array([[1, 1, 1],
    [1, 0, 0],
    [1, 0, 0]]),
    # 4 line
    np.array([[1],
    [1],
    [1],
    [1]]),
    # 5 line
    np.array([[1],
    [1],
    [1],
    [1],
    [1]]),
    # 3 line
    np.array([[1],
    [1],
    [1]]),
    # 2 line
    np.array([[1],
    [1]]),
]


combinations = { 
    'vertical_line' : np.array([[1],[1],[1],[1],[1],[1],[1],[1],[1]]),
    'horizontal_line' : np.array([[1,1,1,1,1,1,1,1,1]]),
    'full_square' : np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]]) 
    }