import pygame
from .constants import *

class Rocket:
    """
    Represents the rocket controlled by the player in the game.

    Attributes:
        width (int): The width of the rocket.
        height (int): The height of the rocket.
        x (int): The x-coordinate of the rocket's position.
        y (int): The y-coordinate of the rocket's position.
        speed (int): The movement speed of the rocket.
        launched (bool): Indicates whether the rocket has been launched.
        rect (pygame.Rect): The rectangular area representing the rocket's position and size.
        color (tuple): The color of the rocket.
    """

    def __init__(self):
        """
        Initializes the rocket at the bottom center of the screen.
        """
        self.width = 50
        self.height = 80
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.launched = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = RED

    def draw(self, screen):
        """
        Draws the rocket on the screen.
        
        Args:
            screen (pygame.Surface): The surface on which to draw the rocket.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw rocket nose
        pygame.draw.polygon(screen, WHITE, [
            (self.x + self.width//2, self.y - 20),
            (self.x, self.y),
            (self.x + self.width, self.y)
        ])

    def move_left(self):
        """
        Moves the rocket to the left if it has been launched.
        """
        if self.launched:
            self.x = max(0, self.x - self.speed)
            self.update_rect()

    def move_right(self):
        """
        Moves the rocket to the right if it has been launched.
        """
        if self.launched:
            self.x = min(WIDTH - self.width, self.x + self.speed)
            self.update_rect()

    def launch(self):
        """
        Launches the rocket and changes its color to indicate launch.
        """
        self.launched = True
        self.color = GREEN

    def update_rect(self):
        """
        Updates the rocket's rectangular boundary based on its current position.
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self):
        """
        Resets the rocket to its initial state.
        """
        self.__init__()
