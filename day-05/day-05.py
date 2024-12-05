#!/usr/bin/env python3

def check_update(followers: dict[int, set], update : list[int]) -> bool:
    seen = set()
    for page in update:
        seen.add(page)
        if followers.get(page, set()).intersection(seen):
            return False
    return True

def fix_update(followers: dict[int, set], update : list[int]) -> list[int]:
    fixed = []
    for this_page in update:
        # Find the first (if any) value which must *follow* this page, insert right before that.
        # If none are found, add the page to the end.
        for i, p in enumerate(fixed):
            if p in followers[this_page]:
                fixed.insert(i, this_page)
                break
        else:
            fixed.append(this_page)
    return fixed

followers : dict[int,set] = {}
updates = []

with open("./input.txt", "r") as f:
    rules_complete = False
    for line in f.readlines():
        line = line.strip()
        if line.strip() == "":
            rules_complete = True
            continue

        if rules_complete:
            updates.append(list(map(int, line.split(","))))
        else:
            before, after = map(int, line.split("|"))
            followers.setdefault(before, set()).add(after)

part1_total: int = 0
part2_total: int = 0
for update in updates:
    if check_update(followers, update):
        middle_idx = (len(update) - 1) // 2
        part1_total += update[middle_idx]

    else:
        fixed = fix_update(followers, update)
        middle_idx = (len(fixed) - 1) // 2
        part2_total += fixed[middle_idx]

print(part1_total)
print(part2_total)