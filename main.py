import pygame
import sys
from game.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rocket Coding Game")
    
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Keyboard controls
                if event.key in [pygame.K_s, pygame.K_LEFT, pygame.K_RIGHT]:
                    game.handle_keyboard_input(event.key)
                
                # Game state controls
                if game.state == Game.START and event.key == pygame.K_SPACE:
                    game.state = Game.PLAYING
                elif game.state == Game.GAME_OVER and event.key == pygame.K_r:
                    game.reset()
                    game.state = Game.PLAYING
                
                # Text command input
                elif game.state == Game.PLAYING:
                    if event.key == pygame.K_RETURN:
                        game.process_command()
                    elif event.key == pygame.K_BACKSPACE:
                        game.current_input = game.current_input[:-1]
                    elif event.unicode.isalpha() or event.unicode in '()_':
                        game.current_input += event.unicode
        
        game.update()
        game.draw(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()
