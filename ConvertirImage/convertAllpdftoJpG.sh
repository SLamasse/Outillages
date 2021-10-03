#!/bin/bash

for inputfile in ./*.pdf ; do
    outputfile="${inputfile%.*}.jpg"
    convert  -sharpen 0x4 -verbose -density 150 -trim "$inputfile" -quality 100  -resize 900x900 "$outputfile" &&
    [[ -e "$outputfile" && "$inputfile" != "$outputfile" ]] && rm "$inputfile"
done

