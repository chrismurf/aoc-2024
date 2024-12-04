#!/usr/bin/env python3
import numpy as np
from scipy import signal

X,M,A,S = map(ord, 'XMAS')

PT1_MATCH = X**2 + M**2 + A**2 + S**2
VALID_PT1_PATTERNS = [
  [[X,M,A,S]],

  [[S,A,M,X]],

  [[X, 0, 0, 0],
   [0, M, 0, 0],
   [0, 0, A, 0],
   [0, 0, 0, S]],

  [[S, 0, 0, 0],
   [0, A, 0, 0],
   [0, 0, M, 0],
   [0, 0, 0, X]],

  [[0, 0, 0, X],
   [0, 0, M, 0],
   [0, A, 0, 0],
   [S, 0, 0, 0]],

  [[0, 0, 0, S],
   [0, 0, A, 0],
   [0, M, 0, 0],
   [X, 0, 0, 0]],

  [[S],[A],[M],[X]],

  [[X],[M],[A],[S]],
]

PT2_MATCH = 2*M**2 + A**2 + 2*S**2
VALID_PT2_PATTERNS = [
  [[M, 0, S],
   [0, A, 0],
   [M, 0, S]],

  [[M, 0, M],
   [0, A, 0],
   [S, 0, S]],

  [[S, 0, M],
   [0, A, 0],
   [S, 0, M]],

  [[S, 0, S],
   [0, A, 0],
   [M, 0, M]],
]


data = np.fromfile("./input.txt", dtype="B").reshape((-1,141))[:,:-1]

part1 = 0
for pattern in VALID_PT1_PATTERNS:
    output = signal.convolve2d(data, pattern, 'valid')
    part1 += (output == PT1_MATCH).sum()

part2 = 0
for pattern in VALID_PT2_PATTERNS:
    output = signal.convolve2d(data, pattern, 'valid')
    part2 += (output == PT2_MATCH).sum()

print(part1)
print(part2)
