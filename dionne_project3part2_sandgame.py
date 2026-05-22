'''
    Description of program: Sand game is a game where a player can click on the screen to draw sand, water, or floor 
    and interact in different ways with the world. sand, floor, and water all have different physics
    Filename: dionne_sand_game_p1.py
    Author: Grady Dionne
    Date: 1/29/2025
    Course: Comp 1352
    Assignment: Project 3 SandGame - Part 2
    Collaborators: None
    Internet Source: https://www.w3schools.com/python/python_ref_list.asp
'''

import dudraw
import random

class SandWorld:

    # constants for elements on the canvas
    SAND = 1
    EMPTY = 0
    FLOOR = 2
    WATER = 3

    def __init__(self, size: int):
        '''
        Function: Initialize variables gameboard (2D list for storing variables) and size (how big the rectangles in the grid are)
        Parameters: self, size
        Output: Size, Gameboard 2D list
        '''

        # initialize size and create 2D list for the gameboard
        self.size = size   
        gameboard = [[0 for _ in range (self.size)]for _ in range (self.size)]
        self.gameboard = gameboard
        updated_pixels = []
    
    def draw_world(self):
        '''
        Function: draws the canvas
        Parameters: size, gameboard, x (x axis counter), y (y axis counter),
        row (horizontal lines of sand) and grain (individual pixels in line of sand)
        I/O: creates canvas within main loop to show where sand is
        '''
        # initialize dudraw canvas

        '''
        This is where I planned on setting my canvas size, but if I put that code in it tells me that 
        my canvas size has already been set, even though I had never set it. it works fine in the test code,
        and I did a lot of digging but I can't seem to find the issue.
        '''
        dudraw.set_x_scale(0, self.size)
        dudraw.set_y_scale(0, self.size)
        dudraw.clear(dudraw.BOOK_LIGHT_BLUE)

        # scale for squares on canvas
        x = 0
        y = 0
        

        # sets colors of the squares in the 2D list
        for row in self.gameboard:
            for grain in row:
                if grain == SandWorld.EMPTY:
                    dudraw.set_pen_color(dudraw.BOOK_LIGHT_BLUE)
                    dudraw.filled_square(x + 0.5, y + 0.5, .6)
                    x += 1
                elif grain == SandWorld.SAND:
                    dudraw.set_pen_color_rgb(190, 178, 128)
                    dudraw.filled_square(x + 0.5, y + 0.5, .6)
                    x += 1
                elif grain == SandWorld.FLOOR:
                    dudraw.set_pen_color(dudraw.BLACK)
                    dudraw.filled_square(x + 0.5, y + 0.5, .6)
                    x += 1
                elif grain == SandWorld.WATER:
                    dudraw.set_pen_color_rgb(10 , 10, 245)
                    dudraw.filled_square(x + 0.5, y + 0.5, .6)
                    x += 1

            y += 1
            x = 0

    def draw_sand(self):
        '''
        Function: draws sand on the gameboard when the mouse is clicked
        Parameters: x_cord and y_cord, positions in the 2D list where user clicks
        I/O: returns a grain of sand where the user clicks
        '''

        # detects if mouse is pressed and returns coordinates as points in the 2D list
        if dudraw.mouse_is_pressed():
            x_cord = int(dudraw.mouse_x())
            y_cord = int(dudraw.mouse_y())

            # changes the x coordinate so that sand somes from 0-3 pixels away on either side
            x_cord = int(x_cord + random.randint(-3,3))

            # appends the 2D list with the new coordinates
            if 0 <= x_cord < self.size and 0 <= y_cord < self.size:
                if not self.gameboard[y_cord][x_cord] == SandWorld.FLOOR:
                    self.gameboard[y_cord][x_cord] = SandWorld.SAND
                    
        # calls function to make the sand fall
        self.sand_falls()
    
    def sand_falls(self):
        '''
        Function: Takes input when sand is drawn and applies the affect of gravity
        Parameters: size, gameboard
        I/O: Returns sand in a spot one lower than previous
        '''

        # list for deciding which direction to move
        listy = [True, False]

        # if index in row below is empty, sand and blank spot switch places, continues to bottom row
        # go from bottom up
        for i in range(1, self.size):
            for j in range(self.size -1, -1, -1):

                # new choice for direction
                right = random.choice(listy)

                if self.gameboard[i][j] == SandWorld.SAND and self.gameboard[i - 1][j] == SandWorld.EMPTY:
                    self.gameboard[i][j] = SandWorld.EMPTY
                    self.gameboard[i - 1][j] = SandWorld.SAND

                # if there are 2 sand particles on top of each other
                elif self.gameboard[i][j] == SandWorld.SAND and self.gameboard[i-1][j] == SandWorld.SAND:
                    
                    # make sand move diagonally down left if left is empty
                    if right:
                        if j < self.size - 1 and self.gameboard[i - 1][j + 1] == SandWorld.EMPTY:
                            self.gameboard[i][j] = SandWorld.EMPTY
                            self.gameboard[i - 1][j + 1] = SandWorld.SAND
                    
                    # make sand move diagonally down right if right is empty
                    else:
                        if j > 0 and self.gameboard[i - 1][j - 1] == SandWorld.EMPTY:
                            self.gameboard[i][j] = SandWorld.EMPTY
                            self.gameboard[i - 1][j - 1] = SandWorld.SAND


                # make sand sink through water
                if self.gameboard[i][j] == SandWorld.SAND and self.gameboard[i-1][j] == SandWorld.WATER:
                    self.gameboard[i][j], self.gameboard[i - 1][j] = self.gameboard[i - 1][j], self.gameboard[i][j]

                    # sand still moves diagonally through water

                elif j > 1 and j < self.size - 1:
                    if self.gameboard[i][j] == SandWorld.SAND and (self.gameboard[i-1][j-1] == SandWorld.WATER or self.gameboard[i-1][j+1] == SandWorld.WATER): 
                        if right:
                            if j < self.size - 1 and self.gameboard[i - 1][j + 1] == SandWorld.WATER:
                                self.gameboard[i][j], self.gameboard[i - 1][j + 1] = self.gameboard[i - 1][j + 1], self.gameboard[i][j]

                        else: 
                            if j > 0 and self.gameboard[i - 1][j - 1] == SandWorld.WATER:
                                self.gameboard[i][j], self.gameboard[i - 1][j - 1] = self.gameboard[i - 1][j - 1], self.gameboard[i][j]
        
        
    def draw_floor(self):
        '''
        Function: Updates the 2D list of gameboard with a number 2 to signify a drawn floor for sand to land on
        Parameters: self, gameboard, x_cord, y_cord
        I/O: input is gameboard, output is 2D list append
        '''
    
        # check for mouse press
        if dudraw.mouse_is_pressed():
            x_cord = int(dudraw.mouse_x())
            y_cord = int(dudraw.mouse_y())

            # appends the 2D list with the new coordinates
            if 0 <= x_cord < self.size and 0 <= y_cord < self.size:
                self.gameboard[y_cord][x_cord] = SandWorld.FLOOR
                self.gameboard[y_cord + 1][x_cord] = SandWorld.FLOOR
                self.gameboard[y_cord - 1][x_cord] = SandWorld.FLOOR
                self.gameboard[y_cord][x_cord + 1] = SandWorld.FLOOR
                self.gameboard[y_cord][x_cord - 1] = SandWorld.FLOOR

    def draw_water(self):
        '''
        Function: Updates the 2D list of gameboard with a number 3 to create water
        Parameters: size, gameboard, x_cord, y_cord
        I/O: 2D list
        '''

        if dudraw.mouse_is_pressed():
            x_cord = int(dudraw.mouse_x())
            y_cord = int(dudraw.mouse_y())

            # changes the x coordinate so that sand somes from 0-3 pixels away on either side
            x_cord = int(x_cord + random.randint(-3,3))

            # appends the 2D list with the new coordinates
            if 0 <= x_cord < self.size and 0 <= y_cord < self.size:
                if not self.gameboard[y_cord][x_cord] == SandWorld.FLOOR:
                    if not self.gameboard[y_cord][x_cord] == SandWorld.SAND:
                        self.gameboard[y_cord][x_cord] = SandWorld.WATER

        # make the water particles move
        self.water_flows()


    def water_flows(self):
        '''
        Function: Takes input when water is drawn and applies the affect of gravity and flow
        Parameters: size, gameboard, x_cord, y_cord
        I/O: Returns water in a spot one lower than previous and creates a flowing and pooling effect
        '''

        # random selection for water to move left or right
        listy = [True, False]

        # traverse 2D list to make water fall
        for i in range(1, self.size):
            for j in range(self.size -1, -1, -1):

                # random choice for direction
                right = random.choice(listy)

                # water moves down first
                if self.gameboard[i][j] == SandWorld.WATER and self.gameboard[i - 1][j] == SandWorld.EMPTY:
                    self.gameboard[i][j] = SandWorld.EMPTY
                    self.gameboard[i - 1][j] = SandWorld.WATER

                # make water move right
                if right:
                    if j > 0 and self.gameboard[i][j] == SandWorld.WATER and self.gameboard[i][j - 1] == SandWorld.EMPTY:
                        self.gameboard[i][j] = SandWorld.EMPTY
                        self.gameboard[i][j - 1] = SandWorld.WATER
                    
                    # make water move diagonally down if it is blocked from moving sideways
                    elif j > 0 and self.gameboard[i][j] == SandWorld.WATER and self.gameboard[i - 1][j - 1] == SandWorld.EMPTY:
                        self.gameboard[i][j] = SandWorld.EMPTY
                        self.gameboard[i - 1][j - 1] = SandWorld.WATER

                # make water move left
                else: 
                    if j < self.size - 1 and self.gameboard[i][j] == SandWorld.WATER and self.gameboard[i][j + 1] == SandWorld.EMPTY:
                        self.gameboard[i][j] = SandWorld.EMPTY
                        self.gameboard[i][j + 1] = SandWorld.WATER
                    
                    # make water move diagonally down if it is blocked from moving sideways
                    elif j < self.size - 1 and self.gameboard[i][j] == SandWorld.WATER and self.gameboard[i - 1][j + 1] == SandWorld.EMPTY:  
                        self.gameboard[i][j] = SandWorld.EMPTY
                        self.gameboard[i - 1][j + 1] = SandWorld.WATER         

