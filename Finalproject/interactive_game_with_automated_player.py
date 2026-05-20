import pygame
import gif_pygame
import sys


# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Toads and Frogs")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
