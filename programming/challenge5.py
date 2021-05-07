#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools

from itertools import repeat
from pwn import *

matrix = []
start = ()
end = ()

def map_to_pos(s, pos):
    if s == '#':
        return 0
    elif s == '0':
        return 1
    elif s == 'D':
        global start
        start = pos
        return 'S'
    elif s == 'F':
        global end
        end = pos
        return 'X'
    else:
        raise 'What??'

con = remote("challenges.unitedctf.ca", 3006)

line_count = int(con.recvline().strip(), 10)
print("Line count", line_count)

matrix = [[0 for _ in range(line_count)] for _ in range(line_count)]

for i in range(0, line_count):
    line = list(str(con.recvline(), "utf-8").strip())
    print(line)
    for c in range(0, len(line)):
        matrix[i][c] = map_to_pos(line[c], (i, c))

print("Start", start)
print("End", end)
print("Matrix")
for c in matrix:
    print(list(map(str, c)))

def solve(matrix, start, end):
    global solution
    solution = []
    visited = []

    def dist(pos1, pos2):
        return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

    def realsolve(pos, goal):
        visited.append(pos)
        if pos == goal:
            return True
        if matrix[pos[0]][pos[1]] == 0:
            print("Ignoring wall", pos)
            return False

        left = right = up = down = None
        if pos[1] - 1 > 0:
            left = (pos[0], pos[1] - 1)
        if pos[1] + 1 < len(matrix) - 1:
            right = (pos[0], pos[1] + 1)
        if pos[0] - 1 > 0:
            up = (pos[0] - 1, pos[1])
        if pos[0] + 1 < len(matrix) - 1:
            down = (pos[0] + 1, pos[1])

        to_visit = [x for x in [left, right, up, down] if x is not None and x not in visited and matrix[x[0]][x[1]] != 0]

        to_visit = sorted(to_visit, key=lambda x: dist(x, goal))
        print(f"{pos}: to visit", to_visit)
        
        for pos in to_visit:
            if realsolve(pos, goal):
                solution.append(pos)
                return True
        else:
            return False

    realsolve(start, end)
    return [start] + solution[::-1]


path = solve(matrix, start, end)
print(path)

sol_length = len(path)
sol_str = '\n'.join(map(lambda x: f'{x[1]} {x[0]}', path))

final_sol = f'{sol_length}\n{sol_str}'

print(final_sol.encode())

con.send(final_sol.encode())

print(con.recvline())

