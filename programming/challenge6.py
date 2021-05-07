#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: with ps; [ pwntools (pytesseract.override { tesseract = tesseract4; }) pillow opencv4 numpy google_cloud_vision ])"
import io
import base64
import string
import re

from pwn import *             # web socket
from PIL import Image         # image
import pytesseract as pyt     # OCR
import cv2 as cv              # preprocessing
import numpy as np            # preprocessing

LETTERS = string.ascii_letters + string.digits
#LETTERS = re.sub('[iIlLmMwW1]', '', string.ascii_letters + string.digits)

config = ' '.join([
    '--oem 2',
    '--psm 6',
    '-c chop_enable=T'
    '-c load_system_dawg=F',
    '-c load_unamig_dawg=F',
    '-c load_bigram_dawg=F',
    '-c load_punc_dawg=F',
    '-c load_freq_dawg=F',
    '-c segment_segcost_rating=F',
    '-c enable_new_segsearch=F',
    '-c language_model_ngram_on=F',
    '-c textord_force_make_prop_words=F',
    '-c edges_max_children_per_outline=40',
    '-c tessedit_char_whitelist=' + LETTERS,
])
print(config)


def fix_result(res):
    replacements = [
        ('IL', 'N'),
        ('Il', 'N'),
        ('II', 'N'),
        ('ll', 'N'),
        ('I', 'T'),
        ('i', 't'),
        ('l', 't'),
        # (' ', ''),
        # ('\n', ''),
    ]
    for (v, r) in replacements:
        res = res.replace(v, r)
    res = re.sub(r'\s+', ' ', res)
    return res

def get_result(result):
    result = re.sub(r'\n\s*\n', '', result)
    #print("Result:", result)

    result = ''.join(fix_result(result).split(' '))

    result = [x.replace(' ', '').strip() for x in result]
    #print("Result:", result)

    return ''.join(result) if len(result) > 0 else ''


# Extracts red color
def cv2_red(im):
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)


    # Extract the red color of the text
    lred = np.array([0, 120, 70])
    ured = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lred, ured)
    mask2 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # The image now only contains reddish colors
    res = cv.bitwise_and(im, im, mask=mask2)

    # Apply a blur to filter out characters
    res = cv.medianBlur(res, 3)

    # Invert colors from reddish to blue
    res = cv.bitwise_not(res)

    # Dilate image to "sharpen" and remove junk
    t = np.zeros((3, 3), np.uint8)
    t[1:] = 1
    v = np.ones((1, 1), np.uint8)
    res = cv.dilate(res, v, iterations=1)

    # Apply a final filter from blue -> gray -> black on white
    res = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    res = cv.threshold(res, 160, 255, cv.THRESH_BINARY)[1]

    res = cv.resize(res, None, fx=1.2, fy=1.2, interpolation=cv.INTER_LANCZOS4)

    #res6 = cv.GaussianBlur(res5, (3, 3), 5);
    #res6 = cv.bitwise_not(cv.Canny(res5, 200, 200));

    cv.imwrite('./tmp-final.jpg', res)
    return res


def detect_text(content):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts[0].description.strip() if not response.error.message else ' '


def main():
    con = remote("challenges.unitedctf.ca", 4003)

    count = -1
    while True:
        count += 1
        try:
            bytesToRead = con.recvline().strip()
        except EOFError:
            print("Failed after", count)
            con = remote("challenges.unitedctf.ca", 4003)
            count = -1
            continue

        imageOrFlag = con.recvline(keepends=False, timeout=0.5)
        if b'flag-' in imageOrFlag.lower():
            print("Flag found!", imageOrFlag)
            break
        if b'Mauvaise' in imageOrFlag:
            print("Failed attempt!")
            continue

        b64 = base64.b64decode(imageOrFlag)
        with open('./tmp.jpg', 'wb') as f:
            f.write(b64)
        image = cv.imdecode(np.frombuffer(b64, np.uint8), 1)
        res = cv2_red(image)
        print("Us:", get_result(pyt.image_to_string(res, config=config, timeout=2.5)))
    
        with open('./tmp-final.jpg', 'rb') as f:
            content = f.read()
        result = detect_text(content)
        print("Google:", result)
        con.send(result)

def offline():
    im = cv.imread('./tmp.jpg')

    res = cv2_red(im)

    result = pyt.image_to_string(res, config=config, timeout=2.5)

    print("Tesseract:", get_result(result))

    with open('./tmp-final.jpg', 'rb') as f:
        content = f.read()
    print("Google:", detect_text(content))


#main()
offline()

