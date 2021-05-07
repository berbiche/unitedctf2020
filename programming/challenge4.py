#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools python3Packages.pylint john

import hashlib
from itertools import product
from pwn import *

con = remote("challenges.unitedctf.ca", 4002)

def hashbreak(passwordHash):
    for length in range(1, 7):
        for chars in product(list('0123456789'), repeat=length):
            hashed = hashlib.sha1(''.join(chars).encode('utf-8')).hexdigest()
            if hashed == passwordHash:
                return ''.join(chars)
    else:
        print("No solutions")
        return None

while True:
    res = con.recv(1024)
    print(res)
    breaked = hashbreak(str(res, 'utf-8').strip())
    print(breaked)
    con.send(breaked.encode())

