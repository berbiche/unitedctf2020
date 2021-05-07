#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.pycryptodome python3Packages.pwntools

from binascii import unhexlify, hexlify
from pwn import *


con = connect('challenges.unitedctf.ca', 3003)

def receive_send(data = ''):
    con.recvuntil("> Your choice:", timeout=5)
    con.sendline(b'1')
    con.recvuntil("> Please enter your name:", timeout=5)
    if data != '':
        print(f"Sending len({len(data)})", data)
    con.sendline(data)
    result = con.recvline()
    return result.replace(b'Result:', b'').strip()

def split(st, size = 16):
    r = [hexlify(st[i:i+size]) for i in range(0, len(st), size)]
    return r

INITIAL_FLAG = receive_send()
print("INITIAL_FLAG", INITIAL_FLAG)
INITIAL_BLOCK = len(INITIAL_FLAG) / 16
print("INITIAL_BLOCK", INITIAL_BLOCK)

NUMBER_FILL_BLOCK = 1
for i in range(1, 16):
    result = len(receive_send(b"a" * i))
    if result / 16 > INITIAL_BLOCK:
        break
    else:
        NUMBER_FILL_BLOCK = i

print("Number of bytes to fill block:", NUMBER_FILL_BLOCK)

LENGTH_FLAG = len(unhexlify(INITIAL_FLAG)) - NUMBER_FILL_BLOCK
print("Length of flag to get:", LENGTH_FLAG)

FLAG = b"FLAG-"
for i in range(len(FLAG) or 1, LENGTH_FLAG + 1):
    LENFLAG = len(FLAG) or 1
    for ch in [*[str(c) for c in range(10)], 'a', 'b', 'c', 'd', 'e', 'f']:
        ch = bytes(ch, 'ascii')
        l = i % 16
        round_1 = i / 16 < 1
        spad = b'a' * (15 - l) if round_1 else b'a' * (15 - l)
        epad = b'a' * ((16 - LENFLAG % 16 - 1) % 16) if round_1 else spad

        result = receive_send(spad + FLAG + ch + epad)

        blocks = split(unhexlify(result))
        uniq = set(blocks)

        if len(blocks) - len(uniq) == 2:
            FLAG += ch
            break
        elif round_1 and len(blocks) - len(uniq) == 1:
            FLAG += ch
            break
    else:
        print("Flag found!", FLAG)
        break
    print(FLAG)
