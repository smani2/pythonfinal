import pygame
import random
from .constants import *

class Asteroid:
    """
    Represents a falling asteroid in the game.

    Attributes:
        size (int): The diameter of the asteroid.
        x (int): The horizontal position of the asteroid.
        y (int): The vertical position of the asteroid (starts off-screen).
        speed (int): The vertical speed at which the asteroid falls.
        rect (pygame.Rect): The rectangular boundary used for drawing and collision detection.
    """
    
    def __init__(self):
        """
        Initializes a new asteroid with random size, position, and speed.
        The asteroid starts above the screen and falls downward.
        """
        self.size = random.randint(10, 30)  # Random size between 10 and 30 pixels
        self.x = random.randint(0, WIDTH - self.size)  # Random horizontal position
        self.y = -self.size  # Start just above the visible screen
        self.speed = 0.15 
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Define the asteroid's shape

    def update(self):
        """
        Updates the asteroid's position by moving it downward.
        Returns:
            bool: True if the asteroid has moved beyond the bottom of the screen, else False.
        """
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Update position for drawing/collision
        return self.y > HEIGHT  # Return True if the asteroid is off-screen

    def draw(self, screen):
        """
        Draws the asteroid as a yellow ellipse on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw the asteroid on.
        """
        pygame.draw.ellipse(screen, YELLOW, self.rect)
