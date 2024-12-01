#!/usr/bin/env python3
import numpy as np

with open("./input.txt", "r") as f:
    raw = np.array([[int(i) for i in row.split()] for row in f.read().splitlines()])
raw.sort(0)
part1 = sum(abs(raw[:,1] - raw[:,0]))
print(f"Part 1 is: {part1}")

keys = set(raw[:,0])
count = dict.fromkeys(keys, 0)
for value in raw[:,1]:
    if value in count:
        count[value] += value
part2 = sum(count.values())
print(f"Part 2 is: {part2}")
