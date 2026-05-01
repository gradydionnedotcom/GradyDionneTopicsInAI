#Toads and Frogs Game

import DLL
import random

"""
Problem 1:

Write a function called has_right_options which takes a string as a parameter. 
The string represents a position in Toads and Frogs. You can assume that the 
string contains only the characters, 'T', 'F', or a blank space. The function 
should then produce True if there is at least one valid move from the given 
position for the Right player. The function should produce False otherwise.
"""

def has_right_option(gameboard: str):
    moves_list = DLL.DoublyLinkedList()
    board = gameboard.split(",")

    for i in range (len(board)-1, 1, -1):
        if board[i] == 'F':
            if board[i - 1] == '_':
                return True
            elif board[i - 1] == 'F' and board[i - 2] is not None:
                if board[i - 2] == '_':
                    return True
    return False

'''
Problem 2:

Write a function called get_right_options which takes a string as a parameter. The string 
represents a position in Toads and Frogs. You can assume that the string contains only 
the characters, 'T', 'F', or a blank space. The function should then produce a list of 
all possible options for the Right player from the given position.
'''

def get_right_options(gameboard: str):

    board = gameboard.split(",")

    possible_moves = []

    for i in range (len(board)-1, 1, -1):
        if board[i] == 'F':
            if board[i - 1] == '_':

                child = board.copy()
                child[i] = '_'
                child[i - 1] = 'F'
                possible_moves.append(",".join(child))

                # old stuff
                # possible_moves.append([position, 'move to the next empty space'])

            elif board[i - 1] == 'T' and board[i - 2] is not None:
                if board[i - 2] == '_':
                    
                    child = board.copy()
                    child[i] = '_'
                    child[i - 2] = 'T'
                    possible_moves.append(",".join(child))

                    # old stuff again
                    # possible_moves.append([position, 'jump over a toad to empty an space'])
    
    return possible_moves

'''
Problem 3

Test Cases for has options
generate a random toads and frogs board, print the board, and return true/false if options exist
'''

def has_right_option_test():

    for i in range(3):
        moves = ''
        value = ['T','_','F']
        for j in range(random.randint(7, 15)):
            moves += (random.choice(value))
            moves += ','
        
        test_case = has_right_option(moves)

        print(f"Gameboard: {moves} | Has right option(s): {test_case}")

    return

moves = has_right_option_test()
print(moves)

'''
Problem 4

Test Cases for get options
generate a random toads and frogs board, print the board, and show options
'''

def get_right_option_test():

    for i in range(3):
        moves = ''
        value = ['T','_','F']
        for i in range(random.randint(7, 15)):
            moves += (random.choice(value))
            moves += ','
        
        test_case = get_right_options(moves)

        print(f"Gameoard: {moves}")
        if test_case:
            for option in test_case:
                print(f"  {option}")
        else:
            print( "There are no possible moves")

    return

test = get_right_option_test()