#!/usr/bin/env python3
from parse import compile
import math

TEMPLATE_A = compile("Button A: X+{ax:d}, Y+{ay:d}")
TEMPLATE_B = compile("Button B: X+{bx:d}, Y+{by:d}")
TEMPLATE_P = compile("Prize: X={px:d}, Y={py:d}")

# Parse 'em
machines = []
with open("input.txt", "r") as f:
    while True:
        machine = {}
        try:
            machines.append((
                TEMPLATE_A.parse(f.readline().strip()).named |
                TEMPLATE_B.parse(f.readline().strip()).named |
                TEMPLATE_P.parse(f.readline().strip()).named
            ))
            f.readline()
        except:
            break

def total_cost(machine):
    # Watch for divide by zero errors, though this dataset had none
    try:
        # Solve two simultaneous equations.  I did math on paper, it happened.
        num = machine['py'] - (machine['px']*machine['ay']/machine['ax'])
        den = machine['by'] - (machine['bx']*machine['ay']/machine['ax'])
        b = round(num / den)
        a = round((machine['px'] - b*machine['bx'])/machine['ax'])
        # Make sure we have integer numbers of button presses
        if ((b*machine['bx'] + a*machine['ax'] == machine['px']) and
            (b*machine['by'] + a*machine['ay'] == machine['py'])):
            return 3*a + b
    except:
        pass
    return 0

cost = sum(map(total_cost, machines))
print(f"Part 1: {cost}")

# Part 2 - correct PX, PY
for machine in machines:
    machine['px'] += 10000000000000
    machine['py'] += 10000000000000

cost = sum(map(total_cost, machines))
print(f"Part 2: {cost}")
