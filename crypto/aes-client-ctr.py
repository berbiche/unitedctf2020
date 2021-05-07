#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.pycryptodome python3Packages.pwntools

from itertools import zip_longest

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def fromh(b):
    return bytes.fromhex(b)


INPUT = b"aaaaaaaaaaaaaaaa"

k1 = byte_xor(fromh("3f7b27e0f3477b333b7330c6e7c60557"), INPUT)
k2 = byte_xor(fromh("590dcf9ee5a839f714ae9fd105b30ce2"), INPUT)
k3 = byte_xor(fromh("f618377e4d5529c4ced19ba40ee29477"), INPUT)

keystream = (k1, k2, k3)

print("K1:", k1, "Result:", byte_xor(INPUT, k1).hex())
print("K2:", k2, "Result:", byte_xor(INPUT, k2).hex())
print("K3:", k3, "Result:", byte_xor(INPUT, k3).hex())

FLAG = fromh("185607c6bf14786162256290e2c501005a08cc9cb4ad3aa011fccbd35de455baf24c672a19")
print("Len FLAG", len(FLAG))

decoded = ''
for (kst, st) in zip(keystream, zip_longest(*[iter(FLAG)] * 16, fillvalue='')):
    for (p, k) in zip(st, kst):
        if len(decoded) == 37:
            break
        ch = p ^ k
        decoded += chr(ch)
        print("Char:", chr(ch))

print(decoded)
