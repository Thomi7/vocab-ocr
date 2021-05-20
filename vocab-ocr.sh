#!/bin/sh
# $1: path
# $2: image filename
# $3: from tesseract language code
# $4: to tesseract language code
# $5: modus

path="$1"
filename="$2"
from_lang="$3"
to_lang="$4"
mode="$5"

postprocess_text()
{
    echo "$1" | sed -e 's/,/;/'         `# replace , by ; (, is used as csv delimiter)` \
                    -e '/^\W*$/d'       `# remove white lines` \
                    -e 's/\s*$//'       `# remove trailing spaces`
}

postprocess_greenwich_text()
{
    echo "$1" | vim -c "silent! %s/\(\S.*\)-\s*$\n\(\S.*\)$/\1\2/g" \
                    -c "silent! %s/\(\S.*\)$\n\(\S.*\)$/\1 \2/g" -c "wq! $path/sed" - > /dev/null

    sed "$path/sed" -e 's/\[.*$//'      `# remove everything after [` \
                    -e 's/|.*$//'       `# remove everything after |` \
                    -e 's/{.*$//'       `# remove everything after {` \
                    -e 's/AF/AE/'       `# replace 'AF' with 'AE'` \
                    -e 's/p\//pl/'      `# replace 'p/' with`
}

convert -crop 50%x100% +repage "$path/$filename" "$path/split.png"
if [ "$mode" = "greenwich" ]
then
    convert -fuzz 40% -fill black -opaque "#000000" -monochrome "$path/split-0.png" "$path/split-0.png"
    convert -fuzz 50% -fill black -opaque "#000000" -opaque "#0000FF" -monochrome "$path/split-1.png" "$path/split-1.png"

    postprocess_text "$(postprocess_greenwich_text "$(tesseract -l "$from_lang" "$path/split-0.png" stdout)")" > "$from_lang"
    postprocess_text "$(postprocess_greenwich_text "$(tesseract -l "$to_lang" "$path/split-1.png" stdout)")" > "$to_lang"
    paste -d"," "$from_lang" "$to_lang" > "$path/out.csv"
else
    convert -monochrome "$path/split-0.png" "$path/split-0.png"
    convert -monochrome "$path/split-1.png" "$path/split-1.png"

    postprocess_text "$(tesseract -l "$from_lang" "$path/split-0.png" stdout)" > "$from_lang"
    postprocess_text "$(tesseract -l "$to_lang" "$path/split-1.png" stdout)" > "$to_lang"
    paste -d"," "$from_lang" "$to_lang" > "$path/out.csv"
fi
