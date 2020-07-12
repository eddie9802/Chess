import Board
import pkg_resources.py2_warn
import pygame


HEIGHT = 800
WIDTH = 800
LEFT = 1
RIGHT = 3
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))


def game_loop():
    pygame.init()
    Board.init(GAME_DISPLAY)
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    while not hasQuit:
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == pygame.QUIT:
                hasQuit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                Board.select_square(pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                pos = pygame.mouse.get_pos()
                Board.promote_pawn(pos)


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Board.remove_selection()

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    game_loop()