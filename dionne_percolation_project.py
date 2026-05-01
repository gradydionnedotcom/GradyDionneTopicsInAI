from __future__ import annotations
import random
import SLL
import dudraw
import matplotlib.pyplot as plt
import numpy as np

'''
Grady Dionne - Percolation project
Will the fire be able to spread across the canvas

    Description of program: A simulation using depth first and breadth first searches to see if a fire will 
    spread to the bottom of the forest

    Filename: dionne_percolation_project.py
    Author: Grady Dionne
    Date: 4/29/2025
    Course: Comp 1353
    Assignment: Project 3 - Percolation part 1
    Collaborators: None
    Internet Source: dudraw reference website
'''

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
    
class Cell:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __str__(self):
        return f"Cell: {self.row}, {self.column}"

class Forest:
    '''
    Basis for the simulation
    '''
    def __init__(self, w, h, d):
        self.width = w
        self.height = h
        self.density = d
        self.canvas = [[1 if random.random() < self.density else 0 for _ in range(self.width)]for _ in range(self.height)]

    def __str__(self):
        return f"{self.canvas}"

    def start_fire_depth(self):
        '''
        Function to light the top row on fire for depth first search
        '''
        cells_to_explore = Stack()
        #set the top row of the forest on fire
        for col in range(self.width):
            if self.canvas[self.height - 1][col] == 1:
                self.canvas[self.height - 1][col] = 2  # mark as on fire
                cells_to_explore.push(Cell(self.height - 1, col)) 

        # return the stack
        return cells_to_explore
    
    def depth_first_search(self, cells_to_explore: Stack):
        '''
        A Function that searches for adjacent tiles exploring the furthest reaches of one pathway first, spreading the fire to other trees if possible
        '''
        #continue lighting neighbors on fire
        #As long as cells_to_explore is not empty
        current_cell = cells_to_explore.pop()
        r = current_cell.row
        c = current_cell.column
        #pop the stack into current_cell
        #if current_cell is on the bottom row then the fire spreads and we should return true
        if r > 0:
            if self.canvas[r - 1][c] == 1:
                self.canvas[r - 1][c] = 2
                cells_to_explore.push(Cell(r - 1, c)) 
        if r < self.height - 1:
            if self.canvas[r + 1][c] == 1:
                self.canvas[r + 1][c] = 2
                cells_to_explore.push(Cell(r + 1, c)) 
        if c > 0:
            if self.canvas[r][c - 1] == 1:
                self.canvas[r][c - 1] = 2
                cells_to_explore.push(Cell(r, c - 1)) 
        if c < self.height - 1:
            if self.canvas[r][c + 1] == 1:
                self.canvas[r][c + 1] = 2
                cells_to_explore.push(Cell(r, c + 1)) 
        
        # check if fire reached the bottom
        if r == 0:
            return True
        else:
            return False

    def start_fire_breadth(self):
        '''
        Function to light the top row on fire for breadth first search
        '''
        cells_to_explore = Queue()
        #set the top row of the forest on fire
        for col in range(self.width):
            if self.canvas[self.height - 1][col] == 1:
                self.canvas[self.height - 1][col] = 2  # mark as on fire
                cells_to_explore.enqueue(Cell(self.height - 1, col)) 

        # return the queue
        return cells_to_explore


    def breadth_first_search(self, cells_to_explore: Queue):
        '''
        A function that searches for adjacent tiles exploring every pathway one away from each cell first, lighting trees on fire if possible
        '''
        current_cell = cells_to_explore.dequeue()
        r = current_cell.row
        c = current_cell.column
        #pop the stack into current_cell
        #if current_cell is on the bottom row then the fire spreads and we should return true
        if r > 0:
            if self.canvas[r - 1][c] == 1:
                self.canvas[r - 1][c] = 2
                cells_to_explore.enqueue(Cell(r - 1, c)) 
        if r < self.height - 1:
            if self.canvas[r + 1][c] == 1:
                self.canvas[r + 1][c] = 2
                cells_to_explore.enqueue(Cell(r + 1, c)) 
        if c > 0:
            if self.canvas[r][c - 1] == 1:
                self.canvas[r][c - 1] = 2
                cells_to_explore.enqueue(Cell(r, c - 1)) 
        if c < self.height - 1:
            if self.canvas[r][c + 1] == 1:
                self.canvas[r][c + 1] = 2
                cells_to_explore.enqueue(Cell(r, c + 1)) 
        
        # Check if fire reached the bottom
        if r == 0:
            return True
        else:
            return False

    def draw(self):
        '''
        A function to draw the simulation of fire spreading
        '''
        x = 0
        y = 0

        # loop through the 2D canvas list and color the cells accordingly
        for row in self.canvas:
            for pixel in row:
                if pixel == 0:
                    dudraw.set_pen_color(dudraw.LIGHT_GRAY)
                    dudraw.filled_square(x + 0.5, y + 0.5, .5)
                    x += 1
                elif pixel == 1:
                    dudraw.set_pen_color(dudraw.DARK_GREEN)
                    dudraw.filled_square(x + 0.5, y + 0.5, .5)
                    x += 1
                elif pixel == 2:
                    dudraw.set_pen_color(dudraw.RED)
                    dudraw.filled_square(x + 0.5, y + 0.5, .5)
                    x += 1

            y += 1
            x = 0

