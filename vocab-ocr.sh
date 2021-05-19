#!/bin/sh
# $1: path
# $2: image filename
# $3: from tesseract language code
# $4: to tesseract language code

path="$1"
filename="$2"
from_lang="$3"
to_lang="$4"

# threshold=50
# [ ! -z $5 ] && threshold=$5

# split in half, color to gray
# convert -threshold "$threshold%" -monochrome -crop 50%x100% +repage "$path/$filename" "$path/split.png"
convert -crop 50%x100% +repage "$path/$filename" "$path/split.png"
# convert -threshold "30%" -monochrome "$path/split-0.png" "$path/split-0.png"
# convert -threshold "$threshold%" -monochrome "$path/split-1.png" "$path/split-1.png"

ocr()
{
    tesseract -l "$1" "$2" stdout \
        | sed   -e 's/\[.*$//'      `# remove everything after [` \
                -e 's/,/;/'         `# replace , by ; (, is used as csv delimiter)` \
                -e 's/‘.*$//'       `# remove everything after ‘` \
                -e 's/".*$//'       `# remove everything after "` \
                -e 's/|.*$//'       `# remove everything after |` \
                -e 's/{.*$//'       `# remove everything after {` \
                -e 's/AF/AE/'       `# replace 'AF' with 'AE'` \
                -e 's/p\//pl/'      `# replace 'p/' with 'pl'` \
                -e '/^\W*$/d'       `# remove white lines` \
                -e 's/\s*$//'       `# remove trailing spaces` \
        > "$path/$1.txt"
}

# ocr from language
convert "$path/split-0.png" -fuzz 40% -fill black -opaque "#000000" "$path/split-0.png"
convert -threshold 10% -monochrome "$path/split-0.png" "$path/split-0.png"
ocr "$from_lang" "$path/split-0.png"

# ocr to language
convert "$path/split-1.png" -fuzz 50% -fill black -opaque "#0000FF" -opaque "#000000" "$path/split-1.png"
convert -threshold 10% -monochrome "$path/split-1.png" "$path/split-1.png"
ocr "$to_lang" "$path/split-1.png"

# merge to csv
paste -d"," "$path/$from_lang.txt" "$path/$to_lang.txt" > "$path/out.csv"
