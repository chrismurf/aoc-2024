#!/usr/bin/env python3
import re

with open("./input.txt", "r") as f:
    raw = f.read()

matches = re.finditer(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)", raw, re.MULTILINE)

part1_total = 0
part2_total = 0
enabled = True
for match in matches:
    if match.group(0) == "do()":
        enabled = True
    elif match.group(0) == "don't()":
        enabled = False
    else:
        a = int(match.group(1))
        b = int(match.group(2))
        part1_total += a*b
        if enabled: part2_total += a*b

print(part1_total)
print(part2_total)
