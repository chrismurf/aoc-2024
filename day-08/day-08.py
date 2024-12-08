#!/usr/bin/env python3
import itertools

antennas : dict[str, set[tuple[int, int]]] = {}

with open("input.txt", "r") as f:
    for row, line in enumerate(f.readlines()):
        for col, char in enumerate(line.strip()):
            if char != '.':
                antennas.setdefault(char, set()).add((row, col))
MAX_ROW, MAX_COL = row, col

# Part 1
pt1_antinodes = set()
for freq, locs in antennas.items():
    for (ar, ac), (br, bc) in itertools.permutations(locs, 2):
        row, col = ar + (ar-br), ac + (ac-bc)
        if row >= 0 and row <= MAX_ROW and col >= 0 and col <= MAX_COL:
            pt1_antinodes.add((row, col))

print(f"Part 1: {len(pt1_antinodes)}")

# Part 2
pt2_antinodes = set()
for freq, locs in antennas.items():
    for (ar, ac), (br, bc) in itertools.permutations(locs, 2):
        row, col = ar, ac
        dr, dc = (ar-br), (ac-bc)
        while row >= 0 and row <= MAX_ROW and col >= 0 and col <= MAX_COL:
            pt2_antinodes.add((row, col))
            row, col = row+dr, col+dc

print(f"Part 2: {len(pt2_antinodes)}")
