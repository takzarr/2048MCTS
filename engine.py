import random
from copy import deepcopy
import math

# GAME ENGINE CODE BELOW

# number of rows and cols of 2048 grid
rows, cols = 4, 4
# actions of 2048 game
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

#create an instance of the grid with two tiles
def new_grid():
    # creates a list of lists. The list contains 'rows' lists,
    # where each list contains 'cols' values, with the value 0
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    # add a value 2 or 4 to a empty tile
    new_tiles(grid)
    # add a value 2 or 4 to a empty tile
    new_tiles(grid)
    return grid

def new_tiles(grid):
    # get random value between 0 (inclusive) and 1 (exclusive)
    chance = random.random()
    # add value 2 to a empty tile if chance is less than 0.9,
    # and, otherwise, add value 4 to a empty tile.
    if chance < 0.9:
        spawn_tiles(grid, 2)
    else: 
        spawn_tiles(grid, 4)

#Check for empty tiles and place value if not empty
def spawn_tiles(grid, value):
    # creates a list of tuples. Each tuple contains the row (r) index
    # and the column (c) of the grid tile position, for tiles that 
    # contain the value 0
    empty = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    if not empty:
        return
    r,c = random.choice(empty)
    grid[r][c] = value

# prints the grid
def print_grid(grid):
    for r in grid:
        for c in r:
            print(f"{c}", end='')
        print("\n", end='')

#STEPS
# shift row
# combine
# shift row again

def right(grid):
    g = deepcopy(grid)
    total_gain = 0
    moved = False

    # for every row
    for r in range(rows):
        # give me the current row list
        original = g[r][:]
        # move non-zero values to the end of list
        shift_row_right(g[r])
        # combines tiles
        total_gain += combine_row_right(g[r])
        # move non-zero values to the end of list
        shift_row_right(g[r])
        # set moved to true if one row's tiles changes value
        if g[r] != original:
            moved = True
    return g, total_gain, moved

#Shift non zero elements to the right
def shift_row_right(row):
    # create a new list that contains all
    # non-zero values from row list.
    new_row = [x for x in row if x != 0]
    # create a new list that appends all zero values
    # from the row list before the list of non-zero values
    new_row = [0] * (len(row) - len(new_row)) + new_row
    row[:] = new_row #modify in place

#Combine row_right
def combine_row_right(row):
    score_gain = 0
    # for row indexes 3 to 1
    for i in range(3, 0, -1):
        # if tile i is non-zero and tile i is equal to tile i-1
        if row[i] != 0 and row[i] == row[i-1]:
            # multiply tile value by 2
            row[i] *= 2
            # add tile value to score 
            score_gain += row[i]
            # set tile i-1 to 0
            row[i-1] = 0
    return score_gain

def left(grid):
    g = deepcopy(grid)
    total_gain = 0
    moved = False

    # for every row
    for r in range(rows):
        # give me the current row list
        original = g[r][:]
        # move non-zero values to beginning of list
        shift_row_left(g[r])
        # combines tiles
        total_gain += combine_row_left(g[r])
        # move non-zero values to beginning of list
        shift_row_left(g[r])
        # set moved to true if one row's tiles changes value
        if g[r] != original:
            moved = True
    return g, total_gain, moved

#Shift non zero elements to the left
def shift_row_left(row):
    # create a new list that contains all
    # non-zero values from row list.
    new_row = [x for x in row if x != 0]
    # append all zero values from the row list after
    # the list of non-zero values
    new_row += [0] * (len(row) - len(new_row))
    row[:] = new_row #modify in place

def combine_row_left(row):
    score_gain = 0
    # for row indexes 0 to 3
    for i in range(3):
        # if tile i is non-zero and tile i is equal to tile i+1
        if row[i] != 0 and row[i] == row[i+1]:
            # multiply tile value by 2
            row[i] *= 2
            # add tile value to score 
            score_gain += row[i]
            # set tile i+1 to 0
            row[i+1] = 0
    return score_gain

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def up(grid):
    # tranpose the grid so that columns become rows
    # and rows become columns
    transposed = transpose(grid)
    # do left action on tranpose grid
    move_board, total_gain, moved = left(transposed)
    # tranpose the tranpose grid to get original grid
    new_grid = transpose(move_board)
    return new_grid, total_gain, moved

def down(grid):
    # tranpose the grid so that columns become rows
    # and rows become columns
    transposed = transpose(grid)
    # do right action on tranpose grid
    move_board, total_gain, moved = right(transposed)
    # tranpose the tranpose grid to get original grid
    new_grid = transpose(move_board)
    return new_grid, total_gain, moved

#apply the correct action to the grid and return the new grid, score gain, and whether any tile moved.
def apply_action(grid, action):
    if action == "LEFT":
        new_grid_, score_gain, moved = left(grid)
    elif action == "RIGHT":
        new_grid_, score_gain, moved = right(grid)
    elif action == "UP":
        new_grid_, score_gain, moved = up(grid)
    elif action == "DOWN":
        new_grid_, score_gain, moved = down(grid)
    else:
        raise ValueError(f"Unknown action: {action}")
    # spawn a new random tile if grid tiles moved
    if moved:
        new_tiles(new_grid_)  # spawn a new random tile
    return new_grid_, score_gain, moved

#get list of valid actions
def get_valid_actions(grid):
    valid = []
    for action in ACTIONS:
        new_grid, _, moved = apply_action(deepcopy(grid), action)
        if moved:
            valid.append(action)
    return valid

#get max tile value from grid
def max_tile(grid):
    return max(max(row) for row in grid)    

#check for number of valid actions or max tile equal to 2048
def gameover(grid):
    if len(get_valid_actions(grid)) == 0:
        return True
    elif max_tile(grid) == 2048:
        return True
    else:
        return False
