#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.pycryptodome python3Packages.pwntools

from itertools import zip_longest

LEN_FLAG = len(b"&flag=False")
LEN_FLAG2 = len(b"&flag=True")

#INPUT1 = b"name=" + b"a" * 11 + b"a" * (16 - LEN_FLAG2) + b"bflag=True" + b"a" (16 - LEN_FLAG) + b"&flag=False"

# Extract the "&flag="
INPUT1 = b"name=" + b"a" * 11 + b"a" * (16 - 6)
print(INPUT1.replace(b'name=', b''))

# Extract "True"aaaaaaaaaaa
INPUT2 = b"name=" + b"a" * 11 + b"True"
print(INPUT2.replace(b'name=', b''))

# Extract "&"aaaaaaaaaaaa

R_INPUT1 = bytes.fromhex("153b2a65af4ac1e3904fd903cf2b575a8eb6d9c8ef003c6785b71fe8b729925b557337173ababfbaf2a81d523789bf1d")

R_INPUT2 = bytes.fromhex("153b2a65af4ac1e3904fd903cf2b575a4b46e3b3805821ff339a2c2eccf7293b")

# "name=aaaaaaaaaaa" == len(16)
FIRST_PART = R_INPUT1[:16]
# "aaaaaaaaaa&flag=" == len(16)
SECOND_PART = R_INPUT1[16:32]
# "True&flag=False\0" == len(16)
THIRD_PART = R_INPUT2[16:32]

print(len(FIRST_PART), FIRST_PART.hex())
print(len(SECOND_PART), SECOND_PART.hex())
print(len(THIRD_PART), THIRD_PART.hex())

print(len(FIRST_PART + SECOND_PART + THIRD_PART), (FIRST_PART + SECOND_PART + THIRD_PART).hex())



'''
name = input("> Enter your name: ").replace("&", "").replace("=", "")
name = remove_newline(name)

cookie = f"name={name}&flag=False"
ciphertext = aes.encrypt(pad(cookie.encode(), 16))

print(f"Cookie: {cookie}")
print(f"Ciphertext: {ciphertext.hex()}")
elif choice == "2":
cookie = input("> Enter your cookie: ")
cookie = bytes.fromhex(cookie)

plaintext = unpad(aes.decrypt(cookie), 16).decode()

for entry in plaintext.split("&"):
    key, value = entry.split("=")

    if key == "flag" and value == "True":
        print(flag.flag)
'''
