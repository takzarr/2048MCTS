import random
from copy import deepcopy
import math

# GAME ENGINE CODE BELOW

rows, cols = 4, 4
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#grid = [[0 for _ in range(cols)] for _ in range(rows)]
#grid[1] = [2,2,0,2]
# grid[0][0] = 2
# grid[1][0] = 2
# grid[2][0] = 2
# grid[3][0] = 2


#create an instance of the grid with two tiles
def new_grid():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    new_tiles(grid)
    new_tiles(grid)
    return grid

def new_tiles(grid):
    chance = random.random()
    if chance < 0.9:
        spawn_tiles(grid, 2)
    else: 
        spawn_tiles(grid, 4)
'''
##check gameover
grid[0][0] = 2
grid[0][1] = 4
grid[0][2] = 2
grid[0][3] = 4

grid[1][0] = 4
grid[1][1] = 2
grid[1][2] = 4
grid[1][3] = 2

grid[2][0] = 2
grid[2][1] = 4
grid[2][2] = 2
grid[2][3] = 4

grid[3][0] = 4
grid[3][1] = 2
grid[3][2] = 4
grid[3][3] = 2
'''

#Check for empty tiles and place valie if not empty
def spawn_tiles(grid, value):
    empty = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    if not empty:
        return
    r,c = random.choice(empty)
    grid[r][c] = value
    '''
    while True:
        num1 = random.randint(0,3)
        num2 = random.randint(0,3)
        if not grid[num1][num2]:
            grid[num1][num2] = value
            break
    '''

def print_grid(grid):
    for i in grid:
        print(i)
    print("\n\n")



#STEPS
# shift row
# combine
# shift row again

def right(grid):
    g = deepcopy(grid)
    total_gain = 0
    moved = False

    for r in range(rows):
        original = g[r][:]
        shift_row_right(g[r])
        total_gain += combine_row_right(g[r])
        shift_row_right(g[r])
        if g[r] != original:
            moved = True
    return g, total_gain, moved
    '''
    for i in range(4):
        shift_row_right(grid[i])
        combine_row_right(grid[i])
        shift_row_right(grid[i])
    '''
#Shift non zero elements to the right
def shift_row_right(row):
    new_row = [x for x in row if x != 0]
    new_row = [0] * (len(row) - len(new_row)) + new_row
    row[:] = new_row #modify in place
    '''
    for i in range(3):
        for j in range(3):
            if not row[j + 1]:
                row[j+1] = row[j]
                row[j] = 0
    '''

#Combine row_right
def combine_row_right(row):
    score_gain = 0
    for i in range(3, 0, -1):
        if row[i] != 0 and row[i] == row[i-1]:
            #row[i] += row[i-1]
            row[i] *= 2
            score_gain += row[i]
            row[i-1] = 0
    return score_gain

def left(grid):
    g = deepcopy(grid)
    total_gain = 0
    moved = False

    for r in range(rows):
        original = g[r][:]
        shift_row_left(g[r])
        total_gain += combine_row_left(g[r])
        shift_row_left(g[r])
        if g[r] != original:
            moved = True
    return g, total_gain, moved

    '''
    for i in range(4):
        shift_row_left(grid[i])
        combine_row_left(grid[i])
        shift_row_left(grid[i])
    '''

#Shift non zero elements to the left
def shift_row_left(row):
    new_row = [x for x in row if x != 0]
    new_row += [0] * (len(row) - len(new_row))
    row[:] = new_row #modify in place
    '''
    for i in range(3):
        for j in range(3):
            if not row[j]:
                row[j] = row[j + 1]
                row[j + 1] = 0
    '''
def combine_row_left(row):
    score_gain = 0
    for i in range(3):
        if row[i] != 0 and row[i] == row[i+1]:
            #row[i] += row[i+1]
            row[i] *= 2
            score_gain += row[i]
            row[i+1] = 0
    return score_gain

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def up(grid):
    transposed = transpose(grid)
    move_board, total_gain, moved = left(transposed)
    new_grid = transpose(move_board)
    return new_grid, total_gain, moved
    '''
    for i in range(4):
        shift_col_up(i)
        combine_col_up(i)
        shift_col_up(i)
    '''

'''
def shift_col_up(col):
    for i in range(3):
        for row in range(3):
            if not grid[row][col]:
                grid[row][col] = grid[row+1][col]
                grid[row+1][col] = 0

def combine_col_up(col):
    for row in range(3):
        if grid[row][col] == grid[row+1][col]:
            grid[row][col] += grid[row+1][col]
            grid[row+1][col] = 0
'''

def down(grid):
    transposed = transpose(grid)
    move_board, total_gain, moved = right(transposed)
    new_grid = transpose(move_board)
    return new_grid, total_gain, moved

'''
def shift_col_down(col):
    for i in range(3):
        for row in range(3,0,-1):
            if not grid[row][col]:
                grid[row][col] = grid[row-1][col]
                grid[row-1][col] = 0
def combine_col_down(col):
    for row in range(3,0,-1):
        if grid[row][col] == grid[row-1][col]:
            grid[row][col] += grid[row-1][col]
            grid[row-1][col] = 0
    
def gameover():

    if not check_4d(1,1) and not check_4d(1,2) and not check_4d(2,1) and not check_4d(2,2):
        if grid[0][0] != grid[1][0] and grid[0][0] != grid[0][1] and \
        grid[3][0] != grid[2][0] and grid[3][0] != grid[3][1] and \
        grid[0][3] != grid[0][2] and grid[0][3] != grid[1][3] and \
        grid[3][3] != grid[3][2] and grid[3][3] != grid[2][3]:
            print("Gameover")
def check_4d(row,col):
    if grid[row][col] != grid[row+1][col] and \
    grid[row][col] != grid[row-1][col] and \
    grid[row][col] != grid[row][col+1] and \
    grid[row][col] != grid[row][col-1]:
        return False
    
'''
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

#check for number of valid actions nonemeans gameover
def gameover(grid):
    return len(get_valid_actions(grid)) == 0

def max_tile(grid):
    return max(max(row) for row in grid)    


def main():
    # #Starting tiles
    # spawn_tiles(2); spawn_tiles(2); print_grid()

    # down(); print_grid()
    # #new_tiles(); print_grid()
    # up(); print_grid()
    # #new_tiles(); print_grid()
    #gameover()
    pass




if __name__ == "__main__":
    main()



            


