import SLL
import itertools
import random
import time


"""
Problem 1: Write a function which creates a list of all possible Toads and Frogs positions of size n.
"""

def all_combos(n: int) -> list[str]:
    return [",".join(c) for c in itertools.product("TF_", repeat=n)]


"""
Problem 2:

Write a function which creates a list of all possible Toads and Frogs positions of size n which
exactly contain a given number of Toads t and a given number of Frogs f.
"""


# A class for understanding that multiple occurences of F or T are the same for permutations

class unique_element:
    def __init__(self, value, occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    e_set=set(elements)
    list_unique = [unique_element(i,elements.count(i)) for i in e_set]
    u=len(elements)
    return perm_unique_helper(list_unique,[0]*u,u-1)

def perm_unique_helper(list_unique, result_list, d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in list_unique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for j in  perm_unique_helper(list_unique, result_list, d-1):
                    yield j
                i.occurrences+=1

# function to find said permutations
def all_combos_with_given_values(n: int, t: int, f: int):

    board = []

    # add all the stuff to the list
    for _ in range(t):
        board.append('T')

    for _ in range(n - t - f):
        board.append('_')

    for _ in range(f):
        board.append('F')

    # find permutations
        
    return [",".join(c) for c in perm_unique(board)]


"""
Problem 3:

For each of the two functions from Problem 1 and Problem 2, build a table which shows for each n, 
the size of the list of positions, and the number of seconds it took to generate the list. The table 
should start at n = 3 and continue until n is big enough that either it takes 30 minutes to run or your 
computer doesn't have enough memory to build the list of positions.
"""

# first for function 1

def test_all_combos():

    dataset = []

    for i in range(3, 19):

        start = time.time()
        all_combos(i)
        finish = time.time()

        dataset.append([finish-start, i])

    return dataset

# dataset = test_all_combos()

'''
print('This is the test for function 1')
for i in range (len(dataset)):
    print(f'Time for game of size {dataset[i][1]}: {dataset[i][0]:.4f} Seconds')


This is the test for function 1
Time for game of size 3: 0.0000 Seconds
Time for game of size 4: 0.0000 Seconds
Time for game of size 5: 0.0000 Seconds
Time for game of size 6: 0.0001 Seconds
Time for game of size 7: 0.0003 Seconds
Time for game of size 8: 0.0013 Seconds
Time for game of size 9: 0.0037 Seconds
Time for game of size 10: 0.0121 Seconds
Time for game of size 11: 0.0606 Seconds
Time for game of size 12: 0.1086 Seconds
Time for game of size 13: 0.3447 Seconds
Time for game of size 14: 1.1732 Seconds
Time for game of size 15: 3.7058 Seconds
Time for game of size 16: 11.6038 Seconds
Time for game of size 17: 36.6015 Seconds
Time for game of size 18: 136.1437 Seconds

** I tried many times to get it to run longer than this but it crashed every time
'''

# test for function 2

def test_all_combos_with_give_values():

    dataset = []

    for i in range(3, 22):

        start = time.time()
        all_combos_with_given_values(i, round(i/3), round(i/3))
        finish = time.time()

        dataset.append([finish-start, i])

    return dataset

dataset = test_all_combos_with_give_values()


print('This is the test for function 2')
for i in range (len(dataset)):
    print(f'Time for game of size {dataset[i][1]}: {dataset[i][0]:.4f} Seconds')
'''
This is the test for function 2
Time for game of size 3: 0.0000 Seconds
Time for game of size 4: 0.0000 Seconds
Time for game of size 5: 0.0000 Seconds
Time for game of size 6: 0.0001 Seconds
Time for game of size 7: 0.0003 Seconds
Time for game of size 8: 0.0009 Seconds
Time for game of size 9: 0.0025 Seconds
Time for game of size 10: 0.0070 Seconds
Time for game of size 11: 0.0188 Seconds
Time for game of size 12: 0.0868 Seconds
Time for game of size 13: 0.1561 Seconds
Time for game of size 14: 0.4176 Seconds
Time for game of size 15: 1.3059 Seconds
Time for game of size 16: 3.5688 Seconds
Time for game of size 17: 10.5294 Seconds
Time for game of size 18: 32.0111 Seconds
Time for game of size 19: 88.8040 Seconds
Time for game of size 20: 260.2243 Seconds
Time for game of size 21: 835.2847 Seconds
'''



'''
Problem 4:

Write a function which performs breadth first search from a given Toads and Frogs position of size n. 
The function does not need to determine which player wins. It only needs to visit each of the nodes in the 
game tree in breadth first order. The function should return the number of total nodes visited.
'''

# stack and queue class

class Stack:
    def __init__(self):
        self.the_stack = SLL.SinglyLinkedList()
        self.size = 0

    #top of the stack is at the beginning(head)
    #of the list
    def push(self, v):
        self.the_stack.add_first(v)
        self.size += 1

    def pop(self):
        self.size -= 1
        return self.the_stack.remove_first()

    def top(self):
        return self.the_stack.get(0)

    def size(self):
        return self.the_stack.size()

    def is_empty(self):
        return self.size == 0

    def __str__(self):
        return "top:" + str(self.the_stack)

class Queue:
    def __init__(self):
        self.the_queue = SLL.SinglyLinkedList()
        self.size = 0

    def enqueue(self, v):
        self.the_queue.add_last(v)
        self.size += 1

    def dequeue(self):
        self.size -= 1
        return self.the_queue.remove_first()

    def first(self):
        return self.the_queue.head.value
    
    def is_empty(self):
        return self.size == 0

# has left/right options function from daily 2 + 3
def has_left_options(gameboard: str):

    board = gameboard.split(",")

    for i in range (len(board) - 1):
        if board[i] == 'T':
            if board[i + 1] == '_':
                return True
            elif board[i + 1] == 'F' and i + 2 < len(board):
                if board[i + 2] == '_':
                    return True
    return False

def has_right_option(gameboard: str):
    board = gameboard.split(",")

    for i in range (len(board)-1, 1, -1):
        if board[i] == 'F':
            if board[i - 1] == '_':
                return True
            elif board[i - 1] == 'T' and i - 2 >= 0:
                if board[i - 2] == '_':
                    return True
    return False


# has left/right options function from daily 2 + 3
def get_left_options(gameboard: str):

    board = gameboard.split(",")

    # a list of boards
    possible_moves = []

    for i in range (len(board)-1):
        if board[i] == 'T':
            if board[i + 1] == '_':
                # make a new gameboard here with the new moves, a child, and add it to a list of options
                child = board.copy()
                child[i] = '_'
                child[i + 1] = 'T'
                possible_moves.append(",".join(child))

                # old function material
                # possible_moves.append([position, 'move to the next empty space'])
            elif board[i + 1] == 'F' and i + 2 < len(board):
                if board[i + 2] == '_':

                    # make a new gameboard here with the new moves, a child, and add it to a list of options
                    child = board.copy()
                    child[i] = '_'
                    child[i + 2] = 'T'
                    possible_moves.append(",".join(child))
                    
                    # old function material
                    # possible_moves.append([position, 'jump over a frog to empty an space'])
    
    return possible_moves

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

            elif board[i - 1] == 'T' and i - 2 >= 0:
                if board[i - 2] == '_':
                    
                    child = board.copy()
                    child[i] = '_'
                    child[i - 2] = 'F'
                    possible_moves.append(",".join(child))

                    # old stuff again
                    # possible_moves.append([position, 'jump over a toad to empty an space'])
    
    return possible_moves


# searches functions

def start_breadth_first_search(gameboard: str):
    # initialize queue for dfs
    children = Queue()
    visited_states = set()

    visited_states.add(gameboard)

    # check for left options and add to stack
    if has_left_options(gameboard):
        children_list = get_left_options(gameboard)
        for child in children_list:
            children.enqueue(child)

    # check for right options and add to stack
    elif has_right_option(gameboard):
        children_list = get_right_options(gameboard)
        for child in children_list:
            children.enqueue(child)

    return children, visited_states

def breadth_first_search(children: Queue, visited_states: set):

    board_to_check = children.dequeue()

    # make sure we haven't been to this gameboard already
    if board_to_check in visited_states:
        return 0
    visited_states.add(board_to_check)

    # check for left options and add to stack
    if has_left_options(board_to_check):
        children_list = get_left_options(board_to_check)
        for child in children_list:
            children.enqueue(child)

    # check for right options and add to stack
    if has_right_option(board_to_check):
        children_list = get_right_options(board_to_check)
        for child in children_list:
            children.enqueue(child)
    
    return 1

def main_breadth():
    
    # generate random board
    board = ''
    value = ['T','_','F']
    for i in range(10):
        board += (random.choice(value))
        if i < 9:
            board += ',' 

    print(board)

    # start search
    children, visited_states = start_breadth_first_search(board)

    nodes_visited = 1

    # continue search until all nodes have been visited
    while not children.is_empty():
        nodes_visited += breadth_first_search(children, visited_states)

    if nodes_visited is not None:
        print(nodes_visited)


'''
Problem 5:

Write a function which performs depth first search from a given Toads and Frogs position of size n. 
The function does not need to determine which player wins. It only needs to visit each of the nodes in the game 
tree in depth first order. The function should return the number of total nodes visited.
'''

def start_depth_first_search(gameboard: str):
        
    # initialize stack for dfs
    children = Stack()
    visited_states = set()

    visited_states.add(gameboard)

    # check for left options and add to stack
    if has_left_options(gameboard):
        children_list = get_left_options(gameboard)
        for child in children_list:
            children.push(child)

    # check for right options and add to stack
    elif has_right_option(gameboard):
        children_list = get_right_options(gameboard)
        for child in children_list:
            children.push(child)

    return children, visited_states

def depth_first_search(children: Stack, visited_states: set):
        
    board_to_check = children.pop()

    # make sure we haven't been to this gameboard already
    if board_to_check in visited_states:
        return 0
    visited_states.add(board_to_check)

    # check for left options and add to stack
    if has_left_options(board_to_check):
        children_list = get_left_options(board_to_check)
        for child in children_list:
            children.push(child)

    # check for right options and add to stack
    if has_right_option(board_to_check):
        children_list = get_right_options(board_to_check)
        for child in children_list:
            children.push(child)
    
    return 1

def main_depth():
    
    # generate random board
    board = ''
    value = ['T','_','F']
    for i in range(10):
        board += (random.choice(value))
        if i < 9:
            board += ',' 

    print(board)

    # start search
    children, visited_states = start_depth_first_search(board)

    nodes_visited = 1

    # continue search until all nodes have been visited
    while not children.is_empty():
        nodes_visited += depth_first_search(children, visited_states)

    if nodes_visited is not None:
        print(nodes_visited)


if __name__ == "__main__":
    # main_depth()
    # main_breadth()
    pass