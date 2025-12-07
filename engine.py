import random

rows, cols = 4, 4
grid = [[0 for _ in range(cols)] for _ in range(rows)]
#grid[1] = [2,2,0,2]
# grid[0][0] = 2
# grid[1][0] = 2
# grid[2][0] = 2
# grid[3][0] = 2

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
def spawn_tiles(value):

    while True:
        num1 = random.randint(0,3)
        num2 = random.randint(0,3)
        if not grid[num1][num2]:
            grid[num1][num2] = value
            break


def print_grid():
    for i in grid:
        print(i)
    print("\n\n")

def new_tiles():
    chance = random.random()
    if chance < 0.9: #spawn 2
        spawn_tiles(2)
    else:
        spawn_tiles(4) 


#STEPS
# shift row
# combine
# shift row again

def right():
    for i in range(4):
        shift_row_right(grid[i])
        combine_row_right(grid[i])
        shift_row_right(grid[i])

def shift_row_right(row):
    for i in range(3):
        for j in range(3):
            if not row[j + 1]:
                row[j+1] = row[j]
                row[j] = 0

def combine_row_right(row):
    for i in range(3, 0, -1):
        if row[i] == row[i-1]:
            row[i] += row[i-1]
            row[i-1] = 0

def left():
    for i in range(4):
        shift_row_left(grid[i])
        combine_row_left(grid[i])
        shift_row_left(grid[i])

def shift_row_left(row):
    for i in range(3):
        for j in range(3):
            if not row[j]:
                row[j] = row[j + 1]
                row[j + 1] = 0

def combine_row_left(row):
    for i in range(3):
        if row[i] == row[i+1]:
            row[i] += row[i+1]
            row[i+1] = 0

def up():
    for i in range(4):
        shift_col_up(i)
        combine_col_up(i)
        shift_col_up(i)

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

def down():
    for i in range(4):
        shift_col_down(i)
        combine_col_down(i)
        shift_col_down(i)
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
    

def main():
    # #Starting tiles
    # spawn_tiles(2); spawn_tiles(2); print_grid()

    # down(); print_grid()
    # #new_tiles(); print_grid()
    # up(); print_grid()
    # #new_tiles(); print_grid()
    gameover()




if __name__ == "__main__":
    main()



            


