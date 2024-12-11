#!/usr/bin/env python3

stones = list(map(int, open("./input.txt", "r").read().strip().split()))
stones = {k:stones.count(k) for k in set(stones)}

def blink_n_times(stones, n):
    for i in range(n):
        new_stones = {}
        for value, count in stones.items():
            if value == 0:
                new_stones[1] = new_stones.get(1, 0) + count
                continue
            value_str = str(value)
            if len(value_str) % 2 == 0:
                half = len(value_str)//2
                first_half = int(value_str[:half])
                second_half = int(value_str[half:])
                new_stones[first_half] = new_stones.get(first_half, 0) + count
                new_stones[second_half] = new_stones.get(second_half, 0) + count
            else:
                value *= 2024
                new_stones[value] = new_stones.get(value, 0) + count
        stones = new_stones
    return stones

stones = blink_n_times(stones, 25)
print(f"Part 1: {sum(stones.values())}")

stones = blink_n_times(stones, 50)
print(f"Part 2: {sum(stones.values())}")
