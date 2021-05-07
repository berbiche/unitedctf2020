#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools python3Packages.pylint

from pwn import *

con = remote("challenges.unitedctf.ca", 4001)

def eval(left, op, right):
    if op == '*':
        return left * right
    if op == '/':
        return left / right
    if op == '+':
        return left + right
    else:
        return left - right

while True:
    res = con.recv(1024)
    print(res)
    left, op1, middle, op2, right = str(res, 'utf-8').strip().split(' ')
    lexpr = 0
    rexpr = 0
    ans = 0
    if op1 not in ('*', '/') and op2 in ('*', '/'):
        rexpr = eval(int(middle, 10), op2, int(right, 10))
        lexpr = eval(int(left, 10), op1, rexpr)
        ans = lexpr
    else:
        lexpr = eval(int(left, 10), op1, int(middle, 10))
        rexpr = eval(lexpr, op2, int(right, 10))
        ans = rexpr

    print(f'{ans}')
    con.send(f'{ans}'.encode())

