#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools python3Packages.pylint

from pwn import *

HOST = ("challenges.unitedctf.ca", 3004)
con = remote(HOST[0], HOST[1])

while True:
    result = con.recv(1024)
    print(str(result, 'utf-8'))
    con.sendline(bytes(result))

