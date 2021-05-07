#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools python3Packages.pylint

from pwn import *
from json import dumps, loads

print("Connecting...")
con = remote("challenges.unitedctf.ca", 3005)

res = con.recv(1024)

j = loads(res)
print(j)
k = j["child"]["child"]
k["grandparent"] = j["name"]
print(k)
r = dumps(k)

con.send(r.encode())

print(con.recv(1024))

