# lines if other enemies blocking path search for different way to player

import pygame
import random
import math
import time
from math_functions import count_angle, find_point_circle, distance_points, hypotenuse
from tiles import Level
from settings import *
from support import import_folder

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


# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 720


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.import_assets()
        self.frame_index = 0
        self.animations_speed = 0.5
        player_image = pygame.transform.scale(self.animations['idle'][self.frame_index], (75, 75))
        self.surf = player_image
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.rect.width = 25
        self.rect.height = 25

    def import_assets(self):
        character_path = "images/Top_Down_Survivor/handgun/"
        self.animations = {'idle': [], 'move': [], 'shoot': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations['idle']

        # loop over frame index
        self.frame_index += self.animations_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.surf = pygame.transform.scale(animation[int(self.frame_index)], (75, 75))

    def update(self, pressed_keys, mouse):

        self.animate()
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
        enemy_image = pygame.transform.scale(pygame.image.load("images/zombie/skeleton-idle_0.png").convert_alpha(),
                                             (75, 75))
        self.surf = enemy_image
        # self.surf.fill((255, 255, 255))

        # create enemy at random place outside the screen
        left_side = random.randint(-100, -25)
        right_side = random.randint(SCREEN_WIDTH + 25, SCREEN_WIDTH + 100)
        top = random.randint(SCREEN_HEIGHT + 25, SCREEN_HEIGHT + 100)
        bottom = random.randint(-100, -25)
        horizontal = (left_side, right_side)
        vertical = (top, bottom)
        option1 = (horizontal[random.randint(0, 1)], random.randint(-100, SCREEN_HEIGHT + 100))
        option2 = (random.randint(-100, SCREEN_WIDTH + 100), vertical[random.randint(0, 1)])
        options = (option1, option2)
        # choose sides randomly
        self.rect = self.surf.get_rect(center=options[random.randint(0, 1)])

        self.rect.width = 50
        self.rect.height = 50

        self.speed = random.randint(2, 3)

    def update(self, player_position, distance=0):
        if distance == 0:
            distance = self.speed
        else:
            print(distance)

        # get coordinates of player and enemy
        point1 = player_position[:2]
        point2 = self.rect[:2]

        angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
        cosinus = math.cos(angle)
        sinus = math.sin(angle)

        # count speed on each axis
        x = cosinus * distance
        y = sinus * distance

        # make sure enemy goes in correct direction

        self.rect.move_ip(-x, -y)
        # print(sinus, angle)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy2, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((100, 100, 100))

        # choose sides randomly
        self.rect = self.surf.get_rect(
            center=(random.randint(25, SCREEN_WIDTH - 25), random.randint(25, SCREEN_HEIGHT + 25)))

        self.speed = random.randint(2, 3)

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
    def __init__(self, screen):
        self.screen = screen
        self.level = Level(level_map, self.screen)
        # create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemies_sprites_list = pygame.sprite.Group()

        self.new_enemy = Enemy()
        self.all_sprites_list.add(self.new_enemy)
        self.enemies_sprites_list.add(self.new_enemy)

        self.dummy = Enemy2()
        self.all_sprites_list.add(self.dummy)

        self.player = Player()
        self.all_sprites_list.add(self.player)

        self.bullets_sprites_list = pygame.sprite.Group()

        # create custom event for adding a new enemy
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 500)

        self.game_over = False
        self.score = 0
        self.start = time.time()
        self.finish = time.time()

    def process_events(self):
        """method to process all events. Returns False to close the window"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                # restarts game
                if self.game_over and event.key == K_l:
                    self.__init__(self.screen)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_bullet = Bullet(self.player.rect, pygame.mouse.get_pos())
                    self.bullets_sprites_list.add(new_bullet)
                    self.all_sprites_list.add(new_bullet)
            elif event.type == self.ADDENEMY:
                new_enemy = Enemy()
                self.all_sprites_list.add(new_enemy)
                self.enemies_sprites_list.add(new_enemy)

        return True

    def run_logic(self):
        """method to update positions and check for collisions"""

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        pressed_mouse = pygame.mouse.get_pressed()

        self.player.update(pressed_keys, pygame.mouse)

        # self.enemies_sprites_list.update((self.player.rect[0], self.player.rect[1]))
        for enemy in self.enemies_sprites_list:
            # remember the last position in case there will be a collision
            placeholder_x = enemy.rect.x
            placeholder_y = enemy.rect.y
            enemy.update((self.player.rect[0], self.player.rect[1]))

            # check if enemies collide with each other
            if pygame.sprite.spritecollide(enemy, self.enemies_sprites_list, 0) \
                    and pygame.sprite.spritecollide(enemy, self.enemies_sprites_list, 0) != [enemy]:
                collided_enemy = pygame.sprite.spritecollide(enemy, self.enemies_sprites_list, 0)[1]
                enemy.rect.x, enemy.rect.y = placeholder_x, placeholder_y

                enemy.speed = -enemy.speed
                enemy.update(collided_enemy.rect[:2])
                enemy.speed = -enemy.speed

                point = find_point_circle(self.player.rect[:2], enemy.rect[:2], enemy.speed,
                                          distance_points(self.player.rect[:2], enemy.rect[:2]))
                enemy.update(point)

            # check if bullet hit enemy
            if pygame.sprite.spritecollide(enemy, self.bullets_sprites_list, 0):
                bullet = pygame.sprite.spritecollide(enemy, self.bullets_sprites_list, 0)
                bullet[0].kill()
                enemy.kill()
                if not self.game_over:
                    self.score += 1

        if pygame.sprite.spritecollide(self.player, self.enemies_sprites_list, 0):
            pygame.sprite.spritecollide(self.player, self.enemies_sprites_list, 0)[0].kill()
            if not self.game_over:
                self.finish = time.time()
            self.game_over = True

        self.bullets_sprites_list.update()
        point = find_point_circle(self.player.rect[:2], self.dummy.rect[:2], self.dummy.speed,
                                  distance_points(self.player.rect[:2], self.dummy.rect[:2]))
        self.dummy.update(point)

    def display_frame(self):
        """Display everything on the screen"""
        self.screen.fill((0, 0, 0))

        # game over screen
        if self.game_over:
            font = pygame.font.SysFont("Serif", 25)
            text = font.render(f"""Game over\n Score: {self.score} Time: {round(self.finish - self.start, 2)}""", True,
                               (255, 255, 255))
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            self.screen.blit(text, [center_x, center_y])
        else:
            # draw all sprites
            for entity in self.all_sprites_list:
                self.screen.blit(entity.surf, entity.rect)

            self.level.run()
            font = pygame.font.SysFont("Serif", 25)
            text = font.render(f"Score: {self.score} Time: {round(time.time() - self.start, 2)}", True,
                               (255, 255, 255))
            self.screen.blit(text, [0, 0])

        # pygame.draw.circle(screen, (255, 255, 255), self.player.rect[:2],
        #                    distance_points(self.player.rect[:2], self.dummy.rect[:2]))
        point = find_point_circle(self.player.rect[:2], self.dummy.rect[:2], self.dummy.speed,
                                  distance_points(self.player.rect[:2], self.dummy.rect[:2]))

        # pygame.draw.rect(screen, (10, 200, 140), point + (25, 25))
        pygame.display.flip()


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    running = True
    game = Game(screen)

    while running:
        running = game.process_events()
        game.run_logic()
        game.display_frame()
        clock.tick(60)
        # print(clock.get_fps())

    pygame.quit()


if __name__ == "__main__":
    main()

# helped with bullet trajectory: https://stackoverflow.com/questions/43951409/pygame-bullet-motion-from-point-a-to-point-b


"""
for other_enemy in self.enemies_sprites_list:
    if enemy.rect.colliderect(other_enemy.rect) and other_enemy != enemy:
        enemy.rect.x, enemy.rect.y = placeholder_x, placeholder_y
"""
