from PIL import Image
import pytesseract
import cv2
import math
import re
import tempfile
import os
import numpy as np

def process(image, lang_from, lang_to, preprocess_from, preprocess_to, postprocess_from, postprocess_to, tmp_dir=tempfile.TemporaryDirectory()):

    # cv2.imshow('output', cv2.resize(image, None, fx=0.3, fy=0.3))
    # cv2.waitKey()

    # split image horizontally in half
    height, width = image.shape[0:2]
    half_width = math.floor(width/2)
    image_from = image[0:height, 0:half_width]
    image_to = image[0:height, half_width+1:width]

    preprocess_from(image_from)
    preprocess_to(image_to)

    image_from_path = os.path.join(tmp_dir.name, 'from.png')
    cv2.imwrite(image_from_path, image_from)
    image_to_path = os.path.join(tmp_dir.name, 'to.png')
    cv2.imwrite(image_to_path, image_to)

    text_from = pytesseract.image_to_string(image_from_path, lang=lang_from)
    text_to = pytesseract.image_to_string(image_to_path, lang=lang_to)

    # print(text_from)
    # cv2.imshow('test', image_from)
    # cv2.waitKey(0)

    text_from = postprocess_text(postprocess_from(text_from))
    text_to = postprocess_text(postprocess_to(text_to))

    out = ""
    for line1, line2 in zip(text_from.split('\n'), text_to.split('\n')):
        out += line1 + "," + line2 + "\n"
    return out;

def postprocess_text(text):
    text = text.replace(',', ';')                                   # replace , by ; (, is used as csv delimiter)
    text = re.sub(r'^\s*\n', '', text, 0, re.MULTILINE)             # remove white lines
    text = re.sub(r'\s*$', '', text, 0, re.MULTILINE)               # remove trailing spaces
    return text

def postprocess_text_greenwich(text):
    text = re.sub(r'-\s*\n(\S)', r'\1', text, 0, re.MULTILINE)      # replace hyphen line break with concatenated word

    text = re.sub(r'\[.*$', '', text, 0, re.MULTILINE)              # remove everything after [
    text = re.sub(r'\|.*$', '', text, 0, re.MULTILINE)              # remove everything after |
    text = re.sub(r'{.*$', '', text, 0, re.MULTILINE)               # remove everything after {
    text = text.replace('AF', 'AE')                                 # replace 'AF' with 'AE'
    text = text.replace('p/', 'pl')                                 # replace 'p/' with 'pl'
    return text

def preprocess_image_greenwich_from(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    lower = np.array([0,0,0])
    i = 170
    upper = np.array([i,i,i]) # BGR
    mask = cv2.inRange(image, lower, upper)
    image = cv2.bitwise_and(image, image, mask= mask)

    mask = cv2.bitwise_not(mask)
    bk = np.full(image.shape, 255, dtype=np.uint8)
    bkg = cv2.bitwise_and(bk, bk, mask=mask)
    image = cv2.bitwise_or(image, bkg)

    # cv2.imshow('output', cv2.resize(image, None, fx=0.4, fy=0.4))
    # cv2.waitKey()
    return image

def preprocess_image_greenwich_to(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.line(image, (0, 0), (0, 300), (255, 0, 0), 5)
    # image = cv2.line(image, (100, 0), (100, 300), (0, 255, 0), 5)
    # image = cv2.line(image, (200, 0), (200, 300), (0, 0, 255), 5)
    lower = np.array([0,0,0])
    upper = np.array([255,200,180]) # BGR
    mask = cv2.inRange(image, lower, upper)
    image = cv2.bitwise_and(image, image, mask= mask)

    mask = cv2.bitwise_not(mask)
    bk = np.full(image.shape, 255, dtype=np.uint8)
    bkg = cv2.bitwise_and(bk, bk, mask=mask)
    image = cv2.bitwise_or(image, bkg)

    cv2.imshow('output', cv2.resize(image, None, fx=0.4, fy=0.4))
    cv2.waitKey()
    return image

image='Untitled2.png'
print(process(image, 'eng', 'deu', preprocess_image_greenwich_from, preprocess_image_greenwich_to,
        postprocess_text_greenwich, postprocess_text_greenwich))
