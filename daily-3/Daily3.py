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
    for item in gameboard.split(","):
        moves_list.add_last(item)

    current = moves_list.trailer
    while current is not None and current.prev is not None:
        if current.value == 'F':
            if current.prev.value == ' ':
                return True
            elif current.prev.value == 'F' and current.prev.prev is not None:
                if current.prev.prev.value == ' ':
                    return True
        current = current.prev
    return False

'''
Problem 2:

Write a function called get_right_options which takes a string as a parameter. The string 
represents a position in Toads and Frogs. You can assume that the string contains only 
the characters, 'T', 'F', or a blank space. The function should then produce a list of 
all possible options for the Right player from the given position.
'''

def get_right_options(gameboard: str):
    moves_list = DLL.DoublyLinkedList()
    for item in gameboard.split(","):
        moves_list.add_last(item)

    possible_moves = []
    position = moves_list.size + 1

    current = moves_list.trailer
    while current is not None and current.prev is not None:
        if current.value == 'F':
            if current.prev.value == ' ':
                possible_moves.append([position, 'move to the next empty space'])
            elif current.prev.value == 'T' and current.prev.prev is not None:
                if current.prev.prev.value == ' ':
                    possible_moves.append([position, 'jump over a toad to empty an space'])
        current = current.prev
        position -= 1
    
    if possible_moves:
        return [f'Frog in square {pos} can {mov}' for pos, mov in possible_moves]
    
    return 'There are no possible moves for the right player'

'''
Problem 3

Test Cases for has options
generate a random toads and frogs board, print the board, and return true/false if options exist
'''

def has_right_option_test():

    for i in range(3):
        moves = ''
        value = ['T',' ','F']
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
        value = ['T',' ','F']
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