class FireProbability:
    '''

    '''
    def probability_of_fire_spread_dfs(self, d):
        # given a density "d"
        fire_spread_count = 0

        for i in range (1000):
            f = Forest(50, 50, d)
            cells_to_explore = f.start_fire_depth()
            while not cells_to_explore.is_empty():
                percolation = f.depth_first_search(cells_to_explore)
                if percolation:
                    fire_spread_count += 1

        # the probability of fire spreading in forests of density "d" is:
        return fire_spread_count/1000


    def probability_of_fire_spread_bfs(self, d):
        # given a density "d"
        fire_spread_count = 0

        for _ in range (1000):
            f = Forest(50, 50, d)
            cells_to_explore = f.start_fire_breadth()
            while not cells_to_explore.is_empty():
                percolation = f.breadth_first_search(cells_to_explore)
                if percolation:
                    fire_spread_count += 1
                    break

        # the probability of fire spreading in forests of density "d" is:
        return fire_spread_count/1000

    def highest_Density_dfs(self):
        low_density = 0.0
        high_density = 1.0

        while high_density > low_density:
            #check the midpoint
            density = (high_density + low_density) / 2.0

            #get probability of fire spreading in forests of 'density'
            p = self.probability_of_fire_spread_dfs(density)

            #check probability of fire spreading
            if p < 0.5:
                #low probability: density can be increased
                low_density = density + 0.01
            else:
                #high probability: density should be decreased
                high_density = density - 0.01
                # // the last value of "density" is the value we seek

        return density

    def highest_Density_bfs(self):
        low_density = 0.0
        high_density = 1.0

        while high_density > low_density:
            #check the midpoint
            density = (high_density + low_density) / 2.0

            #get probability of fire spreading in forests of 'density'
            p = self.probability_of_fire_spread_bfs(density)

            #check probability of fire spreading
            if p < 0.5:
                #low probability: density can be increased
                low_density = density + 0.01
            else:
                #high probability: density should be decreased
                high_density = density - 0.01
                # // the last value of "density" is the value we seek

        return density
    
def plot_fire_probability():
    fp = FireProbability()
    densities = [i / 20 for i in range(21)]  # Densities from 0.0 to 1.0 in steps of 0.05
    probabilities = []

    for d in densities:
        # p = fp.probability_of_fire_spread_dfs(d)
        p = fp.probability_of_fire_spread_bfs(d)
        probabilities.append(p)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(densities, probabilities, marker='o', linestyle='-')
    plt.title("Probability of Fire Spread vs Forest Density (BFS)")
    plt.xlabel("Forest Density")
    plt.ylabel("Probability of Fire Spreading")
    plt.grid(True)
    plt.show()

def main():

    # variable for size
    size = 50

    # initialize canvas
    dudraw.set_canvas_size(600, 600)
    dudraw.set_x_scale(0, size)
    dudraw.set_y_scale(0, size)

    # create a forest object
    the_forest = Forest(size, size, .9)

    # graph results
    plot_fire_probability()

    # create the cells to explore queue or stack
    cells_to_explore = the_forest.start_fire_breadth()
    # cells_to_explore = the_forest.start_fire_depth()

    display_text = ""
    
    # loop to run the simulation while pathways are available
    while not cells_to_explore.is_empty():

        # clear the canvas
        dudraw.clear(dudraw.LIGHT_GRAY)

        # search functions
        percolation = the_forest.breadth_first_search(cells_to_explore)
        # percolation = the_forest.depth_first_search(cells_to_explore)

        # check if the fire reached the bottom
        if percolation:
            display_text = "Fire Percolated"
            break
        if not percolation:
            display_text = "Fire Did Not Percolate"

        # call the draw and show functions
        the_forest.draw()
        dudraw.show(1)

    # keep the display when the simulation ends and display if the fire percolated or not
    the_forest.draw()
    dudraw.set_font_size(30)
    dudraw.set_font_family('Courier')
    dudraw.set_pen_color(dudraw.BLACK)
    dudraw.text(size / 2, size / 2, display_text)
    dudraw.show(float("inf"))
    

if __name__ == "__main__":
    main()