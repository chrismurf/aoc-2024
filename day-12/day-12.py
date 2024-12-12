#!/usr/bin/env python3
from enum import Enum

RC = tuple[int, int]
RIGHT: RC = (0, 1)
DOWN: RC = (1, 0)
LEFT: RC = (0, -1)
UP: RC = (-1, 0)

def fill_region(
        garden: dict[RC, str],
        counted: dict[RC, bool],
        r0: int,
        c0: int
) -> tuple[set[RC], int, set[RC]]:
    
    edges = set()
    veggie = garden[(r0, c0)]

    region = set()
    new_cells = {(r0, c0)}
    while new_cells:
        region = region.union(new_cells)
        next_new_cells = set()
        for r, c in new_cells:
            counted[(r,c)] = True
            for (dr, dc) in [RIGHT, DOWN, LEFT, UP]:
                if garden.get((r+dr, c+dc), None) == veggie:
                    if not counted.get((r+dr, c+dc), True):
                        counted[(r+dr, c+dc)] = True
                        next_new_cells.add((r+dr, c+dc))
                else:
                    edges.add(((dr, dc), r, c))
        new_cells = next_new_cells
    return edges, region

with open("input.txt", "r") as f:
    garden = {}
    for r, line in enumerate(f.readlines()):
        for c, char in enumerate(line.strip()):
            garden[(r,c)] = char
nrows, ncols = r+1, c+1

counted = {(r, c): False for r in range(nrows) for c in range(ncols)}
regions = []
for r in range(nrows):
    for c in range(ncols):
        if not counted[(r, c)]:
            # regions = [(veggie, edges, region), ...]
            regions.append((garden[(r, c)], *fill_region(garden, counted, r, c)))

# Sum up the perimeter
total_cost = sum((len(edges) * len(region) for (_, edges, region) in regions))
print(f"Part 1: {total_cost}")

def count_sides(edges) -> int:
    sides = 0

    horz_edges = [(dir, r, c) for dir, r, c in edges if dir in (UP, DOWN)]
    vert_edges = [(dir, c, r) for dir, r, c in edges if dir not in (UP, DOWN)]

    prev_dir, prev_r, prev_c = None, None, None
    for dir, c, r in sorted(vert_edges):
        if dir != prev_dir or c != prev_c or r-1 != prev_r: sides += 1
        prev_dir, prev_r, prev_c = dir, r, c

    prev_dir, prev_r, prev_c = None, None, None
    for dir, r, c in sorted(horz_edges):
        if dir != prev_dir or r != prev_r or c != prev_c + 1: sides += 1
        prev_dir, prev_r, prev_c = dir, r, c

    return sides


# Now walk the boundary of each region and figure out the number of sides
total_cost = sum((count_sides(edges) * len(region) for (_, edges, region) in regions))
print(f"Part 2: {total_cost}")