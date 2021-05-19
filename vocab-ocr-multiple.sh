#!/bin/sh
# $1: path
# $2: image base filename
# $3: from tesseract language code
# $4: to tesseract language code
# $5: count of images

path=$1

for i in `seq 1 $5`
do
    vocab-ocr "$path" "$2$i" "$3" "$4"
    cat "$path/out.csv" >> "$path/concat.csv"
done
