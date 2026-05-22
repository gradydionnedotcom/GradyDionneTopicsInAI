import pygame
import gif_pygame

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

        for i in range (len(self.board)-1, -1, -1):
            if self.board[i] == 'F':
                if self.board[i - 1] == '_':
                    return True
                elif self.board[i - 1] == 'T' and i - 2 >= 0:
                    if self.board[i - 2] == '_':
                        return True
        return False
    
    def valid_move_toad(self, pos):
        if self.board[pos] == "T":
            if self.pos < self.size:
                if self.board[pos + 1] == '_':
                    return True
                if self.pos < self.size - 1:
                    if self.board[pos + 1] == "F" and self.board[pos + 2] == "_":
                        return True
            
        return False

    def valid_move_frog(self, pos):
        if self.board[pos] == "F":
            if self.pos < 1:
                if self.board[pos - 1] == '_':
                    return True
                if self.pos < 2:
                    if self.board[pos - 1] == "F" and self.board[pos - 2] == "_":
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

        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i] == 'F':
                if i - 1 >= 0 and self.board[i - 1] == '_':
                    child = self.board.copy()
                    child[i] = '_'
                    child[i - 1] = 'F'
                    possible_moves.append(",".join(child))

                elif i - 2 >= 0 and self.board[i - 1] == 'T' and self.board[i - 2] == '_':
                    child = self.board.copy()
                    child[i] = '_'
                    child[i - 2] = 'F'
                    possible_moves.append(",".join(child))

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
        for i in range (board.size - 1):

            if board.board[i] == 'T' and board.board[i + 1] == 'T':
                value += 5

            if board.board[i] == 'F' and board.board[i + 1] == 'F':
                value -= 5

            # skips vs. one space moves and distance from the end for toads
            if board.board[i] == 'T':
                value += round(i/2)
                if i + 2 < self.size:
                    if board.board[i + 1] == "_":
                        value += round((self.size - i)/2)
                        left_moves += 1
                    elif i + 2 < self.size:
                        if board.board[i + 1] == "F" and board.board[i + 2] == "_":
                            value += board.size - i
                            left_moves += 1
            
            # blocked moves
            if board.size > i + 2:
                if board.board[i] == "T" and board.board[i + 1] == 'F' and board.board[i + 2] == 'F':
                    value -= 15
            
            if i > 2:
                if board.board[i] == "F" and board.board[i - 1] == 'T' and board.board[i - 2] == 'T':
                    value += 15

            # face off?
            if board.board[i] == "T" and board.board[i + 1] == "F":
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
        for i in range (board.size - 1):

            if board.board[i] == 'T' and board.board[i + 1] == 'T':
                value += 5

            if board.board[i] == 'F' and board.board[i + 1] == 'F':
                value -= 5
            
            # skips vs. one space moves and distance from the end for frogs
            if board.board[i] == 'F':
                value -= round((board.size - 1 - i)/2)
                if i > 2:
                    if board.board[i - 1] == "_":
                        value -= i
                        right_moves += 1
                    elif board.board[i - 1] == 'T':
                        if board.board[i - 2] == '_':
                            value -= round(i/2)
                            right_moves += 1
            
            # blocked moves
            if board.size > i + 2:
                if board.board[i] == "T" and board.board[i + 1] == 'F' and board.board[i + 2] == 'F':
                    value += 25
            
            if i > 2:
                if board.board[i] == "F" and board.board[i - 1] == 'T' and board.board[i - 2] == 'T':
                    value -= 25

            # face off?
            if board.board[i] == "T" and board.board[i + 1] == "F":
                value -= 20

        # number of total moves
        value += (left_moves * 5)
        value -= (right_moves * 5)

        return value

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
            board.v = self.left_board_value(board)
            vnew, _, n = board.min_value_with_pruning(a, b, best_move, n)
            if vnew > value: 
                value = vnew
                best_move = child
            if value >= b:
                return value, best_move, n
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
            board.v = self.right_board_value(board)
            vnew, _, n = board.max_value_with_pruning(a, b, best_move, n)
            if vnew < value: 
                value = vnew
                best_move = child
            if value <= a:
                return value, best_move, n
            if vnew <= b:
                b = vnew
        return value, best_move, n
        

def main():
    pygame.init()

    # Variables for board size, altering size & scaling
    board_size = 20
    math_helper = -board_size*0.2 + 6
    CELL_WIDTH = math_helper * 30
    CELL_HEIGHT = math_helper * 40
    ICON_SCALE = (11 * math_helper, 8 * math_helper)

    # get window size from board
    screen_width = board_size * CELL_WIDTH
    screen_height = CELL_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Toads and Frogs")
    clock = pygame.time.Clock()

    # images
    background_gif = gif_pygame.load("/Users/gradydionne/Documents/GradyDionneTopicsInAI/Finalproject/Lilypad_in_water.gif")
    gif_pygame.transform.scale(background_gif, (CELL_WIDTH, CELL_HEIGHT))

    toad_image = pygame.transform.scale(
        pygame.image.load("/Users/gradydionne/Documents/GradyDionneTopicsInAI/Finalproject/Toad.png"), ICON_SCALE
    )
    frog_image = pygame.transform.scale(
        pygame.image.load("/Users/gradydionne/Documents/GradyDionneTopicsInAI/Finalproject/Frog.png"), ICON_SCALE
    )

    # Board state 
    # 'T' = Toad, 'F' = Frog, _ = empty
    # Toads fill left third, Frogs fill right third, middle is empty
    num_pieces = board_size // 3
    board = (['T'] * num_pieces + ['_'] * (board_size - 2 * num_pieces) + ['F'] * num_pieces)
    board_string = ",".join(str(i) for i in board)

    icon_x_offset = (CELL_WIDTH - ICON_SCALE[0]) // 2   # center icon horizontally in cell
    icon_y_offset = (CELL_HEIGHT - ICON_SCALE[1]) // 2   # center icon vertically in cell

    while Board.has_left_options or Board.has_right_options:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # Draw board cells
        for i in range(board_size):
            background_gif.render(screen, (i * CELL_WIDTH, 0))

        # Draw pieces based on board state
        for i, cell in enumerate(board):
            if cell == 'T':
                screen.blit(toad_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))
            elif cell == 'F':
                screen.blit(frog_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_cell = mouse_x // CELL_WIDTH  
                # which cell was clicked for testing
                print(f"Clicked cell {int(clicked_cell)}: {board[int(clicked_cell)]}")
                print(board_string)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()