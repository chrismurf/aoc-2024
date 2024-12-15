#!/usr/bin/env python3
import sys
import time
from enum import Enum
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np

@dataclass(frozen=True)
class Point:
    r: int
    c: int

    def __add__(self, o):
        return Point(self.r + o.r, self.c + o.c)

UP = Point(-1, 0)
RIGHT = Point(0, 1)
DOWN = Point(1, 0)
LEFT = Point(0, -1)

DIR_SYMBOLS = {UP: "^", RIGHT: ">", DOWN: "v", LEFT: "<"}

class Spot(Enum):
    WALL = 0
    BOX = 1
    BOX_LH = 2
    BOX_RH = 3
    EMPTY = 4

pt1_map : dict[Point, Spot] = {}
pt2_map : dict[Point, Spot] = {}
robot = None, None
robot2 = None, None
directions = []
with open("input.txt", "r") as f:
    for r, line in enumerate(f):
        if not line.strip(): break # Move onto parsing directions
        for c, char in enumerate(line.strip()):
            if char == '.':
                pt1_map[Point(r,c)] = Spot.EMPTY
                pt2_map[Point(r,2*c)] = Spot.EMPTY
                pt2_map[Point(r,2*c+1)] = Spot.EMPTY
            elif char == '#':
                pt1_map[Point(r,c)] = Spot.WALL
                pt2_map[Point(r,2*c)] = Spot.WALL
                pt2_map[Point(r,2*c+1)] = Spot.WALL
            elif char == 'O':
                pt1_map[Point(r,c)] = Spot.BOX
                pt2_map[Point(r,2*c)] = Spot.BOX_LH
                pt2_map[Point(r,2*c+1)] = Spot.BOX_RH
            elif char == '@':
                pt1_map[Point(r,c)] = Spot.EMPTY
                pt2_map[Point(r,2*c)] = Spot.EMPTY
                pt2_map[Point(r,2*c+1)] = Spot.EMPTY
                robot = Point(r, c)
                robot2 = Point(r, 2*c)
            else:
                print(f"Error parsing '{char}' at {r}, {c}")
                sys.exit(0)
    HEIGHT, WIDTH = r, c+1

    for line in f:
        if not line.strip(): break # Done parsing
        for char in line.strip():
            if char == '^': directions.append(UP)
            elif char == '>': directions.append(RIGHT)
            elif char == 'v': directions.append(DOWN)
            elif char == '<': directions.append(LEFT)
            else:
                print(f"Error parsing '{char}'")
                sys.exit(0)

for direction in directions:
    next_robot = robot + direction
    if pt1_map[next_robot] == Spot.EMPTY:
        robot = next_robot
    elif pt1_map[next_robot] == Spot.WALL:
        continue
    elif pt1_map[next_robot] == Spot.BOX:
        new_box_spot = next_robot + direction
        while pt1_map[new_box_spot] == Spot.BOX:
            new_box_spot += direction
        if pt1_map[new_box_spot] == Spot.WALL:
            continue # Can't push into a wall
        else: # Must be an empty spot - move some boxes!
            pt1_map[new_box_spot] = Spot.BOX
            pt1_map[next_robot] = Spot.EMPTY
            robot = next_robot

pt1_score = 0
for point, spot in pt1_map.items():
    if spot == Spot.BOX:
        pt1_score += 100*point.r + point.c
print(f"Part 1 is: {pt1_score}")

########

def try_move(map: dict[Point, Spot], robot : Point, direction : Point):
    next_robot = robot + direction
    if map[next_robot] == Spot.EMPTY:
        return next_robot
    elif map[next_robot] == Spot.WALL:
        return robot
    elif direction in (LEFT, RIGHT) and map[next_robot] in (Spot.BOX_LH, Spot.BOX_RH):
        to_move = set((next_robot, ))
        to_explore = set((next_robot + direction, ))
    elif direction in (UP, DOWN) and map[next_robot] == Spot.BOX_LH:
        to_move = set()
        to_explore = set((next_robot, next_robot + RIGHT))
    elif direction in (UP, DOWN) and map[next_robot] == Spot.BOX_RH:
        to_move = set()
        to_explore = set((next_robot, next_robot + LEFT))
    else:
        print("ERROR")

    while to_explore:
        to_move.update(to_explore)
        to_iterate = to_explore.copy()
        to_explore.clear()
        for box_spot in to_iterate:
            next_spot = box_spot + direction

            if map[next_spot] == Spot.WALL:
                return robot
            elif direction in (LEFT, RIGHT) and map[next_spot] in (Spot.BOX_LH, Spot.BOX_RH):
                to_move.add(next_spot)
                to_explore.add(next_spot + direction)
            elif direction in (UP, DOWN) and map[next_spot] == Spot.BOX_LH:
                to_explore.add(next_spot)
                to_explore.add(next_spot + RIGHT)
            elif direction in (UP, DOWN) and map[next_spot] == Spot.BOX_RH:
                to_explore.add(next_spot)
                to_explore.add(next_spot + LEFT)
        
    # Move the furthest boxes first so we fill in the empty spots they leave behind
    def sort_order(point: Point):
        if direction == LEFT: return point.c
        elif direction == RIGHT: return -point.c
        elif direction == UP: return point.r
        elif direction == DOWN: return -point.r

    order_to_move = sorted(to_move, key=sort_order)
    for box_spot in order_to_move:
        part_type = map[box_spot]
        map[box_spot] = Spot.EMPTY
        map[box_spot + direction] = part_type
    return next_robot

for direction in directions:
    robot2 = try_move(pt2_map, robot2, direction)

pt2_score = 0
for point, spot in pt2_map.items():
    if spot == Spot.BOX_LH:
        pt2_score += 100*point.r + point.c
print(f"Part 2 is: {pt2_score}")