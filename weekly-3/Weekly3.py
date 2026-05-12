import random
'''
Problem 1: min max searcb
'''


class Board:

    def __init__(self, board: str):
        self.board = board.split(",")

        self.size = len(self.board)

        self.num_frogs = 0
        self.num_toads = 0

        for i in range (len(self.board)):
            if self.board[i] == 'F':
                self.num_frogs += 1
            if self.board[i] == 'T':
                self.num_toads += 1

        self.v = 0

    # get left/right options function from daily 2 + 3
    def has_left_options(self):

        for i in range (len(self.board) - 1):
            if self.board[i] == 'T':
                if self.board[i + 1] == '_':
                    return True
                elif self.board[i + 1] == 'F' and i + 2 < len(self.board):
                    if self.board[i + 2] == '_':
                        return True
        return False

    def has_right_options(self):

        for i in range (len(self.board)-1, 1, -1):
            if self.board[i] == 'F':
                if self.board[i - 1] == '_':
                    return True
                elif self.board[i - 1] == 'T' and i - 2 >= 0:
                    if self.board[i - 2] == '_':
                        return True
        return False

    # has left/right options function from daily 2 + 3
    def get_left_options(self):

        # a list of boards
        possible_moves = []

        for i in range (len(self.board)-1):
            if self.board[i] == 'T':
                if self.board[i + 1] == '_':
                    # make a new gameboard here with the new moves, a child, and add it to a list of options
                    child = self.board.copy()
                    child[i] = '_'
                    child[i + 1] = 'T'
                    possible_moves.append(",".join(child))

                    # old function material
                    # possible_moves.append([position, 'move to the next empty space'])
                elif self.board[i + 1] == 'F' and i + 2 < len(self.board):
                    if self.board[i + 2] == '_':

                        # make a new gameboard here with the new moves, a child, and add it to a list of options
                        child = self.board.copy()
                        child[i] = '_'
                        child[i + 2] = 'T'
                        possible_moves.append(",".join(child))
                        
                        # old function material
                        # possible_moves.append([position, 'jump over a frog to empty an space'])
        
        return possible_moves

    def get_right_options(self):

        possible_moves = []

        for i in range (len(self.board)-1, 1, -1):
            if self.board[i] == 'F':
                if self.board[i - 1] == '_':

                    child = self.board.copy()
                    child[i] = '_'
                    child[i - 1] = 'F'
                    possible_moves.append(",".join(child))

                    # old stuff
                    # possible_moves.append([position, 'move to the next empty space'])

                elif self.board[i - 1] == 'T' and i - 2 >= 0:
                    if self.board[i - 2] == '_':
                        
                        child = self.board.copy()
                        child[i] = '_'
                        child[i - 2] = 'F'
                        possible_moves.append(",".join(child))

                        # old stuff again
                        # possible_moves.append([position, 'jump over a toad to empty an space'])
        
        return possible_moves


    # determine if lead node
    def is_leaf_node(self)->bool:
        if self.has_left_options():
            return False
        if self.has_right_options():
            return False
        return True

    def left_board_value(self, board):
        # some evaluations for how good a board

        value = 0

        # evaluation variables
        left_moves = 0
        right_moves = 0

        # look at every spot
        for i in range (board.size):

            # 2 in a row for toad
            if self.board[i] == 'T' and self.board[i + 1] == 'T':
                value += 2

            # 2 in a row for frog
            if self.board[i] == 'F' and self.board[i - 1] == 'F':
                value -= 2

            # skips vs. one space moves and distance from the end for toads
            if self.board[i] == 'T':
                value += round(i/2)
                if i + 2 < self.size:
                    if self.board[i + 1] == "_":
                        value += round((self.size - i)/2)
                        left_moves += 1
                    elif i + 2 < self.size:
                        if self.board[i + 1] == "F" and self.board[i + 2] == "_":
                            value += board.size - i
                            left_moves += 1
            
            # blocked moves
            if board.size > i + 3:
                if self.board[i] == "T" and self.board[i + 1] == '_' and self.board[i + 2] == 'F' and self.board[i + 3] == "F":
                    value -= 10
            
            if i > 3:
                if self.board[i] == "F" and self.board[i - 1] == '_' and self.board[i - 2] == 'T' and self.board[i - 3] == "T":
                    value += 10

            # face off?
            if self.board[i] == "T" and self.board[i + 1] == "F":
                value += 20

        # number of total moves
        value += (left_moves * 5)
        value -= (right_moves * 5)

        return value
    
    def right_board_value(self, board):
        # some evaluations for how good a board

        value = 0

        # evaluation variables
        left_moves = 0
        right_moves = 0

        # look at every spot
        for i in range (board.size):

            # 2 in a row for toad
            if self.board[i] == 'T' and self.board[i + 1] == 'T':
                value += 2

            # 2 in a row for frog
            if self.board[i] == 'F' and self.board[i - 1] == 'F':
                value -= 2
            
            # skips vs. one space moves and distance from the end for frogs
            if self.board[i] == 'F':
                value -= round((board.size - 1 - i)/2)
                if i > 2:
                    if self.board[i - 1] == "_":
                        value -= i
                        right_moves += 1
                    elif self.board[i - 1] == 'T':
                        if self.board[i - 2] == '_':
                            value -= round(i/2)
                            right_moves += 1
            
            # blocked moves
            if board.size > i + 3:
                if self.board[i] == "T" and self.board[i + 1] == '_' and self.board[i + 2] == 'F' and self.board[i + 3] == "F":
                    value -= 10
            
            if i > 3:
                if self.board[i] == "F" and self.board[i - 1] == '_' and self.board[i - 2] == 'T' and self.board[i - 3] == "T":
                    value += 10

            # face off?
            if self.board[i] == "T" and self.board[i + 1] == "F":
                value -= 20

        # number of total moves
        value += (left_moves * 5)
        value -= (right_moves * 5)

        return value

    # max for min max search
    def max_value(self, best_move, n):
        if self.is_leaf_node():
            return self.v, best_move, n
        
        children = self.get_left_options()

        if not children:
            return self.v, best_move, n

        value = float('-inf')

        for child in children:
            n += 1
            board = Board(child)
            board.v = self.left_board_value(board)
            vnew, best_move, n = board.min_value(best_move, n)
            if vnew > value: 
                value = vnew
                best_move = child
            return value, best_move, n

    # min for min max search
    def min_value(self, best_move, n):
        if self.is_leaf_node():
            return self.v, best_move, n
        
        children = self.get_right_options()

        if not children:
            return self.v, best_move, n
        
        value = float('inf')

        for child in children:
            n += 1
            board = Board(child)
            board.v = self.right_board_value(board)
            vnew, best_move, n = board.max_value(best_move, n)
            if vnew < value: 
                value = vnew
                best_move = child
            return value, best_move, n
        
    '''
    Problem 2: Alpha Beta Pruning
    '''



    # pruning searches
    def max_value_with_pruning(self, a, b, best_move, n):
        if self.is_leaf_node():
            return self.v, best_move, n
        
        children = self.get_left_options()

        if not children:
            return self.v, best_move, n

        value = float('-inf')

        for child in children:
            n += 1
            board = Board(child)
            vnew, best_move, n = board.min_value_with_pruning(a, b, best_move, n)
            if vnew > value: 
                value = vnew
                best_move = child
            if value >= b:
                return value, n
            if vnew > a:
                a = vnew
            return value, best_move, n

    # min for min max search
    def min_value_with_pruning(self, a, b, best_move, n):
        if self.is_leaf_node():
            return self.v, best_move, n
        
        children = self.get_right_options()

        if not children:
            return self.v, best_move, n
        
        value = float('inf')

        for child in children:
            n += 1
            board = Board(child)
            vnew, best_move, n = board.max_value_with_pruning(a, b, best_move, n)
            if vnew < value: 
                value = vnew
                best_move = child
            if value <= a:
                return value, n
            if vnew <= b:
                b = vnew
            return value, best_move, n
        