def main():
    '''
    Function: Run main animation to create canvas, draw sand, and make sand fall
    Parameters: world, size
    I/O: n/a
    '''

    # set the size of the 2D list, grid, and sand grains
    size = 100

    # initialize variables
    world = SandWorld(size)
    world.draw_world()

    # by default, the game starts in sand mode
    dudraw.set_font_size(15)
    dudraw.set_font_family('Helvetica')
    mode = "SAND"

    key = ''
    while key != 'q':

        # draw sand, floor, or nothing based on the 2D list
        world.draw_world()

        # display what mode you are in in the top left corner
        dudraw.set_pen_color(dudraw.BLACK)
        dudraw.text(5, size-3, mode)

        # draw sand or floor based on the mode
        if mode == "SAND":
            world.draw_sand()
            world.water_flows()
        elif mode == "FLOOR":
            world.draw_floor()
            world.water_flows()
            world.sand_falls()
        elif mode == "WATER":
            world.draw_water()
            world.sand_falls()

        # change game mode if key pressed
        if dudraw.has_next_key_typed():
            key = dudraw.next_key()
            if key == 'f':
                dudraw.set_pen_color(dudraw.BLACK)
                mode = "FLOOR"
                dudraw.text(5, size-3, mode)  

            elif key == 's':
                dudraw.set_pen_color(dudraw.BLACK)
                mode = "SAND"
                dudraw.text(5, size-3, mode)   

            elif key == 'w':
                dudraw.set_pen_color(dudraw.BLACK)
                mode = "WATER"
                dudraw.text(5, size-3, mode)   
        
        # display the animation
        dudraw.show(10)

        
if __name__ == "__main__":
    main()