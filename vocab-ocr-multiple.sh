#!/bin/sh
# $1: path
# $2: image base filename
# $3: from tesseract language code
# $4: to tesseract language code
# $5: mode
# $6: count of images

path=$1

for i in `seq 1 $6`
do
    vocab-ocr "$path" "$2$i" "$3" "$4" "$5"
    echo | cat "$path/out.csv" - >> "$path/concat.csv"
done
