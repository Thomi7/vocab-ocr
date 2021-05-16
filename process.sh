#!/bin/sh
# $1: path
# $2: image filename

path=$1
filename=$2

from_lang="eng"
to_lang="deu"

# split in half, color to gray
convert -crop 50%x100% +repage "$path/$filename" "$path/split.png"

ocr()
{
    tesseract -l "$1" "$2" stdout | sed 's/\[.*$//' | sed 's/,/;/' | sed 's/‘.*$//'| sed 's/".*$//' | sed 's/|.*$//'| sed '/^$/d' | sed '/^\W\+$/d' > "$path/$1.txt"
}

# ocr from language
convert -threshold 50% -monochrome split-0.png split-0.png
ocr "$from_lang" "$path/split-0.png"

# ocr to language
convert -threshold 50% -monochrome split-1.png split-1.png
ocr "$to_lang" "$path/split-1.png"

# merge to csv
paste -d"," "$path/$from_lang.txt" "$path/$to_lang.txt" > "$path/merged.csv"

# convert to xlsx
ssconvert "$path/merged.csv" "$path/out.xlsx"
