#!/bin/sh

from_lang="eng"
to_lang="deu"

# split in half, color to gray
convert -colorspace Gray -crop 50%x100% +repage "$1" split.png

ocr()
{
tesseract -l "$1" "$2" stdout | sed 's/\[.*$//' | sed 's/,/;/' | sed 's/‘.*$//'| sed 's/".*$//' | sed 's/|.*$//'| sed '/^$/d' | sed '/^\W\+$/d' > "$1.txt"
}

# ocr from language
ocr "$from_lang" "split-0.png"

# ocr to language
ocr "$to_lang" "split-1.png"

# merge to csv
paste -d"," "$from_lang.txt" "$to_lang.txt" > merged.csv

# convert to xlsx
ssconvert merged.csv out.xlsx
