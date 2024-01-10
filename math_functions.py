import math


# test
def distance_points(point1, point2):
    """measure distance between two points"""
    x1, y1 = point1
    x2, y2 = point2
    d = math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)
    distance = math.sqrt(d)

    return distance


def count_angle(point1, point2):
    """returns angle of triangle, in which point1 and point2 make hypotenuse"""

    x1, y1 = point1
    x2, y2 = point2

    # measure triangle sides
    adjacent = x2 - x1
    adjacent = abs(adjacent)
    # avoid dividing by zero
    if adjacent == 0:
        return math.radians(90)

    opposite = y2 - y1
    opposite = abs(opposite)

    # count tangent
    tan = opposite / adjacent
    # find angle using arctangent
    angle = math.atan2(opposite, adjacent)
    angle = math.degrees(angle)

    # prevent enemy wobbling when angle is value close to 0
    if -2 < angle < 2:
        angle = 0

    return angle


"""class Enemy(pygame.sprite.Sprite):
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

        angle = count_angle(point1, point2)
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
        # print(sinus, angle)
"""

"""
        for enemy in self.enemies_sprites_list:
            placeholder_x = enemy.rect.x
            placeholder_y = enemy.rect.y
            temp = pygame.sprite.spritecollideany(enemy, self.enemies_sprites_list)
            enemy.update((self.player.rect[0], self.player.rect[1]))
            for other_enemy in self.enemies_sprites_list:
                if enemy.rect.colliderect(other_enemy.rect) and other_enemy != enemy:
                    enemy.rect.x, enemy.rect.y = placeholder_x, placeholder_y
"""