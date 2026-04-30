import random
import DLL

"""
Problem 1: Write a function which creates a list of all possible Toads and Frogs positions of size n.
"""

# use a doubly linked list so previous functions still work, set n to desired size
n = 10

# empty list of lists
positions = []

# nested list of sorts
while len(positions) < n*n:
# initialize list to size n
    for i in range(n):  

        # populate list iteratively with either toad, frog, or empty space

        

# 

"""
Problem 2:

Write a function which creates a list of all possible Toads and Frogs positions of size n which
exactly contain a given number of Toads t and a given number of Frogs f.
"""

"""
Problem 3:

For each of the two functions from Problem 1 and Problem 2, build a table which shows for each n, 
the size of the list of positions, and the number of seconds it took to generate the list. The table 
should start at n = 3 and continue until n is big enough that either it takes 30 minutes to run or your 
computer doesn't have enough memory to build the list of positions.
"""
