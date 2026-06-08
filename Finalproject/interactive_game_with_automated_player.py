import pygame
import gif_pygame

class Board:

    def __init__(self, board: str):
        self.board = board.split(',')

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
            if pos < self.size - 1:
                if self.board[pos + 1] == '_':
                    return True
                if pos < self.size - 2:
                    if self.board[pos + 1] == "F" and self.board[pos + 2] == "_":
                        return True
            
        return False

    def valid_move_frog(self, pos):
        if self.board[pos] == "F":
            if pos >= 1:
                if self.board[pos - 1] == '_':
                    return True
                if pos >= 2:
                    if self.board[pos - 1] == "F" and self.board[pos - 2] == "_":
                        return True
            
        return False
    
    def make_move_toad(self, pos):
        moved_board = self.board.copy()
        if self.board[pos + 1] == '_':
            moved_board[pos] = '_'
            moved_board[pos + 1] = 'T'

        elif self.board[pos + 1] == "F" and self.board[pos + 2] == "_":
            moved_board[pos] = '_'
            moved_board[pos + 2] = "T"

        return moved_board

    def make_move_frog(self, pos):
        moved_board = self.board.copy()
        if self.board[pos - 1] == '_':
            moved_board[pos] = '_'
            moved_board[pos - 1] = 'F'

        elif self.board[pos - 1] == "T" and self.board[pos + 2] == "_":
            moved_board[pos] = '_'
            moved_board[pos - 2] = "F"

        return moved_board

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
    def max_value_with_pruning(self, a, b, best_move, n, max_depth, depth = 0):
        if self.is_leaf_node() or depth >= max_depth:
            return self.v, best_move, n
        
        children = self.get_left_options()

        if not children:
            return self.v, best_move, n

        value = float('-inf')

        for child in children:
            n += 1
            board = Board(child)
            board.v = self.left_board_value(board)
            vnew, _, n = board.min_value_with_pruning(a, b, best_move, n, max_depth, depth + 1)
            if vnew > value: 
                value = vnew
                best_move = child
            if value >= b:
                return value, best_move, n
            if vnew > a:
                a = vnew
        return value, best_move, n

    # min for min max search
    def min_value_with_pruning(self, a, b, best_move, n, max_depth, depth = 0):
        if self.is_leaf_node() or depth >= max_depth:
            return self.v, best_move, n
        
        children = self.get_right_options()

        if not children:
            return self.v, best_move, n
        
        value = float('inf')

        for child in children:
            n += 1
            board = Board(child)
            board.v = self.right_board_value(board)
            vnew, _, n = board.max_value_with_pruning(a, b, best_move, n, max_depth, depth + 1)
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
    clock = pygame.time.Clock()

    # initialize size
    MENU_W, MENU_H = 600, 400
    screen = pygame.display.set_mode((MENU_W, MENU_H))
    pygame.display.set_caption("Toads and Frogs")

    font_big   = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 30)

    # size variables
    board_size = 7          
    MIN_SIZE, MAX_SIZE = 5, 15

    '''
    Menu Loop
    '''
    in_menu = True
    while in_menu:
        clock.tick(60)
        screen.fill((20, 80, 20))

        title = font_big.render("Toads & Frogs", True, (255, 200, 50))
        screen.blit(title, (MENU_W // 2 - title.get_width() // 2, 60))

        size_text = font_small.render(f"Board size:  {board_size}", True, (255, 200, 50))
        screen.blit(size_text, (MENU_W // 2 - size_text.get_width() // 2, 180))

        hint = font_small.render("Press arrow keys to change  | Press ENTER to start", True, (0, 255, 255))
        screen.blit(hint, (MENU_W // 2 - hint.get_width() // 2, 240))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT  and board_size > MIN_SIZE:
                    board_size -= 2          
                elif event.key == pygame.K_RIGHT and board_size < MAX_SIZE:
                    board_size += 2
                elif event.key == pygame.K_RETURN:
                    in_menu = False        

    '''
    Initialize game here
    '''
    math_helper = -board_size * 0.2 + 6
    CELL_WIDTH  = int(math_helper * 30)
    CELL_HEIGHT = int(math_helper * 40)
    ICON_SCALE  = (int(11 * math_helper), int(8 * math_helper))

    screen = pygame.display.set_mode((board_size * CELL_WIDTH, CELL_HEIGHT))

    background_gif = gif_pygame.load("Lilypad_in_water.gif")
    gif_pygame.transform.scale(background_gif, (CELL_WIDTH, CELL_HEIGHT))
    toad_image = pygame.transform.scale(pygame.image.load("Toad.png"), ICON_SCALE)
    frog_image = pygame.transform.scale(pygame.image.load("Frog.png"), ICON_SCALE)

    num_pieces = board_size // 3
    board = ['T'] * num_pieces + ['_'] * (board_size - 2 * num_pieces) + ['F'] * num_pieces
    board_string = ",".join(board)
    gameboard = Board(board_string)

    icon_x_offset = (CELL_WIDTH - ICON_SCALE[0]) // 2
    icon_y_offset = (CELL_HEIGHT - ICON_SCALE[1]) // 2

    player = 'T'
    computer = 'F'
    current_turn = player
    a, b = float('-inf'), float('inf')

    '''
    Main Game Loop
    '''
    timer = 0
    delay = 500
    computer_delay = False
    max_depth = max(3, 9 - (board_size - 9))

    game = True
    while game == True:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # Draw board cells
        for i in range(board_size):
            background_gif.render(screen, (i * CELL_WIDTH, 0))

        # Draw pieces based on board state
        for i, cell in enumerate(gameboard.board):
            if cell == 'T':
                screen.blit(toad_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))
            elif cell == 'F':
                screen.blit(frog_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))

        # process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_cell = mouse_x // CELL_WIDTH  

                # which cell was clicked for testing dolphins (porpoises)
                print(f"Clicked cell {int(clicked_cell)}: {board[int(clicked_cell)]}")
                print(gameboard)

                if current_turn == player and gameboard.valid_move_toad(int(clicked_cell)):
                    new_board_list = gameboard.make_move_toad(int(clicked_cell))
                    gameboard = Board(",".join(new_board_list))
                    print("Player moved:", ",".join(gameboard.board))  
                    if not gameboard.has_right_options():
                        game = False
                    current_turn = computer

        if current_turn == computer:
            if not computer_delay:
                timer = pygame.time.get_ticks()
                computer_delay = True
            if computer_delay and pygame.time.get_ticks() - timer > delay:
                if gameboard.has_right_options():
                    test_case, best_move, n = Board.min_value_with_pruning(gameboard, a, b, None, 1, max_depth)
                    if best_move is not None:
                        gameboard = (Board(best_move))
                    print("Computer moved:", ",".join(gameboard.board))  
                    current_turn = player
                computer_delay = False
                if not gameboard.has_left_options():
                    game = False

        pygame.display.flip()


    '''
    End screen
    '''
    winner = "Toads win!" if not gameboard.has_right_options() else "Frogs win!"
    end = True
    while end:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # Draw board cells
        for i in range(board_size):
            background_gif.render(screen, (i * CELL_WIDTH, 0))

        # Draw pieces based on board state
        for i, cell in enumerate(gameboard.board):
            if cell == 'T':
                screen.blit(toad_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))
            elif cell == 'F':
                screen.blit(frog_image, (i * CELL_WIDTH + icon_x_offset, icon_y_offset))

        winner_text = font_big.render(winner, True, (0, 50, 0))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2,screen.get_height() // 2 - winner_text.get_height() * 1.75))

        bottom_text = font_small.render("Press R to restart  |  Q to quit", True, (0, 50, 0))
        screen.blit(bottom_text, (screen.get_width() // 2 - bottom_text.get_width() // 2, screen.get_height() // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    end = False

    pygame.quit()

if __name__ == "__main__":
    main()