import math


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
