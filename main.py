import pygame
import random
import math

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def update(self, pressed_keys):
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
        # create enemy at random place
        self.rect = self.surf.get_rect(center=(
            random.randint(25, SCREEN_WIDTH - 25),
            random.randint(25, SCREEN_HEIGHT - 25)
        ))

        self.speed = 5

    def distance_points(self, point1, point2):
        """measure distance between two points"""
        x1, y1 = point1
        x2, y2 = point2
        d = math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)
        distance = math.sqrt(d)

        return distance

    def count_angle(self, point1, point2):
        """returns angle of triangle, in which point1 and point2 make hypotenuse"""

        x1, y1 = point1
        x2, y2 = point2

        # measure triangle sides
        adjacent = x2 - x1
        # avoid dividing by zero
        if adjacent == 0:
            return math.radians(90)

        opposite = y2 - y1

        # count tangent
        tan = opposite / adjacent
        # find angle using arctangent
        angle = math.atan(tan)
        angle = math.degrees(angle)

        # prevent enemy wobbling when angle is value close to 0
        if -2 < angle < 2:
            angle = 0

        return angle

    def update(self, player_position):
        # get coordinates of player and enemy
        point1 = player_position[:2]
        point2 = self.rect[:2]

        angle = self.count_angle(point1, point2)
        cosinus = math.cos(angle)
        sinus = math.sin(angle)

        # count speed on each axis
        x = cosinus * self.speed
        y = sinus * self.speed

        # make sure enemy goes in correct direction
        if (point2[0] - point1[0]) > 0:
            x = -abs(x)
        elif (point2[0] - point1[0]) < 0:
            x = abs(x)
        else:
            x = 0

        if (point2[1] - point1[1]) > 0:
            y = -abs(y)
        elif (point2[1] - point1[1]) < 0:
            y = abs(y)
        else:
            y = 0

        self.rect.move_ip(x, y)
        print(sinus, angle)


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

        # Get the set of keys pressed and check for user inputda
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)

        self.enemies_sprites_list.update((self.player.rect[0], self.player.rect[1]))

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
