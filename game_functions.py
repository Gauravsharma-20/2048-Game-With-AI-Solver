import numpy as np

POSSIBLE_MOVES_COUNT = 4
CELL_COUNT = 4
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,4, 4])


#start State
def initialize_game():
    board = np.zeros((NUMBER_OF_SQUARES), dtype = "int")
    #position of Intial two tiles
    initial_twos = np.random.default_rng().choice(NUMBER_OF_SQUARES, 2, replace = False)
    #2-probability(0.8)    4-probability(0.2)
    board[initial_twos] = np.random.default_rng().choice(NEW_TILE_DISTRIBUTION[:], 2, replace=False)
    #Cell x Cell ,Now.
    board = board.reshape((CELL_COUNT, CELL_COUNT))
    return board


# Stacks all the element to the right,to remove the empty 
# space between them to help us merge
def push_board_right(board):
    new = np.zeros((CELL_COUNT, CELL_COUNT), dtype="int")
    done = False
    for row in range(CELL_COUNT):
        count = CELL_COUNT - 1
        for col in range(CELL_COUNT - 1, -1, -1):
            if board[row][col] != 0:
                #count-> current empty
                new[row][count] = board[row][col]
                #ensure move was made {atleast 1 shift}
                if col != count:
                    done = True
                count -= 1
    #new board, if task occured
    return (new, done)


#Merge the elements if they are same
def merge_elements(board):
    score = 0
    done = False
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT - 1, 0, -1): 
            #CELL_COUNT - 1, 0 because first row will be checked by col-1
            if (board[row][col] != 0) and (board[row][col] == board[row][col-1]):
                board[row][col] *= 2
                #whatever the new tile is added to score
                score += board[row][col]
                board[row][col-1] = 0
                #move made
                done = True

    return (board, done, score)


#RIGHT - base template
def move_right(board):
    #stack
    board, has_pushed = push_board_right(board)
    #merge
    board, has_merged, score = merge_elements(board)
    #unstack
    board, _ = push_board_right(board)
    #if no move was performed {check} for Game-Over
    move_made = (has_pushed or has_merged)
    return board, move_made, score


#LEFT
def move_left(board):
    #reverse
    board = np.rot90(board, 2)
    #same operation as that of Right - Stack,Merge,Un-Stack.
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    #Un-reverse
    board = np.rot90(board, -2)
    move_made = has_pushed or has_merged

    return board, move_made, score


#UP
def move_up(board):
    #transpose ---  rot90 does anti-clock rotation
    #-1 takes it in the other direction
    board = np.rot90(board, -1) 
    #same operation as that of Right - Stack,Merge,Un-Stack.
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    #Un-Transpose
    board = np.rot90(board)
    move_made = has_pushed or has_merged

    return board, move_made, score


#DOWN
def move_down(board):
    #transpose ---  rot90 does anti-clock rotation
    board = np.rot90(board)
    #same operation as that of Right - Stack,Merge,Un-Stack.
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    #Un-Transpose
    board = np.rot90(board, -1)
    move_made = has_pushed or has_merged

    return board, move_made, score

#tries all 4 possible moves - 1st AI move }- not using
def fixed_move(board):
    #function names of moves
    move_order = [move_left, move_up, move_down, move_right]
    for func in move_order:
        new_board, move_made, _ = func(board)
        if move_made:
            return new_board, True
    return board, False

#tries all 4 possible moves - for AI traversal \\ at the current node
def random_move(board):
    move_made = False
    move_order = [move_right, move_up, move_down, move_left]
    #making this fast for each node
    length_move_order = len(move_order)
    while((not move_made) and (length_move_order > 0)):
        #move_index = np.random.randint(0, length_move_order)
        move_index = length_move_order - 1
        curr_move = move_order[move_index]
        board, move_made, score  = curr_move(board)
        if move_made:
            return board, True, score
        #pop if not used here
        #move_order.pop(move_index)
        length_move_order -= 1 
    return board, False, score

#Add New Tile
def add_new_tile(board):
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
    #available positions (#use logical not)
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    #random position for spawning
    tile_loc = np.random.randint(0, len(tile_row_options))
    #position will be valid
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return board

#Final Goal
def check_for_win(board):
    return (2048 in board)
