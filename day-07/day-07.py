#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass
class CalibrationEquation:
    test_value: int
    values: list[int]

    @staticmethod
    def from_line(line) -> 'CalibrationEquation':
        left, _, right = line.strip().partition(":")
        return CalibrationEquation(int(left), tuple(map(int, right.split())))

def recursively_solve(values, result_so_far, allow_concat=False):
    if not values:
        yield result_so_far
        return

    for value in recursively_solve(values[:-1], values[-1], allow_concat):
        yield result_so_far * value
        yield result_so_far + value
        if allow_concat:
            yield int(str(value) + str(result_so_far))

def sum_solvable(problems, allow_concat):
    score = 0
    for problem in problems:
        for possible_result in recursively_solve(problem.values[:-1], problem.values[-1], allow_concat):
            if possible_result == problem.test_value:
                score += problem.test_value
                break
    return score

# Parse all the problems
problems : list[CalibrationEquation] = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        problems.append(CalibrationEquation.from_line(line))

print(f"Part 1: {sum_solvable(problems, False)}")
print(f"Part 2: {sum_solvable(problems, True)}")