def test():
    for i in range(5):
        board = ''
        value = ['T','_','F']
        for i in range(random.randint(7, 15)):
            board += (random.choice(value))
            board += ','

        test = Board(board)
        
        test_case, best_move, n = Board.min_value(test, None, 1)

        print(f"Gameoard: {board}\nScore: {test_case}\nNodes Visited: {n}\n Best Move: {best_move}")
        if test_case > 0:
            print('Toad Win, Frogs Moving First\n\n')
        if test_case <= 0:
            print('Frog Win, Frogs Moving First\n\n')
            

    for i in range(5):
        board = ''
        value = ['T','_','F']
        for i in range(random.randint(7, 15)):
            board += (random.choice(value))
            board += ','

        test = Board(board)
        
        test_case, best_move, n = Board.max_value(test, None, 1)

        print(f"Gameoard: {board}\nScore: {test_case}\nNodes Visited: {n}\n Best Move: {best_move}")
        if test_case > 0:
            print('Toad Win, Toads Moving First\n\n')
        if test_case <= 0:
            print('Frog Win, Toads Moving First\n\n')

def ab_test(a, b):
    for i in range(5):
        board = ''
        value = ['T','_','F']
        for i in range(random.randint(7, 15)):
            board += (random.choice(value))
            board += ','

        test = Board(board)
        
        test_case, best_move, n = Board.min_value_with_pruning(test, a, b, None, 1)

        print(f"AB Gameoard: {board}\nScore w/ Pruning: {test_case}\nNodes Visited: {n}\n Best Move: {best_move}")
        if test_case > 0:
            print('Toad Win, Frogs Moving First\n\n')
        if test_case <= 0:
            print('Frog Win, Frogs Moving First\n\n')

    for i in range(5):
        board = ''
        value = ['T','_','F']
        for i in range(random.randint(7, 15)):
            board += (random.choice(value))
            board += ','

        test = Board(board)
        
        test_case, best_move, n = Board.max_value_with_pruning(test, a, b, None, 1)

        print(f"AB Gameoard: {board}\nScore w/ Pruning: {test_case}\nNodes Visited: {n}\n Best Move: {best_move}")
        if test_case > 0:
            print('Toad Win, Toads Moving First\n\n')
        if test_case <= 0:
            print('Frog Win, Toads Moving First\n\n')
    
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

def main():

    print(test())

    a = float("-inf")
    b = float("inf")

    # print(ab_test(a, b))


if __name__ == '__main__':
    main()