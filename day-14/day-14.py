#!/usr/bin/env python3
from parse import compile
from functools import reduce
import math
from matplotlib import pyplot as plt
import numpy as np

TEMPLATE = compile("p={px:d},{py:d} v={vx:d},{vy:d}")
WIDTH, HEIGHT = 101, 103

with open("input.txt", "r") as f:
    poses = [TEMPLATE.parse(line.strip()).named for line in f]

def move(pose, seconds):
    return {
        'px': (pose['px'] + seconds * pose['vx']) % WIDTH,
        'py': (pose['py'] + seconds * pose['vy']) % HEIGHT,
        'vx':pose['vx'],
        'vy':pose['vy']
    }

new_poses = [move(pose, 100) for pose in poses]
QUADRANT1 = reduce(lambda a, b: a+1 if b['px'] < WIDTH//2 and b['py'] < HEIGHT//2 else a, new_poses, 0)
QUADRANT2 = reduce(lambda a, b: a+1 if b['px'] > WIDTH//2 and b['py'] < HEIGHT//2 else a, new_poses, 0)
QUADRANT3 = reduce(lambda a, b: a+1 if b['px'] < WIDTH//2 and b['py'] > HEIGHT//2 else a, new_poses, 0)
QUADRANT4 = reduce(lambda a, b: a+1 if b['px'] > WIDTH//2 and b['py'] > HEIGHT//2 else a, new_poses, 0)
print(QUADRANT1 * QUADRANT2 * QUADRANT3 * QUADRANT4)
print(len(poses))

# I'm not proud of this but it worked.
step = 0
while step < 30000:
    print (f"Step {step}          ", end="\r")
    img = np.zeros((HEIGHT, WIDTH), dtype=np.uint16)
    for pose in poses:
        img[pose['py'], pose['px']] += 1
        pose['px'] = (pose['px'] + pose['vx']) % WIDTH
        pose['py'] = (pose['py'] + pose['vy']) % HEIGHT
    if not (img > 1).any():
        print(f"\n\n UNIQUE ON STEP {step}\n\n")
    plt.figure(0)
    plt.imshow(img, interpolation='nearest')
    plt.title(f"{step:05d}")
    plt.savefig(f"frames/example_{step:05d}.png")
    plt.clf()
    step += 1
