#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.pycryptodome python3Packages.pwntools

from json import loads
from pwn import *

from Crypto.Cipher import AES
from Crypto.Util import Counter


r = remote("challenges.unitedctf.ca", 3000)

while True:
    json = loads(r.recv(1024))
    print(json)
    if 'flag' in json:
        print("Flag found!", json['flag'])
        break
    elif 'success' in json:
        print("Is successful", json['success'])
        if json['success'] == False:
            break
        else:
            continue

    res = b''
    mode, key, iv, op, data = (json['mode'], json['key'], json['iv_or_counter'], json['operation'], json['data'])
    encrypt = op == 'encrypt'
    data = bytes(data, 'utf-8') if encrypt else bytes.fromhex(data)
    key = bytes.fromhex(key)
    iv = bytes.fromhex(iv) if iv is not None else None

    print("I will encrypt?", encrypt)

    cipher = None
    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == 'CBC':
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    else:
        c = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=c)

    res = cipher.encrypt(data).hex() if encrypt else cipher.decrypt(data)

    print("Sending response", res)
    r.send(res)

