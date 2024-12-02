#!/usr/bin/env python3
import numpy as np

def is_safe(report):
    deltas = [report[i+1]-report[i] for i in range(len(report)-1)]
    return all([x >= 1 and x <= 3 for x in deltas]) or \
           all([x >= -3 and x <= -1 for x in deltas])

reports = []
with open("./input.txt", "r") as f:
    for line in f.readlines():
        reports.append(list(map(int, line.split())))

part1_count = 0
part2_count = 0
for report in reports:
    if is_safe(report):
        part1_count += 1
        part2_count += 1
    else:
        for i in range(len(report)):
            dampened_report = report[:i] + report[i+1:]
            if is_safe(dampened_report):
                part2_count += 1
                break

print(f"Part 1: {part1_count}") # 585
print(f"Part 2: {part2_count}") # 626
