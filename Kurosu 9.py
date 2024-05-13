# Kurosu
# Idea from Daily Mail
# https://www.dailymail.co.uk/news/article-5774235/Prepare-Kurosu-ed-latest-brilliant-puzzle-Japan.html
#
# Python version by Roland Waddilove
# Copy it, use it, do whatever you want with it.
# It's just an exercise on my way to learning Python.
# Auto-adjusts for board size, 4x4, 6x6, 8x8, 10x10.
# I'll add a graphical display in a future version.

import os

# Here are some example boards. Un-comment the one to use
board = [
    '...O..',
    '...OO.',
    '......',
    '..O..X',
    '....XX',
    '..X...'
]

# Harder 6 x 6
# board = [
#     'X..XX.',
#     '.....X',
#     '..X...',
#     'X....X',
#     'X...X.',
#     '.O....'
# ]

# Even harder 6 x 6
# board = [
#     '..O.OO',
#     '...X.X',
#     'O.....',
#     '.....X',
#     'O..X..',
#     '......'
# ]

# Hardest 8 x 8
# board = [
#     '..XX..O.',
#     '.......O',
#     '.X......',
#     '....O..X',
#     '...X.O..',
#     '...XX...',
#     'X.O.....',
#     '........'
# ]

# Small 4 x 4
# board = [
#     'O.X.',
#     '..XO',
#     'XO..',
#     '..O.'
# ]

def show_board():
    """Display the current state of the board."""
    print("\n  ", end="")
    for n in range(board_width):    #print the numbers across the top
        print(f"{n} ", end="")

    for i in range(board_height):
        print(f"\n{i} ", end="")
        for j in range(board_width):
            if board[i][j] == '.': print(". ", end="")  #gives the option to change printed character
            if board[i][j] == 'X': print("X ", end="")  #will probably do a graphical pygame version
            if board[i][j] == 'O': print("O ", end="")
    print()

def enter_turn():
    """Input where to store X and O."""
    xo = "z"
    while not xo in "XO" or len(xo)>1:      #input X or O
        xo = input("Enter X or O? ").upper()
    pos = "z"
    while not pos.isnumeric() or len(pos)!=2:    #input position of cell
        pos = input("Row/col (eg. 23)? ")
        row, col = int(pos[0]), int(pos[1])
        if row >= board_height or col >= board_width:
            print("Not a valid position!")
            pos = "z"
    if board[row][col] != ".":    #if not empty
        print("Not a valid position!")
        return
    board[row][col] = xo        #place X or O
    if valid_pos():   #if not valid board (too many Xs or Os)
        move_history.append([row,col])
    else:
        board[row][col] = "."   #undo
        print("Not a valid position!")

def valid_pos():
    """Check if the current board is valid - no rules broken."""
    valid = True
    #check columns
    for col in range(board_width):
        x = o = 0
        for row in range(board_height):
            if board[row][col] == "X": x = x + 1
            if board[row][col] == "O": o = o + 1
        if x>(board_width//2) or o>(board_height//2): valid = False
        for row in range(board_height-2):
            if board[row][col]=='X' and board[row+1][col]=='X' and board[row+2][col]=='X': valid = False
            if board[row][col]=='O' and board[row+1][col]=='O' and board[row+2][col]=='O': valid = False
    #check rows
    for row in range(board_height):
        x = board[row].count('X')
        o = board[row].count('O')
        if x>(board_width//2) or o>(board_height//2): valid = False
        for col in range(board_width-2):
            if board[row][col]=='X' and board[row][col+1]=='X' and board[row][col+2]=='X': valid = False
            if board[row][col]=='O' and board[row][col+1]=='O' and board[row][col+2]=='O': valid = False

    return valid

def solved():
    """if no empty cells and the board is valid."""
    done = True
    for i in range(len(board)):
        if "." in board[i]:
            done = False
    if done: done = valid_pos()
    return done

def solve_it():     #this solves Kurosu
    while len(move_history) > 0:    #undo player moves before starting
        undo_last_move()
    while not solved():             #Repeat until solved.
        solve_kurosu()              #solve 1 cell at a time! 

def solve_kurosu():
    """solve 1 cell at a time! Repeat until solved."""
    if valid_pos():     #if everything ok, find next empty cell
        row = col = 0
        while board[row][col] != ".":
            col = (col + 1) % board_width
            if col == 0: row = row + 1
        stack.append([row,col])     #save cell
        board[row][col] = "X"       #try an X
    else:               #last X/O placed didn't work
        if len(stack) > 0:
            row = stack[-1][0]      #get previous cell looked at
            col = stack[-1][1]
        else:
            row = 0                 #no previous cell if it's the first
            col = 0
        while board[row][col] == "O":
            board[row][col] = "."
            stack.pop()         #step back till cell = X
            row = stack[-1][0]
            col = stack[-1][1]
        board[row][col] = "O"

def undo_last_move():
    if len(move_history) > 0:   #any moves to undo?
        board[move_history[-1][0]][move_history[-1][1]] = '.'   #reset last cell
        move_history.pop()      #remove last played cell


#===================== MAIN =======================
board_width = len(board[0]) #saves typing, easier to read
board_height = len(board)   #saves typing, easier to read
stack = []                  #used with solve_kuroso()
move_history = []           #store player's moves for undo

for i in range(board_width):    #turn board row strings into lists
    x = [i for a,i in enumerate(board[i])] 
    board[i] = x

os.system('cls') if os.name=='nt' else os.system('clear')

print("---------------------")
print("    K U R O S U")
print("---------------------")
print("Complete the puzze by placing Xs and Os.")
print("Maximum 2 adjacent in a row or column.")
print("Half Xs, half Os in each row/column,")
print("eg. 3 Xs and 3 Os in a 6x6 puzzle.")

play = "p"
while not solved() and play!="q":
    show_board()
    play = input("\nEnter: (P)lay, (Q)uit, (S)olve, (U)ndo: ").lower()
    if play == 'u': undo_last_move()
    if play == 'p': enter_turn()
    if play == 's': solve_it()

show_board()
print()
