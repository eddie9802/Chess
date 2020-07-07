import Board

import pygame


HEIGHT = 800
WIDTH = 800
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))


def game_loop():
    pygame.init()
    Board.init(pygame, gameDisplay)
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    while not hasQuit:
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == pygame.QUIT:
                hasQuit = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                Board.select_square(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Board.remove_selection()

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    game_loop()