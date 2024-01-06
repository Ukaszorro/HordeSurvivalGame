import pygame
import random
import math
from math_functions import count_angle

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,
    K_l,
    MOUSEBUTTONDOWN
)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def update(self, pressed_keys, mouse):
        # move player
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        # create enemy at random place outside the screen
        left_side = random.randint(-100, -25)
        right_side = random.randint(SCREEN_WIDTH + 25, SCREEN_WIDTH + 100)
        top = random.randint(SCREEN_HEIGHT + 25, SCREEN_HEIGHT + 100)
        bottom = random.randint(-100, -25)
        horizontal = (left_side, right_side)
        vertical = (top, bottom)
        self.rect = self.surf.get_rect(center=(
            # choose sides randomly
            horizontal[random.randint(0, 1)],
            vertical[random.randint(0, 1)]
        ))

        self.speed = 5

    def update(self, player_position):
        # get coordinates of player and enemy
        point1 = player_position[:2]
        point2 = self.rect[:2]

        angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
        cosinus = math.cos(angle)
        sinus = math.sin(angle)

        # count speed on each axis
        x = cosinus * self.speed
        y = sinus * self.speed

        # make sure enemy goes in correct direction

        self.rect.move_ip(-x, -y)
        # print(sinus, angle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos):
        super(Bullet, self).__init__()
        self.player_pos = (player_pos[0] + player_pos[2] / 2, player_pos[1] + player_pos[3] / 2)
        self.mouse_pos = mouse_pos
        self.speed = 20
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(
            self.player_pos[0],
            self.player_pos[1]
        ))
        angle = math.atan2((self.mouse_pos[1] - self.rect.y), (self.mouse_pos[0] - self.rect.x))
        self.x = self.speed * math.cos(angle)
        self.y = self.speed * math.sin(angle)

    def update(self):
        self.rect.move_ip(self.x, self.y)


class Game():
    def __init__(self):
        # create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemies_sprites_list = pygame.sprite.Group()

        self.new_enemy = Enemy()
        self.all_sprites_list.add(self.new_enemy)
        self.enemies_sprites_list.add(self.new_enemy)

        self.player = Player()
        self.all_sprites_list.add(self.player)

        self.bullets_sprites_list = pygame.sprite.Group()

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
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_bullet = Bullet(self.player.rect, pygame.mouse.get_pos())
                    self.bullets_sprites_list.add(new_bullet)
                    self.all_sprites_list.add(new_bullet)

        return True

    def run_logic(self):
        """method to update positions and check for collisions"""

        # Get the set of keys pressed and check for user inputda
        pressed_keys = pygame.key.get_pressed()

        pressed_mouse = pygame.mouse.get_pressed()

        self.player.update(pressed_keys, pygame.mouse)

        self.enemies_sprites_list.update((self.player.rect[0], self.player.rect[1]))
        self.bullets_sprites_list.update()

    def display_frame(self, screen):
        """Display everything on the screen"""
        screen.fill((0, 0, 0))
        if self.game_over:
            font = pygame.font.SysFont("Serif", 25)
            text = font.render("Game over", True, (0, 0, 0))
        else:
            # draw all sprites
            for entity in self.all_sprites_list:
                screen.blit(entity.surf, entity.rect)

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
        game.run_logic()
        game.display_frame(screen)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

# helped with bullet trajectory: https://stackoverflow.com/questions/43951409/pygame-bullet-motion-from-point-a-to-point-b
