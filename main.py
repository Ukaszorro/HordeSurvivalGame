import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,
    K_l
)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game():
    def __init__(self):
        # create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemies_sprites_list = pygame.sprite.Group()
        self.game_over = False

    def process_events(self):
        """method to process all events. Returns False to close the window"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                # restarts game
                if self.game_over and event.type == K_l:
                    self.__init__()
        return True

    def run_logic(self):
        """method to update positions and check for collisions"""
        pass

    def display_frame(self, screen):

        screen.fill((0, 0, 0))
        if self.game_over:
            font = pygame.font.SysFont("Serif", 25)
            text = font.render("Game over", True, (0, 0, 0))

        pygame.display.flip()


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    running = True
    game = Game()

    while running:
        running = game.process_events()
        game.display_frame(screen)
        clock.tick(60)
        print(running)

    pygame.quit()


if __name__ == "__main__":
    main()
