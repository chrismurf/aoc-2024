#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class WalkResult(Enum):
    MOVED = 0
    TURNED = 1
    DESERTED = 2
    LOOPING = 3

@dataclass
class Guard:
    map: dict[(int, int): bool]
    visits: dict[(int, int): set[Direction]]
    bounds: tuple[int, int]
    position: tuple[int, int]
    direction: Direction

    def walk(self) -> WalkResult:
        dr, dc = {Direction.UP: (-1, 0),
                  Direction.DOWN: (1, 0),
                  Direction.LEFT: (0, -1),
                  Direction.RIGHT: (0, 1)}[self.direction]
        new_position = self.position[0] + dr, self.position[1] + dc
        if new_position[0] > self.bounds[0] or \
           new_position[1] > self.bounds[1] or \
           new_position[0] < 0 or \
           new_position[1] < 0:
            return WalkResult.DESERTED
        if self.map[new_position]:
            self.direction = {
                Direction.UP: Direction.RIGHT,
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.UP,
            }[self.direction]
            if self.direction in self.visits.get(self.position, set()):
                return WalkResult.LOOPING
            else:
                self.visits.setdefault(self.position, set()).add(self.direction)
                return WalkResult.TURNED
        else:
            self.position = new_position
            if self.direction in self.visits.get(self.position, set()):
                return WalkResult.LOOPING
            else:
                self.visits.setdefault(self.position, set()).add(self.direction)
                return WalkResult.MOVED

## Load map
with open("./input.txt", "r") as f:
    map = {}
    for row, line in enumerate(f.readlines()):
        for col, char in enumerate(line.strip()):
            map[(row, col)] = char == "#"
            if char == "^":
                init_guard_pos = (row, col)

## Create a guard, and have him walk the floor until he deserts (or loops)
pt1_guard = Guard(map, {init_guard_pos: {Direction.UP}}, (row, col), init_guard_pos, Direction.UP)
while pt1_guard.walk() not in {WalkResult.DESERTED, WalkResult.LOOPING}:
    pass

## Count how many squares the guard visited
count = 0
for visit in pt1_guard.visits:
    if visit: count += 1
print(f"Initial path visits {count} squares.")

## Now consider putting an obstacle someplace in the Part 1 guard's path (because otherwise he
## wouldn't hit it) and see if it results in a loop.  Count the loops.
loop_count = 0
for r in range(row+1):
    for c in range(col+1):
        # Skip places the pt1 guard never visits, or where they start, or there's already an obstacle
        if not pt1_guard.visits.get((r,c), set()) or init_guard_pos == (r, c) or map[(r,c)]:
            continue

        # Create a new guard
        guard = Guard(map, {init_guard_pos: {Direction.UP}}, (row, col), init_guard_pos, Direction.UP)

        # Put an obstacle in the path, run until desertion or looping, then remove the obstacle from the map
        guard.map[(r,c)] = True
        while (result := guard.walk()) not in {WalkResult.DESERTED, WalkResult.LOOPING}:
            pass
        guard.map[(r,c)] = False

        if result == WalkResult.LOOPING:
            loop_count += 1
print(f"{loop_count} obstacle options resulted in loops.")