#!/usr/bin/env python3
from dataclasses import dataclass

with open("./input.txt", "r") as f:
    raw = f.read().strip()

## PART 1
# Parse the input into a sequence of block IDs and "None" for gaps
ordered = 9 * len(raw) * [None]
left = 0
parsing_block = True
block_id = 0
for c in map(int, raw):
    if parsing_block:
        ordered[left:left+c] = c * [block_id]
        block_id += 1
    parsing_block = not parsing_block
    left += c
ordered = ordered[:left]

# Now try to move everything into the gaps
left = 0
right = len(ordered) - 1
while left < right:
    if ordered[left] is None:
        ordered[left] = ordered[right]
        ordered[right] = None
        while ordered[right] is None and left < right:
            right -= 1
    left += 1

# Compute the part 1 total
pt1_total = 0
ordered = ordered[:left+1]
for i, value in enumerate(ordered):
    pt1_total += i*value
print(f"Part 1: {pt1_total}")

## PART 2
# You really want me to use a linked list and I'm really not gonna do it
@dataclass
class DiskSection:
    id: int | None
    blocks: int

disk = [DiskSection(None if i % 2 else i//2, c) for i, c in enumerate(map(int, raw)) if c > 0]

# Try to move each file to the left once, but only once
right = len(disk)-1
min_checked = disk[right].id + 1
while right >= 0:
    if disk[right].id is not None and disk[right].id < min_checked:
        min_checked = disk[right].id
        for left in range(min(len(disk), right)):
            if disk[left].id is None and disk[left].blocks >= disk[right].blocks:
                old_left_blocks = disk[left].blocks
                disk[left].id = disk[right].id
                disk[left].blocks = disk[right].blocks
                disk[right].id = None
                difference = old_left_blocks - disk[right].blocks
                if difference > 0:
                    disk.insert(left+1, DiskSection(None, difference))
                    right += 1
                break
    right -= 1

# Compute the part 2 total
offset = 0
pt2_total = 0
for value in disk:
    if value.id is None:
        offset += value.blocks
        continue
    for i in range(offset, offset+value.blocks):
        pt2_total += i * value.id
    offset += value.blocks
print(f"Part 2: {pt2_total}")