import random
import pygame
from .rocket import Rocket
from .asteroid import Asteroid
from .constants import *
from utils.command_validator import CommandValidator

class Game:
    """
    The main Game class controlling the logic, rendering, and state of the rocket game.
    """

    # Game state constants
    START = START
    PLAYING = PLAYING
    GAME_OVER = GAME_OVER

    def __init__(self):
        """
        Initializes the game, setting the initial state, creating the rocket,
        preparing asteroid list, setting fonts, and preparing UI messaging.
        """
        self.rocket = Rocket()
        self.asteroids = []
        self.state = START
        self.score = 0
        self.current_input = ""
        self.message = ""
        self.message_color = WHITE
        self.message_timer = 0
        self.asteroid_spawn_rate = 60
        self.spawn_counter = 0
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 36)
        self.validator = CommandValidator()
    
    def handle_keyboard_input(self, key):
        """Handle direct keyboard input"""
        if key == pygame.K_s:
            if not self.rocket.launched:
                self.rocket.launch()
                self.show_message("Rocket launched with key!", GREEN)
            else:
                self.show_message("Rocket already launched!", YELLOW)
        elif key == pygame.K_LEFT:
            if self.rocket.launched:
                self.rocket.move_left()
                self.show_message("Moved left with key!", GREEN)
            else:
                self.show_message("Rocket not launched yet!", RED)
        elif key == pygame.K_RIGHT:
            if self.rocket.launched:
                self.rocket.move_right()
                self.show_message("Moved right with key!", GREEN)
            else:
                self.show_message("Rocket not launched yet!", RED)


    def process_command(self):
        """
        Processes the current input string as a command.
        Validates input and controls the rocket if the command is correct.
        """
        if not self.validator.validate(self.current_input.strip()):
            self.show_message("Invalid command! Try again.", RED)
            self.current_input = ""
            return

        command = self.current_input.strip().lower()
        self.current_input = ""

        if command == "launch_rocket()":
            if not self.rocket.launched:
                self.rocket.launch()
                self.show_message("Correct Command! Rocket launched!", GREEN)
            else:
                self.show_message("Rocket already launched!", YELLOW)

        elif command == "move_left()":
            if self.rocket.launched:
                self.rocket.move_left()
                self.show_message("Correct Command! Rocket moved left.", GREEN)
            else:
                self.show_message("Rocket not launched yet!", RED)

        elif command == "move_right()":
            if self.rocket.launched:
                self.rocket.move_right()
                self.show_message("Correct Command! Rocket moved right.", GREEN)
            else:
                self.show_message("Rocket not launched yet!", RED)

    def show_message(self, text, color):
        """
        Displays a temporary message to the player.

        Args:
            text (str): The message to display.
            color (tuple): RGB color of the message text.
        """
        self.message = text
        self.message_color = color
        self.message_timer = 120  # Display message for 120 frames

    def update(self):
        """
        Updates the game logic depending on the state.
        Handles asteroid spawning, movement, collision, and scoring.
        """
        if self.state == PLAYING:
            # Spawn asteroids over time
            self.spawn_counter += 1
            if self.spawn_counter >= self.asteroid_spawn_rate:
                self.asteroids.append(Asteroid())
                self.spawn_counter = 0
                self.asteroid_spawn_rate = max(20, 60 - self.score // 5)

            # Update asteroid positions
            for asteroid in self.asteroids[:]:
                if asteroid.update():
                    self.asteroids.remove(asteroid)
                    self.score += 1

            # Check for collision with the rocket
            for asteroid in self.asteroids:
                if self.rocket.rect.colliderect(asteroid.rect):
                    self.state = GAME_OVER
                    self.show_message(f"Game Over! Score: {self.score}", RED)
                    break

        # Decrease message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

    def draw(self, screen):
        """
        Draws all visual elements on the screen depending on game state.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        screen.fill(BLACK)

        # Draw background stars
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), 1)

        if self.state == START:
            self.draw_start_screen(screen)
        elif self.state in (PLAYING, GAME_OVER):
            self.draw_game_screen(screen)
            if self.state == GAME_OVER:
                self.draw_game_over_screen(screen)

        pygame.display.flip()

    def draw_start_screen(self, screen):
        """
        Renders the start screen with instructions and title.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        title = self.large_font.render("Rocket Coding Game", True, WHITE)
        instruction1 = self.font.render("Type Python commands to control the rocket:", True, WHITE)
        instruction2 = self.font.render("launch_rocket(), move_left(), move_right()", True, GREEN)
        instruction3 = self.font.render("Press SPACE to start", True, YELLOW)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, 250))
        screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, 300))
        screen.blit(instruction3, (WIDTH // 2 - instruction3.get_width() // 2, 400))

    def draw_game_screen(self, screen):
        """
        Renders the active game screen with rocket, asteroids, score, and input.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        self.rocket.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        # Display score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw input box
        pygame.draw.rect(screen, WHITE, (50, HEIGHT - 50, WIDTH - 100, 40), 2)
        input_text = self.font.render("> " + self.current_input, True, WHITE)
        screen.blit(input_text, (60, HEIGHT - 45))

        # Show feedback message
        if self.message:
            msg_surface = self.font.render(self.message, True, self.message_color)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT - 100))

    def draw_game_over_screen(self, screen):
        """
        Renders the game over overlay and restart prompt.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
        screen.blit(overlay, (0, 0))

        game_over = self.large_font.render("GAME OVER", True, RED)
        restart = self.font.render("Press R to restart", True, WHITE)
        screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

    def reset(self):
        """
        Resets the game to its initial state (like restarting).
        """
        self.__init__()
