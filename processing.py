#!/usr/bin/python3

import pytesseract
import cv2
import math
import re
import tempfile
import os
import numpy as np
import argparse

import time

def showimage(image):
    img_path = '/tmp/image' + str(round(time.time() * 1000)) + '.png'
    cv2.imwrite(img_path, image)
    print(img_path)
    cmd = 'imv ' + img_path
    os.system(cmd)

def process(image, left_lang, right_lang, preprocess_left, preprocess_right, postprocess_left, postprocess_right, tmp_dir=tempfile.TemporaryDirectory()):

    # split image horizontally in half
    height, width = image.shape[0:2]
    half_width = math.floor(width/2)
    left_image = image[0:height, 0:half_width]
    right_image = image[0:height, half_width+1:width]

    left_image = preprocess_left(left_image)
    right_image = preprocess_right(right_image)

    left_image_path = os.path.join(tmp_dir.name, 'left.png')
    cv2.imwrite(left_image_path, left_image)
    right_image_path = os.path.join(tmp_dir.name, 'right.png')
    cv2.imwrite(right_image_path, right_image)

    left_text = pytesseract.image_to_string(left_image_path, lang=left_lang)
    right_text = pytesseract.image_to_string(right_image_path, lang=right_lang)

    left_text = postprocess_text(postprocess_left(left_text))
    right_text = postprocess_text(postprocess_right(right_text))

    left_split = left_text.split('\n')
    right_split = right_text.split('\n')
    # extend splits to match each others length
    for _ in range(0,len(left_split)-len(right_split)):
        right_split += ['']
    for _ in range(0,len(right_split)-len(left_split)):
        left_split += ['']
    out = ''
    for line1, line2 in zip(left_split, right_split):
        out += line1 + ',' + line2 + '\n'
    return out.strip();

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

def preprocess_image_greenwich_left(image):

    # remove non-black pixels
    lower = np.array([0,0,0])
    threshold = 120 # 100-120
    upper = np.array([threshold, threshold, threshold]) # BGR
    mask = cv2.inRange(image, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)

    # make non-black pixels white
    mask = cv2.bitwise_not(mask)
    full_white = np.full(image.shape, 255, dtype=np.uint8)
    image = cv2.bitwise_or(image, cv2.bitwise_and(full_white, full_white, mask=mask))

    return image

def preprocess_image_greenwich_right(image):
    original = image

    # make blue pixels black and remove non-blue pixels
    threshold = 150
    lower = np.array([255-threshold , 0, 0])
    upper = np.array([255, threshold, threshold]) # BGR
    mask = cv2.inRange(image, lower, upper)
    full_black = np.full(image.shape, 0, dtype=np.uint8)
    image = cv2.bitwise_and(image, full_black, mask= mask)

    # readd old background
    mask = cv2.bitwise_not(mask)
    image = cv2.bitwise_or(image, cv2.bitwise_and(original, original, mask=mask))

    # binarize image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return image

def right_image_csv(image, left_lang, right_lang, mode='default'):

    # only default pre- and postprocessing in other modes
    preprocess_left = lambda i : i
    preprocess_right = lambda i : i
    postprocess_left = lambda t : t
    postprocess_right = lambda t : t

    if mode == 'greenwich':
        preprocess_left = preprocess_image_greenwich_left
        preprocess_right = preprocess_image_greenwich_right
        postprocess_left = postprocess_text_greenwich
        postprocess_right = postprocess_text_greenwich

    return process(image, left_lang, right_lang, preprocess_left, preprocess_right, postprocess_left, postprocess_right)

def images_to_csv(images, left_lang, right_lang, mode='default'):
    out = ""
    for image in images:
        out += right_image_csv(image, left_lang, right_lang, mode) + "\n\n"
    return out.strip()

def process_directory(dir_path, left_lang, right_lang, mode='default'):
    images=[]
    for image in sorted(os.listdir(dir_path)):
        images.append(cv2.imread(os.path.join(dir_path, image)))
    return images_to_csv(images, left_lang, right_lang, mode)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', metavar='path', type=str,
                    help='path to directory where images are in')
parser.add_argument('left_lang', metavar='left-lang', type=str,
                    help='language of left column (tesseract lang code, e.g. deu, eng)')
parser.add_argument('right_lang', metavar='right-lang', type=str,
                    help='language of right column (tesseract lang code, e.g. deu, eng)')
parser.add_argument('mode', metavar='mode', type=str, nargs='?',
                    help='image processing mode (default, greenwich)')
args = parser.parse_args()

if 'mode' in args:
    print(process_directory(args.path, args.left_lang, args.right_lang, args.mode))
else:
    print(process_directory(args.path, args.left_lang, args.right_lang))
