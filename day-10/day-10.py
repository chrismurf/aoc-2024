#!/usr/bin/env python3
from collections import deque

Location = tuple[int, int]
LocationDeque = deque[Location]

def find_trails(locations : LocationDeque, trailmap : dict[Location, int], next_value: int) -> list[LocationDeque]:
    if next_value > 9:
        return [deque([loc]) for loc in locations]

    trails : list[LocationDeque] = []
    for (r, c) in locations:
        next_steps : LocationDeque = deque()
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if trailmap.get((r+dr, c+dc), None) == next_value:
                next_steps.append((r+dr, c+dc))
        for trail in find_trails(next_steps, trailmap, next_value + 1):
            trail.insert(0, (r, c))
            trails.append(trail)
    return trails

with open("./input.txt", "r") as f:
    trailmap = {(r,c):int(v) for (r, line) in enumerate(f.readlines()) for (c, v) in enumerate(line.strip())}

trailheads = LocationDeque((loc for loc, v in trailmap.items() if v == 0))
trails = find_trails(trailheads, trailmap, 1)

trailhead_peaks = {}
for trail in trails:
    peaks = trailhead_peaks.setdefault(trail[0], set())
    peaks.add(trail[-1])

trail_count = {}
for trail in trails:
    trail_count[trail[0]] = trail_count.get(trail[0], 0) + 1

print(f"Part 1: {sum((len(x) for x in trailhead_peaks.values()))}")
print(f"Part 2: {sum(trail_count.values())}")